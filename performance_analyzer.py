# performance_analyzer.py
import time
from typing import Dict
from virtual_can import VirtualCANNetwork

class PerformanceAnalyzer:
    def __init__(self):
        self.metrics: Dict = {}

    def run_latency_test(self, network: VirtualCANNetwork, samples: int = 200) -> Dict:
        latencies = []
        for _ in range(samples):
            start = time.perf_counter()
            nonce = network.ecu.generate_nonce()
            frame = network.probes[0].generate_frame(b"benchmark", nonce)
            network.ecu.verify_frame(frame)
            end = time.perf_counter()
            latencies.append((end - start) * 1000.0)
        avg = sum(latencies) / len(latencies)
        p95 = sorted(latencies)[int(0.95 * len(latencies))]
        self.metrics['latency'] = {'avg_ms': avg, 'p95_ms': p95, 'samples': samples}
        return self.metrics['latency']

    def run_throughput_test(self, network: VirtualCANNetwork, duration_s: int = 3) -> Dict:
        start = time.perf_counter()
        messages = 0
        cycles = 0
        while time.perf_counter() - start < duration_s:
            cycles += 1
            nonce = network.ecu.generate_nonce()
            for probe in network.probes:
                # process multiple quick messages
                for _ in range(10):
                    frame = probe.generate_frame(b"t", nonce)
                    if network.ecu.verify_frame(frame):
                        messages += 1
        elapsed = time.perf_counter() - start
        rate = messages / elapsed if elapsed > 0 else 0
        self.metrics['throughput'] = {'messages': messages, 'duration': elapsed, 'msg_per_sec': rate, 'cycles': cycles}
        return self.metrics['throughput']

    def run_memory_estimate(self, network: VirtualCANNetwork) -> Dict:
        probe_memory = len(network.probes) * 100
        ecu_memory = len(network.ecu.probe_keys) * 50
        frame_memory = len(network.ecu.received_frames) * 30
        total = probe_memory + ecu_memory + frame_memory
        self.metrics['memory'] = {'total_bytes': total, 'probe_bytes': probe_memory, 'ecu_bytes': ecu_memory, 'frame_bytes': frame_memory}
        return self.metrics['memory']

def run_perf(duration_s: int = 3, probe_count: int = 3) -> Dict:
    net = VirtualCANNetwork()
    for i in range(probe_count):
        net.add_probe(0x100 + i, f"perf_key_{i}".encode())
    pa = PerformanceAnalyzer()
    lat = pa.run_latency_test(net, samples=200)
    thr = pa.run_throughput_test(net, duration_s)
    mem = pa.run_memory_estimate(net)
    return {'latency': lat, 'throughput': thr, 'memory': mem}

if __name__ == "__main__":
    import json
    print(json.dumps(run_perf(3, 3), indent=2))
