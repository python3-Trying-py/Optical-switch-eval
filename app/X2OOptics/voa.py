import serial
import sys
import time

class Voa:
    VERBOSE = True
    dev = None
    ser = None

    def __init__(self, dev_path) -> None:
        self.ser = serial.Serial(port=dev_path, baudrate=115200, bytesize=8, parity="N", stopbits=1, timeout=1)
        
        #slow down for hardware
        time.sleep(1)
        if self.VERBOSE:
            print("VOA: connecting..")
        identity = self.get_id()
        att = self.get_attenuation()
        if self.VERBOSE:
            print("VOA ID: %s" % identity)
            print("VOA current attenuation: %.2f" % att)
        
    def get_id(self):
        """
        Retrieves VOA id
        """
        self.ser.write(b'ID?\n')
        identity = self.ser.read_until(expected=b"\n")
        if not identity:
            return "NO RESPONSE"
        return identity.decode("utf-8").strip()
        # if VERBOSE:
        #     print("VOA ID: %s" % identity)
        #return identity

    def get_attenuation(self) -> float:
        """
        Retrieves current attenuation
        """
        for _ in range(3):
            self.ser.write(b"A1 A?\n")
            resp = self.ser.read_until(expected=b"\n")
        
            if resp:
                resp = resp.decode("utf-8").strip()
                if "ERR" not in resp:
                    return float(resp)
                
            #slow down for hardware
            time.sleep(0.2)
        raise Exception("VOA did not respond")
        #resp = None

        #while resp is None or "ERR" in resp:
        #    self.ser.write(b"A1 A?\n")
        #    resp = self.ser.read_until(expected=b"\n")
        #    resp = resp.decode("utf-8")

        #att = float(resp)
        #return att

    def attenuate(self, attenuation_db: float) -> None:
        """
        Sets attenuation
        """
        att_str = "%.2f" % attenuation_db
        print("VOA: setting attenuation to %sdB" % att_str)

        for _ in range(5):  # retry up to 5 times
            self.ser.write(('A1 A %s\n' % att_str).encode("utf-8"))
            resp = self.ser.read_until(expected=b"\n")

            if resp:
                resp = resp.decode("utf-8").strip()
                if resp == "OK":
                    print("VOA: attenuation setting done")
                    return

            print("VOA: attenuator busy.. retrying..")

        raise Exception("VOA failed to set attenuation")

    def close(self) -> None:
        """
        Closes VOA
        """
        self.ser.close()

if __name__ == "__main__":
    voa = Voa("/dev/serial/by-id/usb-FTDI_FT230X_Basic_UART_DP04LVOF-if00-port0")

    if len(sys.argv) > 1:
        att = float(sys.argv[1])
        voa.attenuate(att)

    # get_id()
