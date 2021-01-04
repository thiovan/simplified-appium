import os
import time
import logging
import datetime
import requests

logging.basicConfig(level=logging.INFO,
                    format="%(asctime)s.%(msecs)03d [%(levelname)s]: %(message)s", datefmt="%Y-%m-%d %H:%M:%S")

config = {
    "baseApi": "http://127.0.0.1:6790/wd/hub",
    "appPackage": "com.android.vending",
    "appActivity": "AssetBrowserActivity"
}

isAndroid = 'ANDROID_STORAGE' in os.environ or 'ANDROID_ROOT' in os.environ

try:
    # launch apps
    if isAndroid:
        os.system("am start -W -n {0}/.{1} -S -a android.intent.action.MAIN -c android.intent.category.LAUNCHER -f 0x10200000".format(
            config["appPackage"], config["appActivity"]))
    else:
        os.system("adb shell am start -W -n {0}/.{1} -S -a android.intent.action.MAIN -c android.intent.category.LAUNCHER -f 0x10200000".format(
            config["appPackage"], config["appActivity"]))

    def command(type, *args, **kwargs):
        requestData = kwargs.get('data', None)
        sessionId = kwargs.get('sessionId', None)
        elementId = kwargs.get('elementId', None)

        if type == "status":
            requestMethod = "get"
            requestUrl = "{0}/status".format(config['baseApi'])
        elif type == "createSession":
            requestMethod = "post"
            requestUrl = "{0}/session".format(config['baseApi'])
        elif type == "findElement":
            requestMethod = "post"
            requestUrl = "{0}/session/{1}/element".format(
                config['baseApi'], sessionId)
        elif type == "clickElement":
            requestMethod = "post"
            requestUrl = "{0}/session/{1}/element/{2}/click".format(
                config['baseApi'], sessionId, elementId)
        elif type == "inputElement":
            requestMethod = "post"
            requestUrl = "{0}/session/{1}/element/{2}/value".format(
                config['baseApi'], sessionId, elementId)
        elif type == "goBack":
            requestMethod = "post"
            requestUrl = "{0}/session/{1}/back".format(
                config['baseApi'], sessionId)

        if requestMethod == 'post':
            r = requests.post(requestUrl, json=requestData)
        else:
            r = requests.get(requestUrl, json=requestData)

        if r.ok:
            return r.json()
        else:
            raise Exception(r.json()["value"]["error"])

    logging.info("checking is uiautomator server running")
    if not command('status'):
        raise Exception("UIAutomator server not running.")

    logging.info("create new session")
    sessionId = command("createSession", data={
        "capabilities": {
        }
    })["sessionId"]

    time.sleep(1)

    logging.info("find hamburger icon element")
    elementId = command("findElement", sessionId=sessionId, data={
        "strategy": "xpath",
        "selector": "//android.widget.FrameLayout[@content-desc='Show navigation drawer']"
    })["value"]["ELEMENT"]

    logging.info("click hamburger icon element (open drawer)")
    command("clickElement", sessionId=sessionId, elementId=elementId)

    time.sleep(1)

    logging.info("press navigation back button")
    command("goBack", sessionId=sessionId)

    time.sleep(1)

    logging.info("find search bar element")
    elementId = command("findElement", sessionId=sessionId, data={
        "strategy": "xpath",
        "selector": "//android.widget.TextView[contains(@text, 'Search for apps & games')]"
    })["value"]["ELEMENT"]

    logging.info("click search bar element")
    command("clickElement", sessionId=sessionId, elementId=elementId)

    time.sleep(1)

    logging.info("find search text input element")
    elementId = command("findElement", sessionId=sessionId, data={
        "strategy": "xpath",
        "selector": "//android.widget.EditText[contains(@text, 'Search for apps & games')]"
    })["value"]["ELEMENT"]

    logging.info(
        "input text 'google' then press enter to search text input element")
    command("inputElement", sessionId=sessionId, elementId=elementId, data={
        "text": "google\\n"
    })

    time.sleep(1)

    logging.info("find first result element")
    elementId = command("findElement", sessionId=sessionId, data={
        "strategy": "xpath",
        "selector": "//android.support.v7.widget.RecyclerView/android.widget.LinearLayout[1]"
    })["value"]["ELEMENT"]

    logging.info("click first result element")
    command("clickElement", sessionId=sessionId, elementId=elementId)

    time.sleep(2)

    logging.info("closing apps")
    if isAndroid:
        for x in range(3):
            command("goBack", sessionId=sessionId)
    else:
        os.system("adb shell am force-stop {0}".format(config["appPackage"]))

    logging.info("Done.")

except Exception as e:
    logging.error(str(e))
    if isAndroid:
        for x in range(3):
            command("goBack", sessionId=sessionId)
    else:
        os.system("adb shell am force-stop {0}".format(config["appPackage"]))
    exit()
