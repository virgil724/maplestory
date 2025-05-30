def hex_parse(hex_string):
    # 將 hex 字符串轉換為 bytes
    data = bytes.fromhex(hex_string)

    # 計算 byte 位置
    start = 0x0037  # 55 bytes
    end = 0x006C  # 106 bytes

    # 進行 byte 位移
    result = data[end - start :]

    # MegaphoneData 字段
    0x006C - 0x0037
    0x0079 - 0x0037
    print(data[0x006C - start : 0x0079 - start].hex())

    # Channel 字段
    0x0081
    0x0088
    print(data[0x0081 - start : 0x0089 - start].hex())
    # Value
    0x0090 + 2
    ch_start = 0x008A
    ch_val = data[ch_start - start : ch_start + 2 - start].hex()
    print(ch_val)
    # to dec (little endian)
    ch_value = int.from_bytes(bytes.fromhex(ch_val), "little")
    print("channel (dec):", ch_value)
    # Text 字段
    text_start = 0x0093
    text_end = text_start + 4
    text_val = data[text_start - start : text_end - start].hex()
    print(text_val)
    text_type_start = 0x0097
    text_type_end = text_type_start + 2
    print(data[text_type_start - start : text_type_end - start].hex())
    text_len_start = 0x0099
    text_len_end = text_len_start + 4
    text_len = data[text_len_start - start : text_len_end - start].hex()
    print(text_len)
    # from text_len_end + text_len
    text_len_value = int.from_bytes(bytes.fromhex(text_len), "little")
    print(text_len_value)
    text_value_start = text_len_end
    text_value_end = text_value_start + text_len_value
    text_value = data[text_value_start - start : text_value_end - start].decode("utf-8")
    print(text_value)
    # Nickname 字段
    nickname_start = text_value_end + 5
    nickname_end = nickname_start + 8
    print(data[nickname_start - start : nickname_end - start].hex())
    # 2 bytes type
    nickname_type_start = nickname_end
    nickname_type_end = nickname_type_start + 2
    print(data[nickname_type_start - start : nickname_type_end - start].hex())
    # 4 bytes value
    nickname_value_start = nickname_type_end
    nickname_value_end = nickname_value_start + 4
    nickname_value = data[
        nickname_value_start - start : nickname_value_end - start
    ].hex()
    print(nickname_value)
    # to dec (little endian)
    nickname_value_dec = int.from_bytes(bytes.fromhex(nickname_value), "little")
    print(nickname_value_dec)
    nickname_start = nickname_value_end
    nickname_end = nickname_start + nickname_value_dec
    nickname_value = data[nickname_start - start : nickname_end - start].decode("utf-8")
    print(nickname_value)
    # Type 字段
    type_start = nickname_end + 5
    type_end = type_start + 4
    print(data[type_start - start : type_end - start].hex())
    type_type_start = type_end
    type_type_end = type_type_start + 2
    print(data[type_type_start - start : type_type_end - start].hex())
    type_value_len_start = type_type_end
    type_value_len_end = type_value_len_start + 4
    type_value_len = data[
        type_value_len_start - start : type_value_len_end - start
    ].hex()
    print(type_value_len)
    # to dec (little endian)
    type_value_dec = int.from_bytes(bytes.fromhex(type_value_len), "little")
    print(type_value_dec)
    type_value_start = type_value_len_end
    type_value_end = type_value_start + type_value_dec
    type_value = data[type_value_start - start : type_value_end - start].decode()
    print(type_value)
    # Whisper 字段
    whisper_start = type_value_end + 5
    whisper_end = whisper_start + 7
    print(data[whisper_start - start : whisper_end - start].hex())
    # ProfileCode 字段
    profile_code_start = whisper_end + 7
    profile_code_end = profile_code_start + 11
    print(data[profile_code_start - start : profile_code_end - start].hex())

    profile_type_start = profile_code_end
    profile_type_end = profile_type_start + 2
    print(data[profile_type_start - start : profile_type_end - start].hex())

    profile_len_start = profile_type_end
    profile_len_end = profile_len_start + 4
    profile_len = data[profile_len_start - start : profile_len_end - start].hex()
    print(profile_len)
    profile_len_value = int.from_bytes(bytes.fromhex(profile_len), "little")

    print(profile_len_value)

    profile_value_start = profile_len_end
    profile_value_end = profile_value_start + profile_len_value
    profile_value = data[
        profile_value_start - start : profile_value_end - start
    ].decode("utf-8")

    print(profile_value)
    # UserId 字段
    user_id_start = profile_value_end + 5
    user_id_end = user_id_start + 6
    print(data[user_id_start - start : user_id_end - start].hex())
    user_id_type_start = user_id_end
    user_id_type_end = user_id_type_start + 2
    print(data[user_id_type_start - start : user_id_type_end - start].hex())
    user_id_len_start = user_id_type_end
    user_id_len_end = user_id_len_start + 4
    user_id_len = data[user_id_len_start - start : user_id_len_end - start].hex()
    print(user_id_len)
    user_id_len_value = int.from_bytes(bytes.fromhex(user_id_len), "little")
    print(user_id_len_value)
    user_id_value_start = user_id_len_end
    user_id_value_end = user_id_value_start + user_id_len_value
    user_id_value = data[
        user_id_value_start - start : user_id_value_end - start
    ].decode("utf-8")
    print(user_id_value)
    # Color1
    color1_start = user_id_value_end + 6
    color1_end = color1_start + 7
    print(data[color1_start - start : color1_end - start].hex())
    # Color2
    color2_start = color1_end + 6
    color2_end = color2_start + 7
    print(data[color2_start - start : color2_end - start].hex())

    print(result.hex())
    return result


if __name__ == "__main__":
    hex_data = "544f5a2021010000ffffffff02210100006135f07dffffffff0098ac25cf01000000f20000800b000000000b01000016000d0000004d65676170686f6e65446174610700000000070000004368616e6e656c0213030000000400000054657874040041000000373837e887aae794b1e58d96e4b880e5bca0e880b3e6958f3630e58db7efbc8ce4bbb7e9ab98e88085e5be97efbc8ce79bb4e68ea5e69da5e4b88de59b9ee7a78100080000004e69636b6e616d650400050000004775636369000400000054797065040007000000353132303031310007000000576869737065720701000b00000050726f66696c65436f64650400050000004c384c794f000600000055736572496404001100000032303337323130303030353330373537300400070000002335463037333804000700000023656462306365"
    hex_parse(hex_data)
