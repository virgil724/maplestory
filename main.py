def hex_to_ascii_chinese(hex_string):
    """
    將十六進制字符串轉換為ASCII和中文字符

    Args:
        hex_string (str): 十六進制字符串 (例如: "48656c6c6f20e4b896e7958c")

    Returns:
        str: 解碼後的字符串，包含ASCII和中文字符
    """
    try:
        # 移除可能的空格和前綴
        hex_string = hex_string.replace(" ", "").replace("0x", "")

        # 確保十六進制字符串長度為偶數
        if len(hex_string) % 2 != 0:
            hex_string = "0" + hex_string

        # 將十六進制轉換為bytes
        byte_data = bytes.fromhex(hex_string)

        # 嘗試使用UTF-8解碼
        try:
            result = byte_data.decode("utf-8")
            return result
        except UnicodeDecodeError:
            # 如果UTF-8失敗，嘗試使用GBK (簡體中文)
            try:
                result = byte_data.decode("gbk")
                return result
            except UnicodeDecodeError:
                # 如果都失敗，使用Big5 (繁體中文)
                try:
                    result = byte_data.decode("big5")
                    return result
                except UnicodeDecodeError:
                    # 最後使用latin-1，這幾乎不會失敗
                    result = byte_data.decode("latin-1")
                    return result

    except ValueError as e:
        return f"錯誤：無效的十六進制字符串 - {e}"
    except Exception as e:
        return f"錯誤：{e}"


def hex_to_ascii_chinese_advanced(hex_string, encoding="utf-8"):
    """
    高級版本：指定編碼的十六進制轉換函數

    Args:
        hex_string (str): 十六進制字符串
        encoding (str): 指定的編碼格式 (utf-8, gbk, big5, ascii等)

    Returns:
        dict: 包含結果和詳細信息的字典
    """
    try:
        # 移除可能的空格和前綴
        hex_string = hex_string.replace(" ", "").replace("0x", "")

        # 確保十六進制字符串長度為偶數
        if len(hex_string) % 2 != 0:
            hex_string = "0" + hex_string

        # 將十六進制轉換為bytes
        byte_data = bytes.fromhex(hex_string)

        result = {
            "original_hex": hex_string,
            "byte_length": len(byte_data),
            "encoding_used": encoding,
            "success": False,
            "decoded_text": "",
            "error": None,
        }

        try:
            decoded_text = byte_data.decode(encoding)
            result["success"] = True
            result["decoded_text"] = decoded_text
        except UnicodeDecodeError as e:
            result["error"] = f"使用 {encoding} 編碼解碼失敗: {e}"

        return result

    except ValueError as e:
        return {
            "original_hex": hex_string,
            "success": False,
            "error": f"無效的十六進制字符串: {e}",
        }
    except Exception as e:
        return {"original_hex": hex_string, "success": False, "error": f"未知錯誤: {e}"}


def demo_hex_to_chinese():
    """
    演示函數的使用方法
    """
    print("=== 十六進制轉換為ASCII和中文字符演示 ===\n")

    # 測試案例
    test_cases = [
        ("48656c6c6f", "Hello (英文)"),
        ("e4b896e7958c", "世界 (中文UTF-8)"),
        ("48656c6c6f20e4b896e7958c", "Hello 世界 (混合)"),
        ("d0bdd0b5d180d0b8d0b2d0b5d182", "привет (俄文)"),
        ("e38193e38293e381abe381a1e381af", "こんにちは (日文)"),
    ]

    for hex_str, description in test_cases:
        print(f"十六進制: {hex_str}")
        print(f"描述: {description}")

        # 使用基本函數
        result1 = hex_to_ascii_chinese(hex_str)
        print(f"基本轉換結果: {result1}")

        # 使用高級函數
        result2 = hex_to_ascii_chinese_advanced(hex_str)
        if result2["success"]:
            print(f"高級轉換結果: {result2['decoded_text']}")
        else:
            print(f"高級轉換錯誤: {result2['error']}")

        print("-" * 50)


def parse_maplestory_packet(hex_string):
    """
    解析楓之谷封包的具體實現
    專門處理像你提供的範例格式
    """
    try:
        # 移除可能的空格和前綴
        hex_string = hex_string.replace(" ", "").replace("0x", "")
        
        # 確保十六進制字符串長度為偶數
        if len(hex_string) % 2 != 0:
            hex_string = "0" + hex_string

        # 將十六進制轉換為bytes
        byte_data = bytes.fromhex(hex_string)
        
        result = {
            "raw_hex": hex_string,
            "total_length": len(byte_data),
            "parsed_fields": {},
            "readable_text": []
        }
        
        # 解析封包頭部
        if len(byte_data) >= 4:
            header = byte_data[:3]  # TOZ
            result["parsed_fields"]["header"] = header.decode('ascii', errors='ignore')
        
        # 尋找關鍵字段
        packet_str = byte_data.decode('utf-8', errors='ignore')
        
        # 提取 MegaphoneData 相關信息
        if "MegaphoneData" in packet_str:
            result["packet_type"] = "MegaphoneData"
            
            # 使用正則表達式或字符串查找來提取字段
            import re
            
            # 查找 Nickname
            nickname_match = re.search(r'Nickname.*?([A-Za-z0-9]+)', packet_str)
            if nickname_match:
                result["parsed_fields"]["nickname"] = nickname_match.group(1)
            
            # 查找 UserId
            userid_match = re.search(r'UserId.*?(\d{10,})', packet_str)
            if userid_match:
                result["parsed_fields"]["user_id"] = userid_match.group(1)
            
            # 查找 Type
            type_match = re.search(r'Type.*?(\d{7})', packet_str)
            if type_match:
                result["parsed_fields"]["type"] = type_match.group(1)
                
            # 查找顏色代碼
            color_matches = re.findall(r'#[0-9A-Fa-f]{6}', packet_str)
            if color_matches:
                result["parsed_fields"]["colors"] = color_matches
        
        # 提取所有可讀的中文文本
        chinese_text = re.findall(r'[\u4e00-\u9fff]+', packet_str)
        if chinese_text:
            result["readable_text"] = chinese_text
            # 合併成完整消息
            full_message = ' '.join(chinese_text)
            result["parsed_fields"]["message"] = full_message
        
        # 使用更精確的二進制解析
        return parse_packet_binary(byte_data, result)
        
    except Exception as e:
        return {"error": f"解析失敗: {str(e)}", "raw_hex": hex_string}


def parse_packet_binary(byte_data, result):
    """
    精確的二進制封包解析
    """
    try:
        offset = 0
        
        # 跳過 TOZ 開頭和一些控制字節
        while offset < len(byte_data) - 1:
            # 尋找 "MegaphoneData" 字符串
            if offset + 13 < len(byte_data):
                if byte_data[offset:offset+13] == b"MegaphoneData":
                    offset += 13
                    break
            offset += 1
        
        # 解析後續的結構化數據
        fields = {}
        
        while offset < len(byte_data) - 4:
            try:
                # 檢查是否是長度前綴的字符串
                if offset + 4 < len(byte_data):
                    # 嘗試讀取字符串長度（小端序）
                    str_len = int.from_bytes(byte_data[offset:offset+4], 'little')
                    
                    # 檢查長度是否合理
                    if 1 <= str_len <= 200 and offset + 4 + str_len <= len(byte_data):
                        try:
                            string_data = byte_data[offset+4:offset+4+str_len].decode('utf-8')
                            
                            # 根據內容分類
                            if string_data == "Nickname":
                                offset += 4 + str_len
                                # 讀取下一個字符串（昵稱值）
                                if offset + 4 < len(byte_data):
                                    next_len = int.from_bytes(byte_data[offset:offset+4], 'little')
                                    if 1 <= next_len <= 50 and offset + 4 + next_len <= len(byte_data):
                                        nickname = byte_data[offset+4:offset+4+next_len].decode('utf-8')
                                        fields["nickname"] = nickname
                                        offset += 4 + next_len
                                        continue
                            
                            elif string_data == "UserId":
                                offset += 4 + str_len
                                # 讀取用戶ID
                                if offset + 4 < len(byte_data):
                                    next_len = int.from_bytes(byte_data[offset:offset+4], 'little')
                                    if 1 <= next_len <= 50 and offset + 4 + next_len <= len(byte_data):
                                        userid = byte_data[offset+4:offset+4+next_len].decode('utf-8')
                                        fields["user_id"] = userid
                                        offset += 4 + next_len
                                        continue
                            
                            elif string_data == "Type":
                                offset += 4 + str_len
                                # 讀取類型
                                if offset + 4 < len(byte_data):
                                    next_len = int.from_bytes(byte_data[offset:offset+4], 'little')
                                    if 1 <= next_len <= 50 and offset + 4 + next_len <= len(byte_data):
                                        type_val = byte_data[offset+4:offset+4+next_len].decode('utf-8')
                                        fields["type"] = type_val
                                        offset += 4 + next_len
                                        continue
                            
                            elif string_data == "Text":
                                offset += 4 + str_len
                                # 讀取消息文本
                                if offset + 4 < len(byte_data):
                                    next_len = int.from_bytes(byte_data[offset:offset+4], 'little')
                                    if 1 <= next_len <= 500 and offset + 4 + next_len <= len(byte_data):
                                        text = byte_data[offset+4:offset+4+next_len].decode('utf-8')
                                        fields["message"] = text
                                        offset += 4 + next_len
                                        continue
                            
                            elif string_data.startswith("#"):
                                # 顏色代碼
                                if "colors" not in fields:
                                    fields["colors"] = []
                                fields["colors"].append(string_data)
                                offset += 4 + str_len
                                continue
                            
                            # 如果是其他字符串，記錄並跳過
                            if len(string_data) > 0 and string_data.isprintable():
                                if "other_strings" not in fields:
                                    fields["other_strings"] = []
                                fields["other_strings"].append(string_data)
                            
                            offset += 4 + str_len
                            
                        except UnicodeDecodeError:
                            offset += 1
                    else:
                        offset += 1
                else:
                    offset += 1
                    
            except Exception:
                offset += 1
        
        # 更新結果
        result["parsed_fields"].update(fields)
        
        return result
        
    except Exception as e:
        result["binary_parse_error"] = str(e)
        return result


def format_packet_display(hex_string):
    """
    將封包格式化為類似你期望的輸出格式
    """
    try:
        # 基本解碼
        basic_result = hex_to_ascii_chinese(hex_string)
        
        # 詳細解析
        parsed_result = parse_maplestory_packet(hex_string)
        
        print("原始輸入:")
        print(f"{basic_result}")
        print()
        
        print("解析後應該是:")
        
        # 格式化輸出
        current_line = ""
        
        for char in basic_result:
            if ord(char) < 32 or ord(char) > 126:  # 非可印字符
                if char.isprintable() and '\u4e00' <= char <= '\u9fff':  # 中文字符
                    current_line += char
                else:
                    # 非可印字符，用十六進制表示
                    hex_val = f"\\x{ord(char):02x}"
                    current_line += hex_val
            else:
                current_line += char
                
        print(current_line)
        print()
        
        # 顯示結構化信息
        if "parsed_fields" in parsed_result:
            fields = parsed_result["parsed_fields"]
            print("提取的結構化數據:")
            if "nickname" in fields:
                print(f"...Nickname......{fields['nickname']}.....")
            if "user_id" in fields:
                print(f"...UserId......{fields['user_id']}.....")
            if "type" in fields:
                print(f"...Type......{fields['type']}.....")
            if "message" in fields:
                print(f"...Text..<...{fields['message']}......")
            if "colors" in fields:
                for color in fields['colors']:
                    print(f"......{color}......")
        
    except Exception as e:
        print(f"格式化失敗: {e}")


def test_your_example():
    """
    測試你提供的具體範例
    """
    print("=== 測試你的範例 ===")
    
    # 你的原始數據
    hex_data = "544f5a201c010000ffffffff021c0100006135f07dffffffff0098ac25cf01000000f20000800b000000000601000016000d0000004d65676170686f6e65446174610700000000080000004e69636b6e616d6504000500000053656e3737000600000055736572496404001100000032303337323130303030353530333839310004000000547970650400070000003531323030313100070000004368616e6e656c02cc070000000b00000050726f66696c65436f646504000500000031766e4552000700000057686973706572070100040000005465787404003c00000031393936e887aae794b120e8b3a3e99baa2031303030e99baa3d363230307720e58faae69c89e4b880e7ad8620e6b292e5b9a3e8b2b7e6b0b4e4ba860400070000002335463037333804000700000023656462306365"
    
    format_packet_display(hex_data)


def main():
    print("Hello from maplestory!")

    # 運行演示
    demo_hex_to_chinese()

    # 互動式使用示例
    print("\n=== 互動式測試 ===")
    print("您可以使用以下方式測試:")
    print('hex_result = hex_to_ascii_chinese("48656c6c6f20e4b896e7958c")')
    print("print(hex_result)  # 輸出: Hello 世界")
    
    # 測試你提供的封包數據
    test_packet = "544f5a201c010000ffffffff021c0100006135f07dffffffff0098ac25cf01000000f20000800b000000000601000016000d0000004d65676170686f6e65446174610700000000080000004e69636b6e616d6504000500000053656e3737000600000055736572496404001100000032303337323130303030353530333839310004000000547970650400070000003531323030313100070000004368616e6e656c02cc070000000b00000050726f66696c65436f646504000500000031766e4552000700000057686973706572070100040000005465787404003c00000031393936e887aae794b120e8b3a3e99baa2031303030e99baa3d363230307720e58faae69c89e4b880e7ad8620e6b292e5b9a3e8b2b7e6b0b4e4ba860400070000002335463037333804000700000023656462306365"
    
    print("\n=== 原始封包解碼 ===")
    basic_result = hex_to_ascii_chinese(test_packet)
    print(f"基本解碼結果: {basic_result}")

    # 測試楓之谷封包解析
    print("\n=== 楓之谷封包解析測試 ===")
    parsed_result = parse_maplestory_packet(test_packet)
    print("詳細解析結果:")
    for key, value in parsed_result.items():
        print(f"  {key}: {value}")

    # 測試喇叭消息分析
    print("\n=== 喇叭消息分析測試 ===")
    if "parsed_fields" in parsed_result:
        fields = parsed_result["parsed_fields"]
        print("提取的字段:")
        for field_name, field_value in fields.items():
            print(f"  {field_name}: {field_value}")
    
    if "readable_text" in parsed_result and parsed_result["readable_text"]:
        print(f"提取的中文文本: {' '.join(parsed_result['readable_text'])}")
    
    # 測試新的格式化函數
    print("\n" + "="*50)
    test_your_example()


if __name__ == "__main__":
    main()
