# Simplified Appium
Appium test automation without the need to install Appium Server (Desktop). You also can start testing directly from your mobile phone.

##### Before: 

`Client Program -> Appium Server (PC) -> Appium UIAutomator Server (Android) -> Apps (Android)`

##### After: 

`Client Program -> Appium UIAutomator Server (Android) -> Apps (Android)`

If you want to learn about appium goto this url [appium.io](http://appium.io/ "appium.io").
You also can find more detail about android apps used in this repo from here:

- [io.appium.settings](https://github.com/appium/io.appium.settings "io.appium.settings")
- [io.appium.uiautomator2.server](https://github.com/appium/appium-uiautomator2-server "io.appium.uiautomator2.server")

## Getting Started
### Required
- Connect mobile phone to PC via USB
- Make sure USB debugging setting is enable
- ADB added to environment variable path (open `command prompt` then type `adb version`, if output showing version then ADB is configured properly). Read this if you don't know what to do:

	[https://www.xda-developers.com/install-adb-windows-macos-linux/](https://www.xda-developers.com/install-adb-windows-macos-linux/ "https://www.xda-developers.com/install-adb-windows-macos-linux/")

	[https://www.xda-developers.com/adb-fastboot-any-directory-windows-linux/](https://www.xda-developers.com/adb-fastboot-any-directory-windows-linux/ "https://www.xda-developers.com/adb-fastboot-any-directory-windows-linux/")


### Install UI Automator Server
- Clone this repo (`git clone https://github.com/thiovan/simplified-appium`)
- Run `install.bat` and wait until message `Done.` shown
- Open browser and goto this url `http://localhost:6790/wd/hub/status`
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
If server not responding or response not match try run `install.bat` once again
- Your mobile phone now ready for test automation. If you want run test automation without PC, just close all `command prompt` window and disconnect your mobile phone from USB

If get error: `more than one device and emulator`, follow this step first
- Open `command prompt` and run this command `adb devices`
- Open `install.bat` with text editor and replace `YOUR_DEVICE_SERIAL_HERE` with serial number from adb output, then save your changes
- Run `install.bat` again


### Run Test Automation
#### Directly From Phone
- Copy `play-store.py` from `example` directory to your phone internal memory
- Install termux (https://play.google.com/store/apps/details?id=com.termux)
- Open termux then run install python (`pkg install python`)
- Run command `termux-setup-storage`
- Run command `python ~/storage/shared/play-store.py`
- Automation test will running

#### Using PC
- Open `command prompt` then run this command `adb forward tcp:6790 tcp:6790`
- Run command `python play-store.py`
- Automation test will running

Notes: `play-store.py` inside `example` directory just sample, you could implement your own automation testing.

### API Docs
This is list available API in Appium UIAutomator server (notes: list still incomplete)

https://thiovan.github.io/simplified-appium/api-docs/

Parameters used in this API docs:
```json
_.base_url => http://127.0.0.1:6790/wd/hub
_.session_id => hit session create API then you will retrieve sessionId (example: 02150934-8a1b-4233-b48c-d33c491fda79)
:element => hit find element API then you will retrieve ELEMENT (example: 51fad69d-895b-4c11-8381-7ed85b314824)
```

### Todo List
- Build simple interface software or mobile apps
- List all available API
- Add support for IOS apps
- Example for another programming language

If you want to complete task in this todo list, feel free to ask pull request