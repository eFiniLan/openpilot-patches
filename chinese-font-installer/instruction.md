```bash
# 加載成可讀寫模式
mount-o remount,rw /system

# 下載+安裝字型
curl -o /system/fonts/DroidSansFallback.ttf https://raw.githubusercontent.com/eFiniLan/openpilot-patches/master/chinese-font-installer/fonts/DroidSansFallback.ttf
curl -o /system/fonts/DroidSansFallbackFull.ttf https://raw.githubusercontent.com/eFiniLan/openpilot-patches/master/chinese-font-installer/fonts/DroidSansFallbackFull.ttf

# 設定成中文介面 (Android 端: zh-TW = 繁中, zh-CN = 简中)
setprop persist.sys.locale zh-TW

# 重開機
reboot
```