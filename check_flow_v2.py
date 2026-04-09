import json
import os

# Check if file exists and has content
filepath = 'reports/c3_3761_3c7f_flow.json'
size = os.path.getsize(filepath)
print(f'File size: {size} bytes')

# Try to read with different encodings
for encoding in ['utf-8', 'utf-16', 'latin-1', 'cp1252']:
    try:
        with open(filepath, 'r', encoding=encoding) as f:
            content = f.read(1000)
            print(f'{encoding}: First 200 chars: {content[:200]}')
            break
    except Exception as e:
        print(f'{encoding}: {e}')
