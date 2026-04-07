from snes_utils_hirom_v2 import hirom_to_file_offset

rom_path = '../../rom/Chrono Trigger (USA).sfc'

candidates = [
    (0xDBA5, '12 callers (weak) - DB00 region'),
    (0xDD20, '6 callers (weak) - DD00 region'),
    (0xDDAD, '4 callers (weak) - DD00 region'),
    (0xDDA5, '3 callers (weak) - DD00 region'),
    (0xDFA5, '5 callers (weak) - DF00 region'),
]

for addr, name in candidates:
    print(f'=== C0:{addr:04X} - {name} ===')
    offset = hirom_to_file_offset(0xC0, addr)
    with open(rom_path, 'rb') as f:
        f.seek(offset)
        data = f.read(256)
        print(f'  First 12 bytes: {" ".join(f"{b:02X}" for b in data[:12])}')
        returns = [i for i, b in enumerate(data) if b == 0x60]
        if returns:
            print(f'  RTS at +{returns[:3]}')
            print(f'  Provisional end: C0:{addr + returns[0]:04X}')
        else:
            print('  No RTS in first 256 bytes')
    print()
