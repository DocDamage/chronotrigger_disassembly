#!/usr/bin/env python3
"""Verify ROM addressing for C2:8C00"""

def snes_to_file_addr(bank, addr):
    """Convert SNES LoROM address to file offset"""
    return (bank * 0x8000) + (addr & 0x7FFF) + 0x200

# Check C2:8C00
bank = 0xC2
addr = 0x8C00
offset = snes_to_file_addr(bank, addr)

print(f"C2:{addr:04X} -> File offset: 0x{offset:06X}")

with open('rom/Chrono Trigger (USA).sfc', 'rb') as f:
    f.seek(offset)
    data = f.read(64)
    print(f"First 64 bytes at C2:8C00: {' '.join(f'{b:02X}' for b in data)}")

# Check some known location - C2:8006 (hub entry)
offset2 = snes_to_file_addr(0xC2, 0x8006)
print(f"\nC2:8006 -> File offset: 0x{offset2:06X}")

with open('rom/Chrono Trigger (USA).sfc', 'rb') as f:
    f.seek(offset2)
    data = f.read(16)
    print(f"First 16 bytes at C2:8006: {' '.join(f'{b:02X}' for b in data)}")

# Let's also check around C2:8CAB (known score-9 hub)
offset3 = snes_to_file_addr(0xC2, 0x8CAB)
print(f"\nC2:8CAB -> File offset: 0x{offset3:06X}")

with open('rom/Chrono Trigger (USA).sfc', 'rb') as f:
    f.seek(offset3)
    data = f.read(32)
    print(f"First 32 bytes at C2:8CAB: {' '.join(f'{b:02X}' for b in data)}")
    
# Check file size
import os
size = os.path.getsize('rom/Chrono Trigger (USA).sfc')
print(f"\nROM file size: 0x{size:06X} ({size} bytes)")
