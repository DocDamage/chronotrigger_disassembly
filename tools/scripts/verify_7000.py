from snes_utils_hirom_v2 import hirom_to_file_offset
import os, json

rom_path = '../../rom/Chrono Trigger (USA).sfc'
manifests_dir = '../../passes/manifests'

def check_overlap(c_start, c_end):
    for fname in os.listdir(manifests_dir):
        if fname.endswith('.json') and fname.startswith('pass'):
            with open(os.path.join(manifests_dir, fname), 'r') as f:
                try:
                    data = json.load(f)
                    for r in data.get('closed_ranges', []):
                        range_str = r.get('range', '')
                        if range_str.startswith('C0:'):
                            parts = range_str.split('..')
                            if len(parts) == 2:
                                start = int(parts[0].split(':')[1], 16)
                                end = int(parts[1].split(':')[1], 16)
                                if c_start < end and c_end > start:
                                    return (fname, range_str)
                except:
                    pass
    return None

targets = [
    (0x75E9, "C0:75E9 - 6 callers"),
    (0x79CF, "C0:79CF - 10 callers"),
    (0x7D66, "C0:7D66 - 7 callers"),
    (0x7F62, "C0:7F62 - 7 callers"),
]

ready = []
for addr, desc in targets:
    print(f'=== {desc} ===')
    offset = hirom_to_file_offset(0xC0, addr)
    with open(rom_path, 'rb') as f:
        f.seek(offset)
        data = f.read(128)
        print(f'  First 12 bytes: {" ".join(f"{b:02X}" for b in data[:12])}')
        returns = [i for i, b in enumerate(data) if b == 0x60]
        print(f'  RTS at: +{returns[:3]}')
        if returns:
            end = addr + returns[0]
            print(f'  Range: C0:{addr:04X}..C0:{end:04X}')
            overlap = check_overlap(addr, end)
            if overlap:
                print(f'  OVERLAP: {overlap}')
            else:
                print(f'  CLEAR - ready for promotion')
                ready.append((addr, end, desc))
        else:
            print('  No RTS found')
    print()

print("="*60)
print("READY FOR PROMOTION:")
for start, end, desc in ready:
    print(f'  C0:{start:04X}..C0:{end:04X}: {desc}')
