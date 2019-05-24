#!/usr/bin/bash

# 加載成可讀寫模式
mount -o remount,rw /system && \

# 下載+安裝小米蘭亭字型
curl -o /system/fonts/Miui-Regular.ttf https://raw.githubusercontent.com/eFiniLan/openpilot-patches/master/chinese-font-installer/assets/Miui-Regular.ttf && \
curl -o /system/fonts/Miui-Bold.ttf https://raw.githubusercontent.com/eFiniLan/openpilot-patches/master/chinese-font-installer/assets/Miui-Bold.ttf && \

# 設定字型權限
chmod 644 /system/fonts/Miui-*

# 下載+安裝字型設定檔 (DroidSansFallback 改成 小米蘭亭)
curl -o /system/etc/fonts.xml https://raw.githubusercontent.com/eFiniLan/openpilot-patches/master/chinese-font-installer/assets/fonts.xml && \

# 設定字型設定檔權限
chmod 644 /system/etc/fonts.xml

# Android 端設定成中文介面 (zh-TW = 繁中, zh-CN = 简中)
setprop persist.sys.locale zh-TW

