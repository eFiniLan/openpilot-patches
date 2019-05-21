import os
import sys
import json

reload(sys)
sys.setdefaultencoding("utf-8")

with open('./strings.json', 'r') as f:
    ds = json.load(f)

# we need language and ip
if len(sys.argv) < 2:
    print("Usage: install.py <locale> <EON IP>")
    print("Available locale: '%s'" % '\', \''.join(ds["locales"]))
    os._exit(1)

locale = sys.argv[1]
if os.path.isfile('index.android.bundle'):
    src = io.open('index.android.bundle', 'r', encoding='utf-8')
    content = src.read()
    print("Patching strings")
    for string in strings:
        content = content.replace(string['en'], string[locale])
    dest = open('./tmp/apk_src/assets/index.android.bundle', 'w')
    dest.write(content)
