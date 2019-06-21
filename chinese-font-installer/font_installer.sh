#!/usr/bin/bash

## Android 端設定成中文介面 (zh-TW = 繁中, zh-CN = 简中)
lang=zh-TW
update_font_conf=0

if [ ! -f "/system/fonts/Miui-Regular.ttf" ]; then
    update_font_conf=1
    mount -o remount,rw /system && curl -o /system/fonts/Miui-Regular.ttf https://raw.githubusercontent.com/eFiniLan/openpilot-patches/master/chinese-font-installer/assets/Miui-Regular.ttf
fi

if [ ! -f "/system/fonts/Miui-Bold.ttf" ]; then
    update_font_conf=1
    mount -o remount,rw /system && curl -o /system/fonts/Miui-Bold.ttf https://raw.githubusercontent.com/eFiniLan/openpilot-patches/master/chinese-font-installer/assets/Miui-Bold.ttf
fi

if ls /system/fonts/DroidSansFallback*.ttf 1> /dev/null 2>&1; then
    mount -o remount,rw /system && rm -fr /system/fonts/DroidSansFallback*.ttf
fi

if [[ $update_font_conf -eq "1" ]]; then
    mount -o remount,rw /system && curl -o /system/etc/fonts.xml https://raw.githubusercontent.com/eFiniLan/openpilot-patches/master/chinese-font-installer/assets/fonts.xml
    chmod 644 /system/etc/fonts.xml
fi

setprop persist.sys.locale $lang