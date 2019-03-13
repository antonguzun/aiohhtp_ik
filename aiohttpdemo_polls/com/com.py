import com.crc as crc
import serial
import time

BAUD_RATE = 115200
COM_PORT = 'COM8'


def form_req(adr: int):
    """Form request frame kind: 0xXX(address),0x00,0x00,0xXX(CRC low),0xXX(CRC high)
    :param adr: int
    :return: array length 5 bytes
    """
    adr_byte = adr.to_bytes(1, byteorder='big')
    req_val = adr_byte + b'\x00' + b'\x00'
    req_val = req_val + crc.crc16(req_val)
    return req_val


def com_session(adr: int):
    """Make session with ine device
    TODO! EXCEPTION if answer of device is less than 24 bytes
    :param adr: int address of device
    :return: if CRC is ok: response from device - array of 24 bytes
            else: string 'ERROR CRC'
    """
    time.sleep(0.05)                # without this delay don't work
    ser = serial.Serial()
    ser.baudrate = BAUD_RATE
    ser.port = COM_PORT

    ser.open()

    while not ser.writable():
        pass
    ser.write(form_req(adr))

    while not ser.in_waiting:
        pass
    s = ser.read(ser.in_waiting)

    crc_cal = crc.crc16(s[0:22])
    crc_real = s[len(s)-2:len(s)]
    if crc_real == crc_cal:
        ser.close()
        return s
    else:
        ser.close()
        return 'ERROR CRC'
