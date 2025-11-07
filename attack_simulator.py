# attack_simulator.py
import time
import random
from typing import Dict
from virtual_can import VirtualCANNetwork, CANFrame

class AttackSimulator:
    def __init__(self, network: VirtualCANNetwork):
        self.network = network

    def replay_attack(self) -> bool:
        if not self.network.probes:
            return False
        nonce = self.network.ecu.generate_nonce()
        legitimate = self.network.probes[0].generate_frame(b"legitimate_data", nonce)
        self.network.ecu.verify_frame(legitimate)  # accepted first
        # replay the exact same frame (same seq & mac)
        replayed = CANFrame(
            id=legitimate.id,
            data=legitimate.data,
            sequence=legitimate.sequence,
            mac=legitimate.mac,
            timestamp=time.time()
        )
        ok = self.network.ecu.verify_frame(replayed)
        return not ok  # True if replay was blocked

    def spoofing_attack(self) -> bool:
        if not self.network.probes:
            return False
        target_id = self.network.probes[0].probe_id
        spoof = CANFrame(
            id=target_id,
            data=b"malicious",
            sequence=9999,
            mac=random.randint(0, 0x7FFF),
            timestamp=time.time()
        )
        ok = self.network.ecu.verify_frame(spoof)
        return not ok  # True if spoof was blocked

    def unknown_probe_attack(self) -> bool:
        unknown = CANFrame(id=0x999, data=b"attack", sequence=1, mac=12345, timestamp=time.time())
        ok = self.network.ecu.verify_frame(unknown)
        return not ok

def run_attacks(replay: bool = True, spoof: bool = True, attack_rate: float = 0.2, probes: int = 3) -> Dict:
    net = VirtualCANNetwork()
    for i in range(probes):
        pid = 0x100 + i
        net.add_probe(pid, f"probe_key_{i:03d}".encode())

    sim = AttackSimulator(net)
    out = {"replay_blocked": None, "spoof_blocked": None, "unknown_blocked": None, "logs": []}
    if replay:
        out["replay_blocked"] = sim.replay_attack()
    if spoof:
        out["spoof_blocked"] = sim.spoofing_attack()
    out["unknown_blocked"] = sim.unknown_probe_attack()
    out["logs"] = list(net.ecu.security_log)
    return out

if __name__ == "__main__":
    print(run_attacks())
