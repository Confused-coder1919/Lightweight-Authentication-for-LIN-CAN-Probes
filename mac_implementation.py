# mac_implementation.py
import hashlib
import struct
from typing import Optional


class LightweightMAC:
    """SHA-256 truncation-based 15-bit MAC (HOTP-style truncation)"""
    def __init__(self, secret_key: bytes, probe_id: Optional[int] = None):
        self.secret_key = secret_key
        self.probe_id = probe_id

    def compute_mac(self, data: bytes, nonce: int, sequence: int) -> int:
        # include probe_id to bind identity into tag (2 bytes)
        probe_bytes = struct.pack(">H", self.probe_id if self.probe_id is not None else 0)
        message = self.secret_key + probe_bytes + data + struct.pack(">HH", nonce & 0xFFFF, sequence & 0xFFFF)
        h = hashlib.sha256(message).digest()
        offset = h[-1] & 0x0F
        mac_bytes = h[offset:offset+2]
        mac = int.from_bytes(mac_bytes, 'big') & 0x7FFF
        return mac

    def verify_mac(self, data: bytes, nonce: int, sequence: int, received_mac: int) -> bool:
        computed = self.compute_mac(data, nonce, sequence)
        return computed == received_mac


class SimpleMAC:
    """Ultra-lightweight polynomial rolling MAC (for very constrained MCUs)."""
    def __init__(self, secret_key: bytes, probe_id: Optional[int] = None):
        self.secret_key = secret_key
        self.probe_id = probe_id

    def compute_simple_mac(self, data: bytes, nonce: int, sequence: int) -> int:
        prime = 31
        mod = 32768  # 15-bit
        probe_bytes = (self.probe_id or 0).to_bytes(2, 'big')
        combined = self.secret_key + probe_bytes + data + struct.pack(">HH", nonce & 0xFFFF, sequence & 0xFFFF)
        h = 0
        for b in combined:
            h = (h * prime + b) % mod
        return h
