import sys
sys.setrecursionlimit(1000000)


def dump(name, obj, level=0):
    indent = level * '  '#'\t'

    if name is not None:
        prefix = indent + name + " = "
    else:
        prefix = indent

    if isinstance(obj, (int, float, str)):
        print(prefix + str(obj))
    elif isinstance(obj, list):
        print (prefix + "[")

        for value in obj:
            dump(None, value, level + 1)

        print (indent + "]")
    elif isinstance(obj, dict):
        print (prefix + "{")

        for key, value in obj.items():
            dump(key, value, level + 1)

        print (indent + "}")
    else:
        # if obj.__class__.__name__ == "method":
        #     return
        print (prefix + obj.__class__.__name__)

        for key in dir(obj):
            if key.startswith("__") or key == "_accept" or key.startswith("T_"):
                continue

            val = getattr(obj, key)
            if val == None or val == "":
                continue

            dump(key, val, level + 1)
