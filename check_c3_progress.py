import json
import os
import re

# Calculate current C3 coverage from manifests
manifest_dir = 'passes/manifests'
c3_bytes = set()

c3_manifests = []
for f in os.listdir(manifest_dir):
    if f.endswith('.json'):
        filepath = os.path.join(manifest_dir, f)
        try:
            with open(filepath) as fp:
                data = json.load(fp)
                
                # Check closed_ranges
                if 'closed_ranges' in data and isinstance(data['closed_ranges'], list):
                    for cr in data['closed_ranges']:
                        if isinstance(cr, dict) and 'range' in cr:
                            range_str = cr['range']
                            m = re.match(r'C3:([0-9A-F]{4})\.\.C3:([0-9A-F]{4})', range_str, re.I)
                            if m:
                                start = int(m.group(1), 16)
                                end = int(m.group(2), 16)
                                c3_manifests.append((f, start, end))
                                for i in range(start, end + 1):
                                    c3_bytes.add(i)
                
                # Check start/end address
                if 'start_address' in data and 'end_address' in data:
                    m1 = re.match(r'C3:([0-9A-F]{4})', data['start_address'], re.I)
                    m2 = re.match(r'C3:([0-9A-F]{4})', data['end_address'], re.I)
                    if m1 and m2:
                        start = int(m1.group(1), 16)
                        end = int(m2.group(1), 16)
                        c3_manifests.append((f, start, end))
                        for i in range(start, end + 1):
                            c3_bytes.add(i)
        except Exception as e:
            pass

total_c3 = 65536
current = len(c3_bytes)
percent = (current / total_c3) * 100
needed_30 = int(0.30 * total_c3)
gap = needed_30 - current

print(f'=== C3 Coverage Summary ===')
print(f'C3 manifests found: {len(c3_manifests)}')
print(f'Current documented bytes: {current}')
print(f'Current coverage: {percent:.2f}%')
print(f'Target for 30%: {needed_30} bytes')
print(f'Gap to 30%: {gap} bytes')
print()

# Load C3:3700 seam block
try:
    with open('reports/c3_3700_seam_block.json') as f:
        data = json.load(f)
    
    print('=== C3:3700-37FF Seam Block ===')
    print(f"Total code islands: {data.get('total_islands', 0)}")
    print(f"Score-6+ clusters: {data.get('score_6_plus_clusters', 0)}")
    print()
    
    # Show code islands
    islands = data.get('code_islands', [])
    score_6_islands = [i for i in islands if i.get('score', 0) >= 6]
    print(f'Score-6+ islands: {len(score_6_islands)}')
    for i in score_6_islands[:10]:
        start = i.get('start', 0)
        end = i.get('end', 0)
        score = i.get('score', 0)
        width = end - start + 1
        print(f"  C3:{start:04X}..C3:{end:04X} - score {score}, {width} bytes")
except Exception as e:
    print(f'Error loading 3700 seam block: {e}')

print()

# Check C3:3000 seam block
try:
    with open('reports/c3_3000_seam_block.json') as f:
        data = json.load(f)
    
    print('=== C3:3000-30FF Seam Block ===')
    print(f"Total code islands: {data.get('total_islands', 0)}")
    print(f"Score-6+ clusters: {data.get('score_6_plus_clusters', 0)}")
    
    islands = data.get('code_islands', [])
    score_6_islands = [i for i in islands if i.get('score', 0) >= 6]
    print(f'Score-6+ islands: {len(score_6_islands)}')
    for i in score_6_islands[:5]:
        start = i.get('start', 0)
        end = i.get('end', 0)
        score = i.get('score', 0)
        width = end - start + 1
        print(f"  C3:{start:04X}..C3:{end:04X} - score {score}, {width} bytes")
except Exception as e:
    print(f'Error loading 3000 seam block: {e}')

print()

# Check C3:3100 seam block
try:
    with open('reports/c3_3100_seam_block.json') as f:
        data = json.load(f)
    
    print('=== C3:3100-31FF Seam Block ===')
    print(f"Total code islands: {data.get('total_islands', 0)}")
    print(f"Score-6+ clusters: {data.get('score_6_plus_clusters', 0)}")
    
    islands = data.get('code_islands', [])
    score_6_islands = [i for i in islands if i.get('score', 0) >= 6]
    print(f'Score-6+ islands: {len(score_6_islands)}')
    for i in score_6_islands[:5]:
        start = i.get('start', 0)
        end = i.get('end', 0)
        score = i.get('score', 0)
        width = end - start + 1
        print(f"  C3:{start:04X}..C3:{end:04X} - score {score}, {width} bytes")
except Exception as e:
    print(f'Error loading 3100 seam block: {e}')
