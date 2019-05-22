import os
import sys
import json
import io

reload(sys)
sys.setdefaultencoding("utf-8")

# we need language and ip
if len(sys.argv) < 3:
    print("Usage: install.py <locale> <json translation file> <index.android.bundle file>")
    os._exit(1)

locale = sys.argv[1]
json_file = sys.argv[2]
bundle_file = sys.argv[3]

with open(json_file, 'r') as f:
    ds = json.load(f)

# print(ds)
# os._exit(1)
if os.path.isfile(bundle_file):
    src = io.open(bundle_file, 'r', encoding='utf-8')
    content = src.read()
    print("Patching strings")
    for string in ds:
        content = content.replace(string['en'], string[locale])
    dest = open(bundle_file, 'w')
    dest.write(content)
