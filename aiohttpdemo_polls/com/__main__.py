import time
import com.com as com
import com.decoder as dec
#from firebase import firebase


def get_frames(arr_adr):
    for i in arr_adr:
        out = com.com_session(i)           # 0.06 seconds
        data = dec.decode(out)
        print(data)
        data = 0

def get_frame(adr):
    out = com.com_session(adr)           # 0.06 seconds
    data = dec.decode(out)
    return data


