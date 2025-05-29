import json
import time
import threading
from datetime import datetime
from mitmproxy import ctx, tcp


class TCPExportAddon:
    def __init__(self):
        self.tcp_connections = {}  # 使用字典以便快速查找
        self.output_file = "tcp_connections.json"
        self.auto_save_interval = 10  # 每10秒自動保存一次
        self.last_save_time = time.time()
        self.message_counter = 0

        # 啟動自動保存線程
        self.start_auto_save()

    def start_auto_save(self):
        """啟動自動保存線程"""

        def auto_save_worker():
            while True:
                time.sleep(self.auto_save_interval)
                if self.tcp_connections:
                    self.save_connections()

        save_thread = threading.Thread(target=auto_save_worker, daemon=True)
        save_thread.start()
        ctx.log.info(
            f"Auto-save started, will save every {self.auto_save_interval} seconds"
        )

    def tcp_start(self, flow: tcp.TCPFlow):
        """當 TCP 連線開始時記錄"""
        connection_info = {
            "id": flow.id,
            "client_address": f"{flow.client_conn.address[0]}:{flow.client_conn.address[1]}",
            "server_address": f"{flow.server_conn.address[0]}:{flow.server_conn.address[1]}"
            if flow.server_conn.address
            else "Unknown",
            "start_time": datetime.now().isoformat(),
            "last_activity": datetime.now().isoformat(),
            "status": "active",
            "message_count": 0,
            "total_bytes": 0,
            "messages": [],
        }
        self.tcp_connections[flow.id] = connection_info
        ctx.log.info(
            f"TCP connection started: {connection_info['client_address']} -> {connection_info['server_address']}"
        )

        # 立即保存新連線
        self.save_connections()

    def tcp_message(self, flow: tcp.TCPFlow):
        """記錄 TCP 訊息並實時更新"""
        if flow.id not in self.tcp_connections:
            return

        connection = self.tcp_connections[flow.id]

        # 處理新訊息
        current_message_count = len(flow.messages)
        if current_message_count > connection["message_count"]:
            # 有新訊息
            new_messages = flow.messages[connection["message_count"] :]

            for message in new_messages:
                self.message_counter += 1
                message_info = {
                    "sequence": self.message_counter,
                    "timestamp": datetime.now().isoformat(),
                    "from_client": message.from_client,
                    "content_hex": message.content.hex()
                    if hasattr(message.content, "hex")
                    else str(message.content),
                    "length": len(message.content),
                    "direction": "client->server"
                    if message.from_client
                    else "server->client",
                }
                connection["messages"].append(message_info)
                connection["total_bytes"] += len(message.content)

            # 更新連線統計
            connection["message_count"] = current_message_count
            connection["last_activity"] = datetime.now().isoformat()

            ctx.log.info(
                f"New TCP message: {connection['client_address']} -> {connection['server_address']}, "
                f"Size: {len(new_messages[-1].content)} bytes, Total messages: {current_message_count}"
            )

            # 如果距離上次保存超過5秒，則立即保存
            current_time = time.time()
            if current_time - self.last_save_time > 5:
                self.save_connections()

    def tcp_end(self, flow: tcp.TCPFlow):
        """當 TCP 連線結束時更新記錄"""
        if flow.id in self.tcp_connections:
            connection = self.tcp_connections[flow.id]
            connection["end_time"] = datetime.now().isoformat()
            connection["status"] = "closed"
            ctx.log.info(
                f"TCP connection ended: {connection['client_address']} -> {connection['server_address']}"
            )

            # 連線結束時立即保存
            self.save_connections()

    def save_connections(self):
        """保存連線數據到 JSON 文件"""
        try:
            # 轉換為列表格式以便保存
            connections_list = list(self.tcp_connections.values())

            # 添加統計信息
            export_data = {
                "export_time": datetime.now().isoformat(),
                "total_connections": len(connections_list),
                "active_connections": len(
                    [c for c in connections_list if c["status"] == "active"]
                ),
                "total_messages": sum(c["message_count"] for c in connections_list),
                "connections": connections_list,
            }

            with open(self.output_file, "w", encoding="utf-8") as f:
                json.dump(export_data, f, indent=2, ensure_ascii=False)

            self.last_save_time = time.time()
            ctx.log.info(
                f"TCP connections saved: {len(connections_list)} connections, "
                f"{export_data['total_messages']} total messages"
            )

        except Exception as e:
            ctx.log.error(f"Failed to save TCP connections: {e}")

    def tcp_error(self, flow: tcp.TCPFlow):
        """處理 TCP 錯誤"""
        if flow.id in self.tcp_connections:
            connection = self.tcp_connections[flow.id]
            connection["status"] = "error"
            connection["error_time"] = datetime.now().isoformat()
            ctx.log.warn(
                f"TCP connection error: {connection['client_address']} -> {connection['server_address']}"
            )
            self.save_connections()

    def done(self):
        """當 mitmproxy 關閉時保存所有數據"""
        self.save_connections()
        ctx.log.info(
            f"Final save: {len(self.tcp_connections)} TCP connections recorded"
        )


# 註冊 addon
addons = [TCPExportAddon()]
