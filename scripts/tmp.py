import os
import sys
import json
import paramiko
import subprocess
import io
import shutil
import zipfile

ds = None
locale = None
ip = None
ssh = None
key = None

# print(sys.getdefaultencoding())
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
ip = sys.argv[2]

# connect to eon
print("connecting to EON @ %s" % ip)
try:
    ssh = paramiko.SSHClient()
    ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    key = paramiko.RSAKey.from_private_key_file('openpilot_rsa')
    ssh.connect(hostname=ip, username='root', pkey=key, port=8022)
except Exception as e:
    print("*** Connect failed: " + str(e))

print("Connected")

# connect sftp as well
sftp = paramiko.SFTPClient.from_transport(ssh.get_transport())
sftp = ssh.open_sftp()

# # install fonts if required
# if locale in ds["fonts"]:
#     print("Installing fonts")
#     stdin, stdout, stderr = ssh.exec_command('mount-o remount,rw /system')
#     for font in ds["fonts"][locale]:
#         local_path = './fonts/' + font
#         remote_path = '/system/fonts/' + font
#         print("--- Uploading " + local_path)
#         sftp.put(local_path, remote_path)
#         stdin, stdout, stderr = ssh.exec_command('chmod 644 /system/fonts/' + font)
#     print("fonts installed")
#     stdin, stdout, stderr = ssh.exec_command('mount-o remount,r /system')
#
# # change android locale
# print("Change system locale to: " + locale)
# stdin, stdout, stderr = ssh.exec_command('setprop persist.sys.locale ' + locale.replace('_', '-'))

# loop files
for file in ds['translations']:
    path = file['path']
    print('Patching ' + path)
    type = file['type']
    strings = file['strings']
    filename = path.split('/')[-1]
    local_unsigned_path = './tmp/unsigned_' + filename
    local_signed_path = './tmp/' + filename

    # download the file
    sftp.get(path, local_signed_path)

    # if it's a react-native apk file, we use apktool to extract
    # if type == 'react-native':
    #     subprocess.call(['./bin/apktool', 'd', local_path, '-o', './tmp/apk_src/'])
    #     if os.path.isfile('./tmp/apk_src/assets/index.android.bundle'):
    #         src = io.open('./tmp/apk_src/assets/index.android.bundle', 'r', encoding='utf-8')
    #         content = src.read()
    #         print("Patching strings")
    #         for string in strings:
    #             content = content.replace(string['en'], string[locale])
    #         dest = open('./tmp/apk_src/assets/index.android.bundle', 'w')
    #         dest.write(content)
    #         # os.remove(local_path)
    #         subprocess.call(['./bin/apktool', 'b', './tmp/apk_src/', '-o', local_path])
    #         subprocess.call(['./bin/apksigner'])
    #         # shutil.rmtree('./tmp/apk_src')
    if type == 'react-native':
        subprocess.call(['./bin/apktool', 'd', local_signed_path, '-o', './tmp/apk_src/'])
        # zip_ref = zipfile.ZipFile(local_path, 'r')
        # zip_ref.extractall('./tmp/apk_src')
        # zip_ref.close()
        if os.path.isfile('./tmp/apk_src/assets/index.android.bundle'):
            src = io.open('./tmp/apk_src/assets/index.android.bundle', 'r', encoding='utf-8')
            content = src.read()
            print("Patching strings")
            for string in strings:
                content = content.replace(string['en'], string[locale])
            dest = open('./tmp/apk_src/assets/index.android.bundle', 'w')
            dest.write(content)
            os.remove(local_signed_path)
            subprocess.call(['./bin/apktool', 'b', './tmp/apk_src/', '-o', local_unsigned_path])
            # shutil.make_archive(local_path, 'zip', './tmp/apk_src')
            # os.rename(local_path + '.zip', local_path)
            shutil.rmtree('./tmp/apk_src')
            print("Re-sign apk")
            subprocess.call(['jarsigner', '-verbose', '-keystore', './key.keystore', '-storepass', 'password', local_unsigned_path, local_signed_path, 'key.keystore'])
            os._exit(1)
        else:
            print('Unable to patch ' + filename + ': react-native src not found.')

    # upload file

    # make a backup of the file patched
    # stdin, stdout, stderr = ssh.exec_command('cp ' + path + ' ' + path + '.bak')
    sftp.put(local_signed_path, path)
    print(path + " is patched and uploaded.")
    os.remove(local_signed_path)

sftp.close()
ssh.close()


def escape_chars( text, characters ):
    for character in characters:
        text = text.replace( character, '\\' + character )
    return text