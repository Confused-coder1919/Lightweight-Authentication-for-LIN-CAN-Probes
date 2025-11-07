# virtual_can.py
import time
import random
from dataclasses import dataclass
from typing import List, Dict, Optional

from mac_implementation import LightweightMAC

@dataclass
class CANFrame:
    id: int
    data: bytes
    sequence: int
    mac: int
    timestamp: float

class VirtualProbe:
    def __init__(self, probe_id: int, secret_key: bytes):
        self.probe_id = probe_id
        self.secret_key = secret_key
        self.mac_calculator = LightweightMAC(secret_key, probe_id)
        self.sequence_counter = random.randint(0, 1000)

    def generate_frame(self, sensor_data: bytes, nonce: int) -> CANFrame:
        self.sequence_counter += 1
        mac = self.mac_calculator.compute_mac(sensor_data, nonce, self.sequence_counter)
        return CANFrame(
            id=self.probe_id,
            data=sensor_data,
            sequence=self.sequence_counter,
            mac=mac,
            timestamp=time.time()
        )

class VirtualECU:
    def __init__(self):
        self.probe_keys: Dict[int, bytes] = {}
        self.current_nonce: int = 0
        self.received_frames: List[CANFrame] = []
        self.security_log: List[str] = []

    def register_probe(self, probe_id: int, secret_key: bytes):
        self.probe_keys[probe_id] = secret_key

    def generate_nonce(self) -> int:
        # 16-bit nonce
        self.current_nonce = random.randint(0, 65535)
        return self.current_nonce

    def verify_frame(self, frame: CANFrame) -> bool:
        if frame.id not in self.probe_keys:
            self.security_log.append(f"UNKNOWN_PROBE: ID {frame.id:03X}")
            return False

        secret_key = self.probe_keys[frame.id]
        mac_calc = LightweightMAC(secret_key, frame.id)

        if not mac_calc.verify_mac(frame.data, self.current_nonce, frame.sequence, frame.mac):
            self.security_log.append(f"INVALID_MAC: Probe {frame.id:03X}")
            return False

        if not self._check_sequence(frame):
            self.security_log.append(f"REPLAY_ATTACK: Probe {frame.id:03X}, Seq {frame.sequence}")
            return False

        self.received_frames.append(frame)
        return True

    def _check_sequence(self, frame: CANFrame) -> bool:
        previous = [f for f in self.received_frames if f.id == frame.id]
        if previous:
            return frame.sequence > max(f.sequence for f in previous)
        return True

class VirtualCANNetwork:
    def __init__(self):
        self.ecu = VirtualECU()
        self.probes: List[VirtualProbe] = []

    def add_probe(self, probe_id: int, secret_key: bytes) -> VirtualProbe:
        probe = VirtualProbe(probe_id, secret_key)
        self.probes.append(probe)
        self.ecu.register_probe(probe_id, secret_key)
        return probe

    def simulate_communication(self) -> bool:
        """Simulate one authentication cycle across all probes (one nonce)."""
        nonce = self.ecu.generate_nonce()
        for p in self.probes:
            data = f"data_{p.probe_id}_{time.time()}".encode()
            frame = p.generate_frame(data, nonce)
            if not self.ecu.verify_frame(frame):
                # if one probe fails, treat cycle as failed
                return False
        return True
