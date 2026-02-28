import json

def apply_patch(source, patch):
   

    for key, pval in patch.items():

        if pval is None:
            if key in source:
                del source[key]
            continue

      
        if key in source and isinstance(source[key], dict) and isinstance(pval, dict):
            apply_patch(source[key], pval)

        else:
            
            source[key] = pval

    return source


source = json.loads(input())
patch = json.loads(input())

result = apply_patch(source, patch)

print(json.dumps(result, sort_keys=True, separators=(",", ":")))