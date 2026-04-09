#!/usr/bin/env python3
"""Check ROM mapping for Chrono Trigger"""

with open('rom/Chrono Trigger (USA).sfc', 'rb') as f:
    # Read entire ROM
    rom = f.read()

print(f"ROM size: 0x{len(rom):06X} ({len(rom)//1024//1024}MB)")

# The map mode 0x31 at 0xFFD5 indicates this is likely ExHiROM or ExLoROM
# Let me try different address translation approaches

def try_lorom(bank, addr):
    """Standard LoROM"""
    return ((bank & 0x7F) * 0x8000) + (addr & 0x7FFF)

def try_hirom(bank, addr):
    """Standard HiROM"""
    return ((bank & 0x7F) * 0x10000) + (addr & 0xFFFF)

def try_exlorom(bank, addr):
    """Extended LoROM"""
    bank_adj = bank & 0x7F
    if bank_adj >= 0x40:
        return (bank_adj * 0x8000) + (addr & 0x7FFF) + 0x400000
    return (bank_adj * 0x8000) + (addr & 0x7FFF)

def try_exhirom(bank, addr):
    """Extended HiROM"""
    bank_adj = bank & 0x7F
    if bank_adj >= 0x40:
        return ((bank_adj - 0x40) * 0x10000) + (addr & 0xFFFF) + 0x400000
    return (bank_adj * 0x10000) + (addr & 0xFFFF)

# Test with C2:8006 (known hub)
test_bank = 0xC2
test_addr = 0x8006

print(f"\nTest address: C2:{test_addr:04X}")
print(f"  LoROM:     0x{try_lorom(test_bank, test_addr):06X}")
print(f"  HiROM:     0x{try_hirom(test_bank, test_addr):06X}")
print(f"  ExLoROM:   0x{try_exlorom(test_bank, test_addr):06X}")
print(f"  ExHiROM:   0x{try_exhirom(test_bank, test_addr):06X}")

# The ExHiROM result 0x020006 looks reasonable - let me check data there
offset = try_exhirom(test_bank, test_addr)
print(f"\nData at ExHiROM offset 0x{offset:06X}:")
print(f"  Bytes: {' '.join(f'{b:02X}' for b in rom[offset:offset+16])}")

# Let me also check C2:8CAB
offset2 = try_exhirom(0xC2, 0x8CAB)
print(f"\nC2:8CAB at ExHiROM offset 0x{offset2:06X}:")
print(f"  Bytes: {' '.join(f'{b:02X}' for b in rom[offset2:offset2+16])}")

# And C2:8C00
offset3 = try_exhirom(0xC2, 0x8C00)
print(f"\nC2:8C00 at ExHiROM offset 0x{offset3:06X}:")
print(f"  Bytes: {' '.join(f'{b:02X}' for b in rom[offset3:offset3+16])}")

# Verify by looking at code structure - a function should start with a prologue
# and have reasonable code patterns
print("\n--- Verifying ExHiROM mapping ---")
print(f"C2:8006 first 32 bytes: {' '.join(f'{b:02X}' for b in rom[offset:offset+32])}")

# Common prologue check
prologues = {0x08: 'PHP', 0x48: 'PHA', 0x5A: 'PHY', 0xDA: 'PHX', 0xC2: 'REP', 0xE2: 'SEP', 0x20: 'JSR', 0x22: 'JSL'}
first_byte = rom[offset]
if first_byte in prologues:
    print(f"  First byte 0x{first_byte:02X} = {prologues[first_byte]} (valid prologue!)")
else:
    print(f"  First byte 0x{first_byte:02X} = ???")
