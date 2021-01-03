@echo off
color 0A

SET DEVICE_SERIAL=YOUR_DEVICE_SERIAL_HERE
SET ADB_SERVER_PORT=5037
SET APKS_DIR=%cd%\apks


if %DEVICE_SERIAL% == YOUR_DEVICE_SERIAL_HERE goto EMPTY_DEVICE_SERIAL
if %DEVICE_SERIAL% == "" goto EMPTY_DEVICE_SERIAL
goto NOT_EMPTY_DEVICE_SERIAL
:EMPTY_DEVICE_SERIAL
SET PREFIX_COMMAND=adb -P %ADB_SERVER_PORT%
goto MAIN 
:NOT_EMPTY_DEVICE_SERIAL
SET PREFIX_COMMAND=%PREFIX_COMMAND%
goto MAIN


:MAIN
echo Starting ADB server on port %ADB_SERVER_PORT%...
adb -P %ADB_SERVER_PORT% start-server
if errorlevel 1 goto FAILURE

echo Relaxing hidden api policy...
%PREFIX_COMMAND% shell 'settings put global hidden_api_policy_pre_p_apps 1;settings put global hidden_api_policy_p_apps 1;settings put global hidden_api_policy 1' >NUL 2>NUL

echo Getting install status for io.appium.settings...
%PREFIX_COMMAND% shell dumpsys package io.appium.settings | findstr /I io.appium.settings >NUL
if %errorlevel% == 1 (
    echo Installing io.appium.settings...
    %PREFIX_COMMAND% install -r -g %APKS_DIR%\settings_apk-debug.apk
    if errorlevel 1 goto FAILURE
)

echo Starting io.appium.settings...
%PREFIX_COMMAND% shell am start -n io.appium.settings/.Settings -a android.intent.action.MAIN -c android.intent.category.LAUNCHER >NUL
if errorlevel 1 goto FAILURE

echo Forwarding system port: 6790 to device port: 6790
%PREFIX_COMMAND% forward tcp:6790 tcp:6790 >NUL
if errorlevel 1 goto FAILURE

echo Getting install status for io.appium.uiautomator2.server...
%PREFIX_COMMAND% shell dumpsys package io.appium.uiautomator2.server | findstr /I io.appium.uiautomator2.server >NUL
if %errorlevel% == 1 (
    echo Installing io.appium.uiautomator2.server...
    %PREFIX_COMMAND% install -r -g %APKS_DIR%\appium-uiautomator2-server-v4.15.0.apk
    if errorlevel 1 goto FAILURE
)

echo Getting install status for io.appium.uiautomator2.server.test...
%PREFIX_COMMAND% shell dumpsys package io.appium.uiautomator2.server.test | findstr /I io.appium.uiautomator2.server.test >NUL
if %errorlevel% == 1 (
    echo Installing io.appium.uiautomator2.server.test...
    %PREFIX_COMMAND% install -r -g %APKS_DIR%\appium-uiautomator2-server-debug-androidTest.apk
    if errorlevel 1 goto FAILURE
)

echo Performing shallow cleanup of automation leftovers...
%PREFIX_COMMAND% shell am force-stop io.appium.uiautomator2.server.test
if errorlevel 1 goto FAILURE

echo Starting UIAutomator2 server...
start cmd /c %PREFIX_COMMAND% shell nohup am instrument -w io.appium.uiautomator2.server.test/androidx.test.runner.AndroidJUnitRunner

echo Done.
pause >NUL
exit


:FAILURE
echo Something wrong please check message above.
pause >NUL