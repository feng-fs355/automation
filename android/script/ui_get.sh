###!/usr/bin/env bash
#!/usr/bin/env expect
echo "Uiautomatorviewer script"

adb shell uiautomator dump /sdcard/app.uix
adb pull /sdcard/app.uix /home/pi/Documents/script/app.uix

adb shell screencap -p /sdcard/app.png

adb pull /sdcard/app.png /home/pi/Documents/script/app.png