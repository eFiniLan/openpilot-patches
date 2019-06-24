#!/usr/bin/bash

## Android 端設 Z H~P中 V~G K ]  (zh-TW =  A中, zh-CN =  @中)
lang=zh-TW
update_font_reg=0
update_font_bold=0
remove_old_font=0

# check regular font
if [ ! -f "/system/fonts/Miui-Regular.ttf" ]; then
    update_font_reg=1
fi

# check bold font
if [ ! -f "/system/fonts/Miui-Bold.ttf" ]; then
    update_font_bold=1
fi

# check droidsans font
if ls /system/fonts/DroidSansFallback*.ttf 1> /dev/null 2>&1; then
    remove_old_font=1
fi

if [ $update_font_reg -eq "1" ] || [ $update_font_bold -eq "1" ] || [ $remove_old_font -eq "1" ]; then
    # sleep 5 secs in case, make sure the /system is remountable
    sleep 5
    mount -o remount,rw /system
    if [ $update_font_reg -eq "1" ] || [ $update_font_bold -eq "1" ]; then
        # download regular font
        if [ $update_font_reg -eq "1" ]; then
            curl -o /system/fonts/Miui-Regular.ttf https://raw.githubusercontent.com/eFiniLan/openpilot-patches/master/chinese-font-installer/assets/Miui-Regular.ttf
        fi
        # download bold font
        if [ $update_font_bold -eq "1" ]; then
            curl -o /system/fonts/Miui-Bold.ttf https://raw.githubusercontent.com/eFiniLan/openpilot-patches/master/chinese-font-installer/assets/Miui-Bold.ttf
        fi
        # dont new font mapping
        curl -o /system/etc/fonts.xml https://raw.githubusercontent.com/eFiniLan/openpilot-patches/master/chinese-font-installer/assets/fonts.xml
        chmod 644 /system/etc/fonts.xml
        chmod 644 /system/fonts/Miui-*
    fi
    # remove driodsans font
    if [ $remove_old_font -eq "1" ]; then
        rm -fr /system/fonts/DroidSansFallback*.ttf
    fi
    mount -o remount,r /system
    # change system locale
    setprop persist.sys.locale $lang
fi