openpilot patches
======

A collection of patches for modifying official openpilot, it may works with other community forks but not guaranteed.


usage
======

1. find your openpilot version, you will see something like this: **#define COMMA_VERSION "0.5.10-release** and your version will be **0.5.10**
    ```bash
    cat /data/openpilot/selfdrive/common/version.h | grep COMMA_VERSION
    ```

2. find the patch file and copy the command from the top of the file, e.g. (0.5.10/disable_mapd.diff line 1): 
    ```bash
    cd /data/openpilot && curl https://raw.githubusercontent.com/eFiniLan/openpilot-patches/master/0.5.10/disable_mapd.diff | git apply -v
    ```
3. If successful, you should see messages like this:
    ```bash
    Checking patch selfdrive/manager.py...
    Applied patch selfdrive/manager.py cleanly.
    ```

4. Now make openpilot compile, this is to avoid soft brick your device.
    ```bash
    python -m compileall . && make
    ```

5. If something went wrong, reset your branch and restart again:
    ```bash
    git reset --hard
    ```
