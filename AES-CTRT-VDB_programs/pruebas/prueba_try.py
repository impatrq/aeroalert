import json
a = json.dumps(['foo', {'bar': ('baz', None, 1.0, 2)}])


print(json.dumps("hola").encode('utf-8'))
# '["foo", {"bar": ["baz", null, 1.0, 2]}]'