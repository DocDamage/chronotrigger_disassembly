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
    (0x305D, "C0:305D - 5 callers, score 6"),
    (0x5614, "C0:5614 - 13 callers, score 6"),
    (0x568B, "C0:568B - 7 callers, score 6"),
    (0x54BD, "C0:54BD - 4 callers, score 6"),
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
