import json
from pathlib import Path

path = Path(input('Input path. > ').strip())
print(path)
mode = int(input('1: Remove recipe autolearn\nMode. > '))
output = Path(input('Output. >').strip())




for filename in path.rglob('*.json'):
    with open(filename, 'r', encoding='utf-8') as file:
        data = json.load(file)
    fileOut = []
    match mode:
        case 1:
            for entry in data:
                if entry.get('type') not in ('practice', 'recipe'):
                    continue
                try:
                    autolearn = entry.get('autolearn')
                     
                    
                    entryOut = {
                            'type': entry.get('type')
                        }
                    
                    for i in ('tools','components','qualities'):
                        if entry.get(i):
                            entryOut[i] = entry.get(i)
                    
                    if entry.get('type') == 'practice' and autolearn:
                        for skill in autolearn:
                            skill[1] = 11
                        entryOut['id'] = entry.get('id')
                        entryOut['name'] = entry.get('name')
                        entryOut['copy-from'] = entry.get('id')
                        entryOut['autolearn'] = autolearn
                        fileOut.append(entryOut)
                    elif entry.get('type') == 'recipe':
                        if autolearn == False and not entry.get('copy-from') or entry.get('never_learn'):
                            continue
                        entry['autolearn'] = False
                        fileOut.append(entry)
                            
                except Exception as e: print(e)
            
            if not fileOut:
                continue
            try:
                
                dir = output / filename.parent.relative_to(path)
                dir.mkdir(parents=True, exist_ok=True)
                print(dir)
                with open(dir / filename.name, 'w', encoding='utf-8') as f:
                    json.dump(fileOut, f, ensure_ascii=False, indent=4)
            except Exception as e: print(e)
        case _:
            print("Invalid mode selected.")
            break



input("Press enter to exit.")