import json

# Read UTF-16 encoded file
filepath = 'reports/c3_3761_3c7f_flow.json'
with open(filepath, 'r', encoding='utf-16') as f:
    data = json.load(f)

print('=== C3:3761-3C7F Flow Analysis ===')
print(f"Range: {data.get('range', 'unknown')}")
print(f"Page family: {data.get('page_family', {}).get('page_family', 'unknown')}")
print(f"Total islands: {len(data.get('islands', []))}")

# Check islands for score-6+
islands = data.get('islands', [])
score_6_islands = [i for i in islands if i.get('score', 0) >= 6]
print(f'Score-6+ islands: {len(score_6_islands)}')

for i in score_6_islands[:20]:
    start = i.get('start', 0)
    end = i.get('end', 0)
    score = i.get('score', 0)
    size = end - start + 1 if end > start else 0
    print(f'  C3:{start:04X}..C3:{end:04X} - score {score} - {size} bytes')

print()
print('=== Checking 30B1 flow ===')
filepath2 = 'reports/c3_30b1_34ff_flow.json'
with open(filepath2, 'r', encoding='utf-16') as f:
    data2 = json.load(f)

print(f"Range: {data2.get('range', 'unknown')}")
islands2 = data2.get('islands', [])
score_6_islands2 = [i for i in islands2 if i.get('score', 0) >= 6]
print(f'Score-6+ islands: {len(score_6_islands2)}')

for i in score_6_islands2[:15]:
    start = i.get('start', 0)
    end = i.get('end', 0)
    score = i.get('score', 0)
    size = end - start + 1 if end > start else 0
    print(f'  C3:{start:04X}..C3:{end:04X} - score {score} - {size} bytes')
