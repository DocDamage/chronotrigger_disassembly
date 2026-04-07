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

# Verify major function candidates
print("Verifying high-value targets from C0:A000-B000 and C0:E000-F000...")
candidates = [
    (0xA67F, "32 callers (weak) - A600 region"),
    (0xA98A, "16 callers (weak) - A900 region"),
    (0xEC60, "28 callers (weak) - NMI/EC00 region"),
    (0xE87F, "24 callers (weak) - E800 region"),
    (0xA27F, "15 callers (weak) - A200 region"),
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
