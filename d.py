from pydantic import BaseModel
from scapy.all import AsyncSniffer
import time


class MegaphoneData(BaseModel):
    data: str


class Channel(BaseModel):
    hex: str
    value: int


class Text(BaseModel):
    field: str
    type: str
    length: int
    value: str


class Nickname(BaseModel):
    field: str
    type: str
    length: int
    value: str


class Type(BaseModel):
    field: str
    type: str
    length: int
    value: str


class ProfileCode(BaseModel):
    field: str
    type: str
    length: int
    value: str


class UserId(BaseModel):
    field: str
    type: str
    length: int
    value: str


class ParsedData(BaseModel):
    megaphone_data: MegaphoneData
    channel: Channel
    text: Text
    nickname: Nickname
    type: Type
    whisper: str
    profile_code: ProfileCode
    user_id: UserId
    color1: str
    color2: str


def hex_parse(hex_string) -> ParsedData:
    # 將 hex 字符串轉換為 bytes
    data = bytes.fromhex(hex_string)

    # 計算 byte 位置
    start = 0x0037  # 55 bytes
    _ = 0x006C  # 106 bytes

    # MegaphoneData 字段
    megaphone_data = data[0x006C - start : 0x0079 - start].hex()
    if megaphone_data != "4d65676170686f6e6544617461":
        raise ValueError("MegaphoneData field is not valid")

    # Channel 字段
    channel_hex = data[0x0081 - start : 0x0089 - start].hex()
    ch_start = 0x008A
    ch_val = data[ch_start - start : ch_start + 2 - start].hex()
    ch_value = int.from_bytes(bytes.fromhex(ch_val), "little")

    # Text 字段
    text_start = 0x0093
    text_end = text_start + 4
    text_val = data[text_start - start : text_end - start].hex()

    text_type_start = 0x0097
    text_type_end = text_type_start + 2
    text_type = data[text_type_start - start : text_type_end - start].hex()

    text_len_start = 0x0099
    text_len_end = text_len_start + 4
    text_len = data[text_len_start - start : text_len_end - start].hex()
    text_len_value = int.from_bytes(bytes.fromhex(text_len), "little")

    text_value_start = text_len_end
    text_value_end = text_value_start + text_len_value
    text_value = data[text_value_start - start : text_value_end - start].decode("utf-8")

    # Nickname 字段
    nickname_start = text_value_end + 5
    nickname_end = nickname_start + 8
    nickname_field = data[nickname_start - start : nickname_end - start].hex()

    nickname_type_start = nickname_end
    nickname_type_end = nickname_type_start + 2
    nickname_type = data[nickname_type_start - start : nickname_type_end - start].hex()

    nickname_value_start = nickname_type_end
    nickname_value_end = nickname_value_start + 4
    nickname_value = data[
        nickname_value_start - start : nickname_value_end - start
    ].hex()
    nickname_value_dec = int.from_bytes(bytes.fromhex(nickname_value), "little")

    nickname_start = nickname_value_end
    nickname_end = nickname_start + nickname_value_dec
    nickname_value = data[nickname_start - start : nickname_end - start].decode("utf-8")

    # Type 字段
    type_start = nickname_end + 5
    type_end = type_start + 4
    type_field = data[type_start - start : type_end - start].hex()

    type_type_start = type_end
    type_type_end = type_type_start + 2
    type_type = data[type_type_start - start : type_type_end - start].hex()

    type_value_len_start = type_type_end
    type_value_len_end = type_value_len_start + 4
    type_value_len = data[
        type_value_len_start - start : type_value_len_end - start
    ].hex()
    type_value_dec = int.from_bytes(bytes.fromhex(type_value_len), "little")

    type_value_start = type_value_len_end
    type_value_end = type_value_start + type_value_dec
    type_value = data[type_value_start - start : type_value_end - start].decode()

    # Whisper 字段
    whisper_start = type_value_end + 5
    whisper_end = whisper_start + 7
    whisper = data[whisper_start - start : whisper_end - start].hex()

    # ProfileCode 字段
    profile_code_start = whisper_end + 7
    profile_code_end = profile_code_start + 11
    profile_code_field = data[
        profile_code_start - start : profile_code_end - start
    ].hex()

    profile_type_start = profile_code_end
    profile_type_end = profile_type_start + 2
    profile_type = data[profile_type_start - start : profile_type_end - start].hex()

    profile_len_start = profile_type_end
    profile_len_end = profile_len_start + 4
    profile_len = data[profile_len_start - start : profile_len_end - start].hex()
    profile_len_value = int.from_bytes(bytes.fromhex(profile_len), "little")

    profile_value_start = profile_len_end
    profile_value_end = profile_value_start + profile_len_value
    profile_value = data[
        profile_value_start - start : profile_value_end - start
    ].decode("utf-8")

    # UserId 字段
    user_id_start = profile_value_end + 5
    user_id_end = user_id_start + 6
    user_id_field = data[user_id_start - start : user_id_end - start].hex()

    user_id_type_start = user_id_end
    user_id_type_end = user_id_type_start + 2
    user_id_type = data[user_id_type_start - start : user_id_type_end - start].hex()

    user_id_len_start = user_id_type_end
    user_id_len_end = user_id_len_start + 4
    user_id_len = data[user_id_len_start - start : user_id_len_end - start].hex()
    user_id_len_value = int.from_bytes(bytes.fromhex(user_id_len), "little")

    user_id_value_start = user_id_len_end
    user_id_value_end = user_id_value_start + user_id_len_value
    user_id_value = data[
        user_id_value_start - start : user_id_value_end - start
    ].decode("utf-8")

    # Color1
    color1_start = user_id_value_end + 6
    color1_end = color1_start + 7
    color1 = data[color1_start - start : color1_end - start].hex()

    # Color2
    color2_start = color1_end + 6
    color2_end = color2_start + 7
    color2 = data[color2_start - start : color2_end - start].hex()

    return ParsedData(
        megaphone_data=MegaphoneData(data=megaphone_data),
        channel=Channel(hex=channel_hex, value=ch_value),
        text=Text(
            field=text_val, type=text_type, length=text_len_value, value=text_value
        ),
        nickname=Nickname(
            field=nickname_field,
            type=nickname_type,
            length=nickname_value_dec,
            value=nickname_value,
        ),
        type=Type(
            field=type_field,
            type=type_type,
            length=type_value_dec,
            value=type_value,
        ),
        whisper=whisper,
        profile_code=ProfileCode(
            field=profile_code_field,
            type=profile_type,
            length=profile_len_value,
            value=profile_value,
        ),
        user_id=UserId(
            field=user_id_field,
            type=user_id_type,
            length=user_id_len_value,
            value=user_id_value,
        ),
        color1=color1,
        color2=color2,
    )


def hex_parse_by_field_search(hex_string) -> ParsedData:
    """
    使用搜尋欄位名稱來定位並解析資料的版本
    """
    # 將 hex 字符串轉換為 bytes
    data = bytes.fromhex(hex_string)

    def find_field_offset(field_name: str) -> int:
        """尋找欄位名稱在資料中的位置"""
        field_bytes = field_name.encode("utf-8")
        field_hex = field_bytes.hex()
        hex_data = data.hex()

        # 尋找欄位名稱在 hex 字串中的位置
        pos = hex_data.find(field_hex)
        if pos == -1:
            raise ValueError(f"Field '{field_name}' not found in data")

        # 轉換為 byte 位置
        return pos // 2

    # 尋找 MegaphoneData 字段
    megaphone_offset = find_field_offset("MegaphoneData")
    megaphone_data = data[megaphone_offset : megaphone_offset + 13].hex()

    # 尋找 Channel 字段
    channel_offset = find_field_offset("Channel")
    channel_hex = data[channel_offset : channel_offset + 7].hex()

    # Channel 值在字段名稱後的固定偏移
    ch_val_offset = channel_offset + 7 + 1  # 字段名稱 + 類型標識
    ch_val = data[ch_val_offset : ch_val_offset + 2].hex()
    ch_value = int.from_bytes(bytes.fromhex(ch_val), "little")

    # 尋找 Text 字段
    text_offset = find_field_offset("Text")
    text_field = data[text_offset : text_offset + 4].hex()

    # Text 相關數據的偏移
    text_type_offset = text_offset + 4
    text_type = data[text_type_offset : text_type_offset + 2].hex()

    text_len_offset = text_type_offset + 2
    text_len = data[text_len_offset : text_len_offset + 4].hex()
    text_len_value = int.from_bytes(bytes.fromhex(text_len), "little")

    text_value_offset = text_len_offset + 4
    text_value = data[text_value_offset : text_value_offset + text_len_value].decode(
        "utf-8"
    )

    # 尋找 Nickname 字段
    nickname_offset = find_field_offset("Nickname")
    nickname_field = data[nickname_offset : nickname_offset + 8].hex()

    nickname_type_offset = nickname_offset + 8
    nickname_type = data[nickname_type_offset : nickname_type_offset + 2].hex()

    nickname_len_offset = nickname_type_offset + 2
    nickname_len = data[nickname_len_offset : nickname_len_offset + 4].hex()
    nickname_len_value = int.from_bytes(bytes.fromhex(nickname_len), "little")

    nickname_value_offset = nickname_len_offset + 4
    nickname_value = data[
        nickname_value_offset : nickname_value_offset + nickname_len_value
    ].decode("utf-8")

    # 尋找 Type 字段
    type_offset = find_field_offset("Type")
    type_field = data[type_offset : type_offset + 4].hex()

    type_type_offset = type_offset + 4
    type_type = data[type_type_offset : type_type_offset + 2].hex()

    type_len_offset = type_type_offset + 2
    type_len = data[type_len_offset : type_len_offset + 4].hex()
    type_len_value = int.from_bytes(bytes.fromhex(type_len), "little")

    type_value_offset = type_len_offset + 4
    type_value = data[type_value_offset : type_value_offset + type_len_value].decode(
        "utf-8"
    )

    # 尋找 Whisper 字段
    whisper_offset = find_field_offset("Whisper")
    whisper = data[whisper_offset : whisper_offset + 7].hex()

    # 尋找 ProfileCode 字段
    profile_code_offset = find_field_offset("ProfileCode")
    profile_code_field = data[profile_code_offset : profile_code_offset + 11].hex()

    profile_type_offset = profile_code_offset + 11
    profile_type = data[profile_type_offset : profile_type_offset + 2].hex()

    profile_len_offset = profile_type_offset + 2
    profile_len = data[profile_len_offset : profile_len_offset + 4].hex()
    profile_len_value = int.from_bytes(bytes.fromhex(profile_len), "little")

    profile_value_offset = profile_len_offset + 4
    profile_value = data[
        profile_value_offset : profile_value_offset + profile_len_value
    ].decode("utf-8")

    # 尋找 UserId 字段
    user_id_offset = find_field_offset("UserId")
    user_id_field = data[user_id_offset : user_id_offset + 6].hex()

    user_id_type_offset = user_id_offset + 6
    user_id_type = data[user_id_type_offset : user_id_type_offset + 2].hex()

    user_id_len_offset = user_id_type_offset + 2
    user_id_len = data[user_id_len_offset : user_id_len_offset + 4].hex()
    user_id_len_value = int.from_bytes(bytes.fromhex(user_id_len), "little")

    user_id_value_offset = user_id_len_offset + 4
    user_id_value = data[
        user_id_value_offset : user_id_value_offset + user_id_len_value
    ].decode("utf-8")

    # Color1 和 Color2 需要根據前面字段的結束位置來計算
    # 這裡使用相對於 UserId 值結束位置的偏移
    color1_offset = user_id_value_offset + user_id_len_value + 6
    color1 = data[color1_offset : color1_offset + 7].hex()

    color2_offset = color1_offset + 7 + 6
    color2 = data[color2_offset : color2_offset + 7].hex()

    return ParsedData(
        megaphone_data=MegaphoneData(data=megaphone_data),
        channel=Channel(hex=channel_hex, value=ch_value),
        text=Text(
            field=text_field, type=text_type, length=text_len_value, value=text_value
        ),
        nickname=Nickname(
            field=nickname_field,
            type=nickname_type,
            length=nickname_len_value,
            value=nickname_value,
        ),
        type=Type(
            field=type_field,
            type=type_type,
            length=type_len_value,
            value=type_value,
        ),
        whisper=whisper,
        profile_code=ProfileCode(
            field=profile_code_field,
            type=profile_type,
            length=profile_len_value,
            value=profile_value,
        ),
        user_id=UserId(
            field=user_id_field,
            type=user_id_type,
            length=user_id_len_value,
            value=user_id_value,
        ),
        color1=color1,
        color2=color2,
    )


def post_to_ntfy(data: ParsedData):
    import requests

    url = "http://192.168.1.112//artale_maplestory"  # Replace with your ntfy topic URL
    headers = {"Title": "廣播"}
    message = f"""
    Megaphone Data: {data.megaphone_data.data}
    Channel: {data.channel.hex} (Value: {data.channel.value})
    Text: {data.text.value} (Type: {data.text.type}, Length: {data.text.length})
    Nickname: {data.nickname.value} (Field: {data.nickname.field}, Type: {data.nickname.type}, Length: {data.nickname.length})
    Type: {data.type.value} (Field: {data.type.field}, Type: {data.type.type}, Length: {data.type.length})
    Whisper: {data.whisper}
    Profile Code: {data.profile_code.value} (Field: {data.profile_code.field}, Type: {data.profile_code.type}, Length: {data.profile_code.length})
    User ID: {data.user_id.value} (Field: {data.user_id.field}, Type: {data.user_id.type}, Length: {data.user_id.length})
    Color1: {data.color1}
    Color2: {data.color2}
    """
    response = requests.post(url, data=message.encode("utf-8"))


if __name__ == "__main__":
    hex_data = "544f5a2006010000ffffffff02060100006135f07dffffffff0098ac25cf01000000f20000800b00000000f000000016000d0000004d65676170686f6e65446174610700000000070000004368616e6e656c02e8060000000400000054657874040027000000e68891e98099e9a0bbe694b637e5bcb5e9a0ade79b94e6958fe68db73130302520e99baae694b600080000004e69636b6e616d6504000400000041746f6d000400000054797065040007000000353132303031310007000000576869737065720701000b00000050726f66696c65436f64650400050000007267663246000600000055736572496404001100000032303337323130303030353233373635330400070000002335463037333804000700000023656462306365"
    result = hex_parse_by_field_search(hex_data)
    print(result)

    def packet_handler(packet):
        if packet.haslayer("Raw"):
            raw_data = packet["Raw"].load
            hex_data = raw_data.hex()
            # print(f"Raw packet data: {hex_data}")

            # Try to parse the packet if it looks like our expected format
            try:
                if len(hex_data) > 100:  # Basic length check
                    result = hex_parse_by_field_search(hex_data)
                    print(f"Parsed data: {result.text}")
                    post_to_ntfy(result)

            except Exception as e:
                print(f"Failed to parse packet: {e}")

    t = AsyncSniffer(
        filter="tcp port 32800",
        prn=packet_handler,
        store=False,
    )
    t.start()

    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        print("\nStopping packet capture...")
        t.stop()
        t.join()
