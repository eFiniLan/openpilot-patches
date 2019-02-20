openpilot patches
======

A collection of patches for modifying official openpilot, it may works with other community forks but not guaranteed.


usage
======

1. go to your openpilot folder
    ```shell
    cd /data/openpilot
    ```

2. find your openpilot version, you will see something like this: **#define COMMA_VERSION "0.5.8-release** and your version will be **0.5.8**
    ```shell
    cat selfdrive/common/version.h | grep COMMA_VERSION
    ```

3. download and apply patch, repeat this step if you want to apply more patches, e.g.:
    ```shell
    curl https://github.com/eFiniLan/openpilot-patches/0.5.8/shut_down_eon_after_90_mins_if_usb_disconnected.patch | git apply -v
    ```

4. make openpilot compile, making sure no errors
    ```shell
    make
    ```

5. now you can safely reboot your EON
    ```shell
    reboot
    ```