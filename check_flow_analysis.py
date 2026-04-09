import json

# Check flow analysis for more candidates
with open('reports/c3_3761_3c7f_flow.json') as f:
    data = json.load(f)

print('=== C3:3761-3C7F Flow Analysis ===')
print(f"Total nodes: {len(data.get('nodes', []))}")
print(f"Total islands: {len(data.get('islands', []))}")

# Check islands for score-6+
islands = data.get('islands', [])
score_6_islands = [i for i in islands if i.get('score', 0) >= 6]
print(f'Score-6+ islands: {len(score_6_islands)}')

for i in score_6_islands[:15]:
    start = i.get('start', 0)
    end = i.get('end', 0)
    score = i.get('score', 0)
    size = end - start + 1 if end > start else 0
    print(f'  C3:{start:04X}..C3:{end:04X} - score {score} - {size} bytes')

print()

# Check 30b1 flow
with open('reports/c3_30b1_34ff_flow.json') as f:
    data = json.load(f)

print('=== C3:30B1-34FF Flow Analysis ===')
print(f"Total nodes: {len(data.get('nodes', []))}")
print(f"Total islands: {len(data.get('islands', []))}")

# Check islands for score-6+
islands = data.get('islands', [])
score_6_islands = [i for i in islands if i.get('score', 0) >= 6]
print(f'Score-6+ islands: {len(score_6_islands)}')

for i in score_6_islands[:10]:
    start = i.get('start', 0)
    end = i.get('end', 0)
    score = i.get('score', 0)
    size = end - start + 1 if end > start else 0
    print(f'  C3:{start:04X}..C3:{end:04X} - score {score} - {size} bytes')
