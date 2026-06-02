#shelf_manager.py

import paramiko

class ShelfManager:
    """
    Manager object which connects to the board shelf
    """
    def __init__(self, host: str = "192.168.0.2", username: str = "root", password: str = "", port: int = 22) -> None:

        self.host = host
        self.username = username
        self.password = password
        self.port = port

        self.client = None
        self.connected = False

    def connect(self) -> tuple[bool,str]:
        """
        connects the shelf manager to a client with password-only authentication
        """
        try:
            self.client = paramiko.SSHClient()
            self.client.set_missing_host_key_policy(paramiko.AutoAddPolicy())

            self.client.connect(
                hostname=self.host,
                port=self.port,
                username=self.username,
                password=self.password,
                look_for_keys=False,
                allow_agent=False,
                timeout=10,
                disabled_algorithms={"pubkeys": []}
            )

            self.connected = True
            return True, f"Connected to {self.host}"

        except Exception as e:
            self.connected = False
            return False, str(e)

    def disconnect(self) -> None:
        if self.client:
            self.client.close()

        self.connected = False

    def run_clia(self, command: str) -> tuple[bool,str]:
        """
        runs input command within the current client
        """
        if not self.connected:
            return False, "Not connected"

        try:
            full_cmd = f"clia {command}"

            stdin, stdout, stderr = self.client.exec_command(full_cmd)

            out = stdout.read().decode().strip()
            err = stderr.read().decode().strip()

            if err and not out:
                return False, err

            return True, out

        except Exception as e:
            self.connected = False
            return False, str(e)

    def fans(self) -> tuple[bool,str]:
        """
        runs < fans > command
        """
        return self.run_clia("fans")

    def get_min_fan_level(self) -> tuple[bool,str]:
        """
        retrives < minfanlevel >
        """
        return self.run_clia("minfanlevel")

    def set_min_fan_level(self, level: int) -> tuple[bool,str]:
        """
        sets < minfanlevel >
        """
        level = int(level)

        if level < 3:
            return False, "Minimum safe fan level is 3"

        return self.run_clia(f"minfanlevel {level}")

    def set_fan_level(self, fan_addr: str, fru_id: int, level: int) -> tuple[bool, str]:
        """
        runs < setfanlevel > command
        """
        level = int(level)

        if level < 3:
            return False, "Minimum safe fan level is 3"

        return self.run_clia(
            f"setfanlevel {fan_addr} {fru_id} {level}"
        )

    def set_all_fans(self, level: int) -> tuple[bool, str]:
        """
        runs < setfanlevel > command for fans 5c and 5a
        """
        ok1, out1 = self.set_fan_level("5c", 0, level)
        ok2, out2 = self.set_fan_level("5a", 0, level)
        ok3, out3 = self.set_min_fan_level(level)

        output = "\n".join([out1, out2, out3])

        return ok1 and ok2 and ok3, output

    def shelf_status(self) -> tuple[bool,str]:
        """
        runs < shmstatus -v > command
        """
        return self.run_clia("shmstatus -v")

    def power_status(self) -> tuple[bool,str]:
        """
        runs < shelf power_distribution > command
        """
        return self.run_clia("shelf power_distribution")

    def cooling_state(self) -> tuple[bool,str]:
        """
        runs < shelf cooling_state > command
        """
        return self.run_clia("shelf cooling_state")

