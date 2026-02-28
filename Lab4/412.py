import json

MISSING = object()

def to_json_value(v):
    if v is MISSING:
        return "<missing>"
    return json.dumps(v, separators=(",", ":"))

def diff(a, b, path, out):
    # Если оба словари -> сравниваем по ключам рекурсивно
    if isinstance(a, dict) and isinstance(b, dict):
        keys = set(a.keys()) | set(b.keys())
        for k in keys:
            pa = a.get(k, MISSING)
            pb = b.get(k, MISSING)
            new_path = k if path == "" else path + "." + k
            diff(pa, pb, new_path, out)
        return

    # Если не словари -> сравниваем как значения
    if a is MISSING or b is MISSING or a != b:
        out.append(f"{path} : {to_json_value(a)} -> {to_json_value(b)}")


A = json.loads(input())
B = json.loads(input())

out = []
diff(A, B, "", out)

if not out:
    print("No differences")
else:
    out.sort()
    for line in out:
        print(line)