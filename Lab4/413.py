import json
import re

token_re = re.compile(r'([A-Za-z_][A-Za-z0-9_]*)|\[(\d+)\]')

def resolve_query(data, query):
    cur = data

    parts = query.split('.')
    for part in parts:
        if part == "":
            return None, False

        for m in token_re.finditer(part):
            key = m.group(1)
            idx = m.group(2)

            if key is not None:
                if isinstance(cur, dict) and key in cur:
                    cur = cur[key]
                else:
                    return None, False

            else:  
                i = int(idx)
                if isinstance(cur, list) and 0 <= i < len(cur):
                    cur = cur[i]
                else:
                    return None, False

    return cur, True


data = json.loads(input())
q = int(input())

for _ in range(q):
    query = input().strip()
    val, ok = resolve_query(data, query)
    if ok:
        print(json.dumps(val, separators=(",", ":")))
    else:
        print("NOT_FOUND")