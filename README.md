# Simplified Appium
Appium test automation without the need to install Appium Desktop. You also can start testing directly from your mobile phone.
If you don't know about appium goto this url [appium.io](http://appium.io/ "appium.io").
You can find more detail about android apps used in this repo from here:

- [io.appium.settings](https://github.com/appium/io.appium.settings "io.appium.settings")
- [io.appium.uiautomator2.server](https://github.com/appium/appium-uiautomator2-server "io.appium.uiautomator2.server")

## Getting Started
### Required
- Connect mobile phone to PC via USB
- Make sure USB debugging setting is enable
- ADB added to environment variable path (open `command prompt` then type `adb version`, if output showing version then ADB is configured properly)
Read this if you don't know what to do:

	[https://www.xda-developers.com/install-adb-windows-macos-linux/](https://www.xda-developers.com/install-adb-windows-macos-linux/ "https://www.xda-developers.com/install-adb-windows-macos-linux/")

	[https://www.xda-developers.com/adb-fastboot-any-directory-windows-linux/](https://www.xda-developers.com/adb-fastboot-any-directory-windows-linux/ "https://www.xda-developers.com/adb-fastboot-any-directory-windows-linux/")


### Install UI Automator Server
- Clone this repo (`git clone https://github.com/thiovan/simplified-appium`)
- Run `install.bat` and wait until message `Done.` shown
- Open browser and open this url `http://localhost:6790/wd/hub/status`
- Make sure response showing like this:
```json
{
	"sessionId": "None",
	"value": {
			"message": "UiAutomator2 Server is ready to accept commands",
			"ready": true
	}
}
```
If server not responding try run `install.bat` once again
- Close all `command prompt` window and disconnect your mobile phone from USB
- Your mobile phone now ready for test automation

If get error: more than one device and emulator, follow this step first
- Open `command prompt` and run this command `adb devices`
- Open `install.bat` with text editor and replace `YOUR_DEVICE_SERIAL_HERE` with serial number from adb output, then save your changes
- Run `install.bat` again


### Todo List
- Script automatic detect device serial
- Build simple interface software or mobile apps
- List all available API
- Example for another programming language

If you want to complete task in this todo list, feel free to ask pull request