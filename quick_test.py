# quick_test.py
import random
from virtual_can import VirtualCANNetwork
from typing import Any, Dict, List, Tuple

def quick_demo(return_json: bool = False, seed: int | None = None) -> Dict[str, Any] | None:
    if seed is not None:
        random.seed(seed)

    net = VirtualCANNetwork()
    probes: List[Tuple[int, bytes]] = [
        (0x100, b"temp_sensor_key_001"),
        (0x101, b"press_sensor_key_002"),
        (0x102, b"speed_sensor_key_003"),
    ]
    for pid, key in probes:
        net.add_probe(pid, key)

    cycles = 5
    cycle_results: List[bool] = []
    for _ in range(cycles):
        cycle_results.append(net.simulate_communication())

    ok = sum(1 for r in cycle_results if r)

    result = {
        "registered_probes": [f"0x{pid:03X}" for pid, _ in probes],
        "cycles": cycles,
        "authenticated_cycles": ok,
        "cycle_results": cycle_results,
        "frames_received": [{
            "probe": f"0x{f.id:03X}",
            "seq": f.sequence,
            "mac_hex": f"0x{f.mac:04X}"
        } for f in net.ecu.received_frames]
    }

    if return_json:
        return result

    # CLI friendly print
    print("🚗 Automotive MAC Protocol Demo\n")
    for pid, _ in probes:
        print(f"✅ Registered probe 0x{pid:03X}")
    print("\n🔒 Testing Secure Communication...")
    for i, passed in enumerate(cycle_results, start=1):
        print(f"  Cycle {i}: {'✅ Authenticated' if passed else '❌ Failed'}")
    print(f"\n📊 Results: {ok}/{cycles} successful authentications")
    if net.ecu.received_frames:
        print(f"\n📨 Received {len(net.ecu.received_frames)} authenticated frames")
        for f in net.ecu.received_frames[:5]:
            print(f"  Probe 0x{f.id:03X}: Seq {f.sequence}, MAC 0x{f.mac:04X}")

if __name__ == "__main__":
    quick_demo()
