# device_manager.py
import time

try:
    from app.X2OOptics.voa import Voa
except ImportError:
    from mock_voa import Voa

try:
    from app.X2OOptics.optical_switch import Switch
except ImportError:
    from mock_switch import Switch

from app.X2OOptics.opm import OPM
from app.X2OOptics.shelf_manager import ShelfManager

class DeviceManager:
    """
    Manager object which bundles the VOA, switches, and OPM
    """
    def __init__(self,
                 voa_path: str = "/dev/serial/by-id/usb-FTDI_FT230X_Basic_UART_DP04LVOF-if00-port0",
                 switch1_path: str = "/dev/serial/by-id/usb-Silicon_Labs_CP2102N_USB_to_UART_Bridge_Controller_122a29b726c6ef11acb06d527a5e3baa-if00-port0",
                 switch2_path: str = "/dev/serial/by-id/usb-Silicon_Labs_CP2102N_USB_to_UART_Bridge_Controller_56c3d12f28c6ef11bec16f527a5e3baa-if00-port0",
                 opm_id: str = "USB0::0x1313::0x8076::M01217675::0::INSTR") -> None:
        self.voa = None
        self.switch1 = None
        self.switch2 = None
        self.opm = None
        
        self.shelf_manager = None

        #Set device paths
        self.voa_path = voa_path
        self.switch1_path = switch1_path
        self.switch2_path = switch2_path
        
        self.connect_voa(self.voa_path)
        self.connect_optical_switches(
            self.switch1_path,
            self.switch2_path,
            num_channels=64
        )
        self.connect_opm(
            device_id=opm_id
        )

    # -------------------------------------------------
    # VOA
    # -------------------------------------------------
    def connect_voa(self, device_path: str) -> None:
        try:
            print(f"Connecting VOA at {device_path}")
            self.voa = Voa(device_path)
            print("VOA connected")
        except Exception as e:
            print(f"VOA connection failed: {e}")
            self.voa = None

    def set_voa_attenuation(self, attenuation_db: float) -> None:
        if self.voa is None:
            raise RuntimeError("VOA not connected")
        self.voa.attenuate(attenuation_db)

    def get_voa_attenuation(self) -> float:
        if self.voa is None:
            raise RuntimeError("VOA not connected")
        return self.voa.get_attenuation()

    # -------------------------------------------------
    # SWITCHES
    # -------------------------------------------------

    def connect_optical_switches(self, dev1: str, dev2: str, num_channels: int) -> None:
        try:
            print(f"Connecting Switch A at {dev1}")
            self.switch1 = Switch(dev1, num_channels)
            print("Switch A connected")
        except Exception as e:
            print(f"Switch A failed: {e}")
            self.switch1 = None

        try:
            print(f"Connecting Switch B at {dev2}")
            self.switch2 = Switch(dev2, num_channels)
            print("Switch B connected")
        except Exception as e:
            print(f"Switch B failed: {e}")
            self.switch2 = None

    def reconnect_switch1(self) -> None:
        try:
            print("Reconnecting Switch A...")
            if self.switch1:
                self.switch1.ser.close()
        except:
            pass
        
        '''why are we sleeping?
        
        - Payton 05/23/2026'''
        time.sleep(1)

        self.switch1 = Switch(self.switch1_path, 64)

    def reconnect_switch2(self) -> None:
        try:
            print("Reconnecting Switch B...")
            if self.switch2:
                self.switch2.ser.close()
        except:
            pass

        time.sleep(1)

        self.switch2 = Switch(self.switch2_path, 64)

    def set_switch1_channel(self, channel: int) -> None:
        for attempt in range(3):
            try:
                self.switch1.select_chan(channel)
                return
            except Exception as e:
                print(f"Switch A error attempt {attempt+1}: {e}")
                self.reconnect_switch1()
        raise RuntimeError(f"Switch A failed on channel {channel}")

    def set_switch2_channel(self, channel: int) -> None:
        for attempt in range(3):
            try:
                self.switch2.select_chan(channel)
                return
            except Exception as e:
                print(f"Switch B error attempt {attempt+1}: {e}")
                self.reconnect_switch2()
        raise RuntimeError(f"Switch B failed on channel {channel}")

    def get_switch1_channel(self) -> None:
        if self.switch1 is None:
            raise RuntimeError("Optical switch A not connected")
        return self.switch1.current_chan
    
    def get_switch2_channel(self) -> None:
        if self.switch2 is None:
            raise RuntimeError("Optical switch B not connected")
        return self.switch2.current_chan

    # -------------------------------------------------
    # OPM
    # -------------------------------------------------

    def connect_opm(self, device_id: str, avg_count: int = 10) -> None:
        try:
            self.opm = OPM(device_id, avg_count)
            print("OPM Connected")
        except Exception as e:
            print(f"OPM failed: {e}")
            self.opm = None

    def read_optical_power(self) -> float:
        if self.opm is None:
            raise RuntimeError("OPM not connected")
        return self.opm.read_power_dbm()

    # =========================================================
    # SHELF MANAGER
    # =========================================================

    def connect_shelf_manager(self, host: str, username: str = "root", password: str = "") -> tuple[bool,str]:
        try:
            self.shelf_manager = ShelfManager(
                host=host,
                username=username,
                password=password
            )
            return self.shelf_manager.connect()

        except Exception as e:
            return False, str(e)

    def disconnect_shelf_manager(self) -> None:
        if self.shelf_manager:
            self.shelf_manager.disconnect()

    def set_shelf_fans(self, level: int) -> tuple[bool, str]:
        if self.shelf_manager is None:
            return False, "Shelf manager not connected"

        return self.shelf_manager.set_all_fans(level)

    def get_shelf_fans(self) -> tuple[bool,str]:
        if self.shelf_manager is None:
            return False, "Shelf manager not connected"

        return self.shelf_manager.fans()

    def set_min_fan_level(self, level: int) -> tuple[bool,str]:
        if self.shelf_manager is None:
            return False, "Shelf manager not connected"

        return self.shelf_manager.set_min_fan_level(level)

# -------------------------------------------------
    # CLEANUP
    # -------------------------------------------------

    def close_all(self) -> None:
        """
        Closes VOA, switch 1, switch 2, and OPM
        """
        try:
            if self.voa:
                self.voa.close()
        except:
            pass
        try:
            if self.switch1:
                self.switch1.ser.close()
        except:
            pass
        try:
            if self.switch2:
                self.switch2.ser.close()
        except:
            pass
        try:
            if self.opm:
                self.opm.close()
        except:
            pass
