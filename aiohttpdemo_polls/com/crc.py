def crc16(data: bytes):
    """
    CRC-16-ModBus Algorithm
    """
    data = bytearray(data)
    poly = 0xA001
    crc = 0xFFFF
    for b in data:
        crc ^= (0xFF & b)
        for _ in range(0, 8):
            if crc & 0x0001:
                crc = ((crc >> 1) & 0xFFFF) ^ poly
            else:
                crc = ((crc >> 1) & 0xFFFF)
    crc = crc.to_bytes(2, byteorder='little')
    return crc
