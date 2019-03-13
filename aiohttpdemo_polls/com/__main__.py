import com.com as com
import com.decoder as dec


def get_frame(adr):
    out = com.com_session(adr)           # 0.06 seconds
    data = dec.decode(out)
    return data
