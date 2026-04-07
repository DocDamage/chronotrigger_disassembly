from snes_utils_hirom_v2 import hirom_to_file_offset
import os
import json

rom_path = "../../rom/Chrono Trigger (USA).sfc"
manifests_dir = "../../passes/manifests"

def check_existing_coverage(addr):
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
                                if start <= addr <= end:
                                    return (fname, range_str)
                except:
                    pass
    return None

def verify_function(start_addr, name):
    print(f"\n=== C0:{start_addr:04X} - {name} ===")
    
    existing = check_existing_coverage(start_addr)
    if existing:
        print(f"  ALREADY COVERED by {existing[0]}: {existing[1]}")
        return None
    
    offset = hirom_to_file_offset(0xC0, start_addr)
    with open(rom_path, "rb") as f:
        f.seek(offset)
        data = f.read(256)
        
        print(f"  First 16 bytes: {' '.join(f'{b:02X}' for b in data[:16])}")
        
        returns = [i for i, b in enumerate(data) if b == 0x60]
        if returns:
            print(f"  RTS at offsets: +{returns[:5]}")
            first_rts = start_addr + returns[0]
            print(f"  Provisional end: C0:{first_rts:04X}")
            return first_rts
        else:
            print("  No RTS in first 256 bytes")
            return None

# Verify major function candidates from C0:9000-A000 and C0:C000-D000
print("Verifying high-value targets from C0:9000-A000 and C0:C000-D000...")
candidates = [
    (0xC27F, "65 callers (weak) - C200 region MAJOR"),
    (0xC87F, "46 callers (weak) - C800 region MAJOR"),
    (0xC260, "20 callers (weak) - C200 region"),
    (0xC09D, "13 callers (weak) - C000 region"),
    (0xC8C8, "9 callers (weak) - C800 region"),
    (0xC6E7, "6 callers (weak) - C600 region"),
    (0xC7A6, "5 callers (weak) - C700 region"),
    (0x97A6, "7 callers (weak) - 9700 region"),
    (0x997F, "8 callers (weak) - 9900 region"),
]

ready = []
for addr, name in candidates:
    end = verify_function(addr, name)
    if end:
        ready.append((addr, end, name))

print("\n" + "="*60)
print("READY FOR PROMOTION:")
for start, end, name in ready:
    print(f"  C0:{start:04X}..C0:{end:04X}: {name}")
