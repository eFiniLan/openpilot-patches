openpilot patches
======

A collection of patches for modifying official openpilot, it may works with other community forks but not guaranteed.


usage
======
```shell
# go to your openpilot folder
cd /data/openpilot

# find your openpilot version, you will see something like this: **#define COMMA_VERSION "0.5.8-release** and your version will be 0.5.8
cat selfdrive/common/version.h | grep COMMA_VERSION

# download and apply patch, repeat this step if you want to apply more patches.
curl https://github.com/eFiniLan/openpilot-patches/<version>/<patch_file>.patch | git apply -v

# make openpilot compile, making sure no errors
make

# now you can safely reboot your EON
reboot
```