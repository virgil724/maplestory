# // filepath: c:\Users\virgi\maplestory\packet_structure.md
# 楓之谷擴音器封包結構定義

本文檔描述了楓之谷擴音器封包的二進制結構和字段定義。

## 封包概覽

- **起始偏移**: 0x0037 (55 bytes)
- **總體結構**: 包含擴音器數據、頻道、文本、暱稱、類型、私聊標識、個人檔案代碼、用戶ID和顏色等字段

## 字段結構詳細說明

### 1. MegaphoneData 字段
| 偏移   | 長度     | 類型  | 描述                   |
| ------ | -------- | ----- | ---------------------- |
| 0x006C | 13 bytes | ASCII | 固定值 "MegaphoneData" |

**驗證**: 必須等於 `4d65676170686f6e6544617461` (hex)

### 2. Channel 字段
| 偏移   | 長度    | 類型          | 描述       |
| ------ | ------- | ------------- | ---------- |
| 0x0081 | 8 bytes | Hex           | 頻道標識符 |
| 0x008A | 2 bytes | Little Endian | 頻道數值   |

### 3. Text 字段
| 偏移   | 長度    | 類型          | 描述         |
| ------ | ------- | ------------- | ------------ |
| 0x0093 | 4 bytes | Hex           | 文本字段標識 |
| 0x0097 | 2 bytes | Hex           | 文本類型     |
| 0x0099 | 4 bytes | Little Endian | 文本長度     |
| 0x009D | 可變    | UTF-8         | 文本內容     |

### 4. Nickname 字段
| 偏移         | 長度    | 類型          | 描述         |
| ------------ | ------- | ------------- | ------------ |
| text_end + 5 | 8 bytes | Hex           | 暱稱字段標識 |
| +8           | 2 bytes | Hex           | 暱稱類型     |
| +2           | 4 bytes | Little Endian | 暱稱長度     |
| +4           | 可變    | UTF-8         | 暱稱內容     |

### 5. Type 字段
| 偏移             | 長度    | 類型          | 描述         |
| ---------------- | ------- | ------------- | ------------ |
| nickname_end + 5 | 4 bytes | Hex           | 類型字段標識 |
| +4               | 2 bytes | Hex           | 類型類型     |
| +2               | 4 bytes | Little Endian | 類型長度     |
| +4               | 可變    | UTF-8         | 類型內容     |

### 6. Whisper 字段
| 偏移         | 長度    | 類型 | 描述     |
| ------------ | ------- | ---- | -------- |
| type_end + 5 | 7 bytes | Hex  | 私聊標識 |

### 7. ProfileCode 字段
| 偏移            | 長度     | 類型          | 描述                 |
| --------------- | -------- | ------------- | -------------------- |
| whisper_end + 7 | 11 bytes | Hex           | 個人檔案代碼字段標識 |
| +11             | 2 bytes  | Hex           | 個人檔案代碼類型     |
| +2              | 4 bytes  | Little Endian | 個人檔案代碼長度     |
| +4              | 可變     | UTF-8         | 個人檔案代碼內容     |

### 8. UserId 字段
| 偏移            | 長度    | 類型          | 描述           |
| --------------- | ------- | ------------- | -------------- |
| profile_end + 5 | 6 bytes | Hex           | 用戶ID字段標識 |
| +6              | 2 bytes | Hex           | 用戶ID類型     |
| +2              | 4 bytes | Little Endian | 用戶ID長度     |
| +4              | 可變    | UTF-8         | 用戶ID內容     |

### 9. Color1 字段
| 偏移            | 長度    | 類型 | 描述      |
| --------------- | ------- | ---- | --------- |
| user_id_end + 6 | 7 bytes | Hex  | 顏色1數據 |

### 10. Color2 字段
| 偏移           | 長度    | 類型 | 描述      |
| -------------- | ------- | ---- | --------- |
| color1_end + 6 | 7 bytes | Hex  | 顏色2數據 |

## 數據類型說明

- **Little Endian**: 小端序整數，低位字節在前
- **UTF-8**: Unicode文本編碼
- **Hex**: 十六進制原始數據
- **ASCII**: ASCII編碼文本

## 字段間隔

多數字段之間存在固定的間隔（通常為5-7個字節），這些間隔可能包含分隔符或其他控制信息。

## 使用示例

```python
# 解析封包
parsed_data = hex_parse(hex_string)
print(f"頻道: {parsed_data.channel.value}")
print(f"文本: {parsed_data.text.value}")
print(f"暱稱: {parsed_data.nickname.value}")
```