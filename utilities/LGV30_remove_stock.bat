@echo off
REM PURPOSE: Remove apps from LGV30 factory image that appear to not be useful
echo Press enter to remove all un-necessary stock apps for T-Mobile LG V30
pause > nul

@echo on
REM search for installed packages: adb shell "pm list packages -f [NAME] -3"

REM remove MyT-Mobile app (available in Play store)
adb shell "pm uninstall -k --user 0 com.tmobile.pr.mytmobile"

REM !!!! DO NOT REMOVE THIS, it is needed for Google Calendar!
REM adb shell "pm uninstall -k --user 0 com.android.providers.calendar"

REM remove stock Email app
adb shell "pm uninstall -k --user 0 com.lge.email"

REM remove "Wifi Hotpot" widget (dumb button)
adb shell "pm uninstall -k --user 0 com.lge.wifihotspotwidget"
REM remove "Wifi Hotpot" app (links to Settings)
adb shell "pm uninstall -k --user 0 com.lge.hotspotlauncher"

REM remove stock Calendar app
adb shell "pm uninstall -k --user 0 com.android.calendar"

REM remove "Visual Voicemail" TMobile app
adb shell "pm uninstall -k --user 0 com.tmobile.vvm.application"

REM remove Facebook (available in Play store)
adb shell "pm uninstall -k --user 0 com.facebook.katana"
adb shell "pm uninstall -k --user 0 com.facebook.appmanager"
adb shell "pm uninstall -k --user 0 com.facebook.system"

REM remove Google Duo (available in Play store)
adb shell "pm uninstall -k --user 0 com.google.android.apps.tachyon"

REM remove Amazon Assistant and Attribution
adb shell "pm uninstall -k --user 0 com.amazon.aa"
adb shell "pm uninstall -k --user 0 com.amazon.aa.attribution"
