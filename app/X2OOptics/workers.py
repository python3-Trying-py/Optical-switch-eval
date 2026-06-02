import time

from PyQt6.QtCore import (
    Qt,
    QObject,
    QThread,
    pyqtSignal,
)

from device_manager import DeviceManager

# =========================================================
# Custom Typing
# =========================================================

type NestedScanResult = list[tuple[int,int,float]]
type ReproducibilityResults = list[tuple[int,int,int,float]]


# =========================================================
# STABLE CHANNELS
# =========================================================

STABLE_CHANNELS = [
    (1, 1), (2, 2), (3, 3), (4, 4),
    (6, 5), (7, 6), (8, 7), (9, 8),
    (12, 11), (13, 12), (14, 13),
    (15, 14), (16, 15), (17, 16),
    (18, 17), (19, 18), (20, 19),
    (21, 20), (23, 22), (24, 23),
    (25, 24), (28, 27), (29, 28),
    (30, 29), (31, 30), (33, 32),
    (34, 33), (35, 34), (36, 35),
    (37, 36), (39, 38), (40, 39),
]


# =========================================================
# NESTED SCAN WORKER
# =========================================================

class NestedScanWorker(QObject):
    """
    Double iterative channel scanner object
    """

    '''Something to note: these signals will share across all instances,
    so if you wanted to have multiple NestedScanWorker objects they will likely interfere with
    eachother.

    - Payton 05/21/2026'''
    progress = pyqtSignal(int)
    status = pyqtSignal(str)
    finished = pyqtSignal(list)
    error = pyqtSignal(str)

    def __init__(self, dm: DeviceManager, max_a: int, max_b: int) -> None:
        super().__init__()

        self.dm = dm
        self.max_a = max_a
        self.max_b = max_b
        #allows for preventing or interrupting the scan
        self.running = True

    def stop(self) -> None:
        """
        Prevents worker from running
        """
        self.running = False

    """What this does:
        1. Performs a double iterative loop across all a then b channels
            a. Retrieves the optical power from the device_manager
            b. Stores the information in the results list and emits the current value of counter and information on the channel pairing
        2. Once the loops are done, the method emits the results list
        """
    def run(self) -> None:
        """
        Iterates through all channel pairs and emits optical data results
        """
        results = []

        counter = 0

        try:
            for ch_a in range(1, self.max_a + 1):
                if not self.running:
                    break
                self.dm.set_switch1_channel(ch_a)

                for ch_b in range(1, self.max_b + 1):
                    if not self.running:
                        break

                    self.dm.set_switch2_channel(ch_b)

                    power = self.dm.read_optical_power()

                    results.append(
                        [ch_a, ch_b, power]
                    )

                    counter += 1

                    self.progress.emit(counter)

                    self.status.emit(
                        f"A={ch_a}  "
                        f"B={ch_b}  "
                        f"Power={power:.2f} dBm"
                    )

        except Exception as e:
            self.error.emit(str(e))

        self.finished.emit(results)


# =========================================================
# REPRODUCIBILITY WORKER
# =========================================================

class ReproducibilityWorker(QObject):
    """
    Double iterative simulation object
    """

    '''Something to note: these signals will share across all instances,
    so if you wanted to have multiple ReproducibilityWorker objects they will likely interfere
    with eachother
    - Payton 05/21/2026'''
    progress = pyqtSignal(int)
    status = pyqtSignal(str)
    finished = pyqtSignal(list)
    error = pyqtSignal(str)

    def __init__(self, dm: DeviceManager, iterations: int) -> None:
        super().__init__()

        self.dm = dm
        self.iterations = iterations
        #allows for preventing or interrupting the scan
        self.running = True

    def stop(self) -> None:
        """
        Prevents worker from running
        """
        self.running = False

    """What this does:
        1. iterates through the stable channels then iterates through each satble channel pair some number of times
            a. Retrieves the optical power from the device_manager
            b. Stores the information, along with the iteration, in the results list and emits the current value of counter and information on the current iteration
        2. Once the loops are done, the method emits the results list
        """
    def run(self) -> None:
        """
        Iterates through all stable channels and emits optical data results
        """
        results = []
        counter = 0

        try:
            for a, b in STABLE_CHANNELS:
                if not self.running:
                    break

                for i in range(self.iterations):
                    if not self.running:
                        break

                    self.dm.set_switch1_channel(a)

                    self.dm.set_switch2_channel(b)

                    #Sleep to allow switch to change channels
                    time.sleep(2)

                    power = self.dm.read_optical_power()
                    results.append([
                        a,
                        b,
                        i,
                        power,
                    ])

                    counter += 1

                    self.progress.emit(counter)

                    self.status.emit(
                        f"A={a}  "
                        f"B={b}  "
                        f"Iter={i}  "
                        f"Power={power:.2f} dBm"
                    )

        except Exception as e:
            self.error.emit(str(e))

        self.finished.emit(results)