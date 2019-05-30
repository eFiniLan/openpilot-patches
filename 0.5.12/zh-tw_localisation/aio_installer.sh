#!/usr/bin/bash
#
# 中文化一鍵安裝
# curl https://raw.githubusercontent.com/eFiniLan/openpilot-patches/master/0.5.12/zh-tw_localisation/aio_installer.sh | bash
#

# 加載成可讀寫模式
mount -o remount,rw /system && \

# 下載+安裝小米蘭亭字型
curl -o /system/fonts/Miui-Regular.ttf https://raw.githubusercontent.com/eFiniLan/openpilot-patches/master/chinese-font-installer/assets/Miui-Regular.ttf && \
curl -o /system/fonts/Miui-Bold.ttf https://raw.githubusercontent.com/eFiniLan/openpilot-patches/master/chinese-font-installer/assets/Miui-Bold.ttf && \

# 刪除 DroidSansFallback 字型 (舊版)
rm -fr /system/fonts/DroidSansFallback*.ttf && \

# 設定字型權限
chmod 644 /system/fonts/Miui-* && \

# 下載+安裝字型設定檔 (DroidSansFallback 改成 小米蘭亭)
curl -o /system/etc/fonts.xml https://raw.githubusercontent.com/eFiniLan/openpilot-patches/master/chinese-font-installer/assets/fonts.xml && \

# 設定字型設定檔權限
chmod 644 /system/etc/fonts.xml && \

# Android 端設定成中文介面 (zh-TW = 繁中, zh-CN = 简中)
setprop persist.sys.locale zh-TW && \

# 補丁 ai.comma.plus.offroad
curl -o /data/openpilot/apk/ai.comma.plus.offroad.apk https://raw.githubusercontent.com/eFiniLan/openpilot-patches/master/0.5.12/zh-tw_localisation/ai.comma.plus.offroad.apk && \
curl -o /data/openpilot/apk/ai.comma.plus.frame.apk https://raw.githubusercontent.com/eFiniLan/openpilot-patches/master/0.5.12/zh-tw_localisation/ai.comma.plus.frame.apk && \

cd /data/openpilot && \

# 補丁 ui.c
curl https://raw.githubusercontent.com/eFiniLan/openpilot-patches/master/0.5.12/zh-tw_localisation/patch_ui.diff | git apply -v && \

# 補丁 alerts.py
curl https://raw.githubusercontent.com/eFiniLan/openpilot-patches/master/0.5.12/zh-tw_localisation/patch_alerts.diff | git apply -v

# 更換 nanovg 裡的 stb libraries 到最新版 (2.22 & 1.21)
curl -o /data/openpilot/phonelibs/nanovg/stb_image.h https://raw.githubusercontent.com/eFiniLan/openpilot-patches/master/0.5.12/zh-tw_localisation/stb_image.h && \
curl -o /data/openpilot/phonelibs/nanovg/stb_truetype.h https://raw.githubusercontent.com/eFiniLan/openpilot-patches/master/0.5.12/zh-tw_localisation/stb_truetype.h && \

echo Completed!
