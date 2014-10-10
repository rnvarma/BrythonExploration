import javascript, browser, sys
from contextWrapper import *

"""
Adapted for Brython from
http://www.abeautifulsite.net/detecting-mobile-devices-with-javascript/
"""
class Struct(): pass

def onMobileTimer():
    pass

def onComputerTimer():
    horizAcc = data.arrowKeys.right - data.arrowKeys.left
    vertAcc = data.arrowKeys.down - data.arrowKeys.up
    data.xVel += horizAcc
    data.yVel += vertAcc
    if horizAcc == 0 or (horizAcc*data.xVel < 0):
        data.xVel = int(data.xVel * 0.7)
    if vertAcc == 0 or (vertAcc*data.yVel < 0):
        data.yVel = int(data.yVel * 0.7)

def onTimer():
    if data.mobile: onMobileTimer()
    else: onComputerTimer()
    data.x += data.xVel
    data.y += data.yVel
    if data.x < 0:
        data.x = 0
        data.xVel = 0
    if data.x > canvas.width:
        data.x = canvas.width
        data.xVel = 0
    if data.y < 0:
        data.y = 0
        data.yVel = 0
    if data.y > canvas.height:
        data.y = canvas.height
        data.yVel = 0
    redrawAll()

def redrawAll():
    context.clear()
    x, y, r = data.x, data.y, data.radius
    context.drawImage(data.video, 0, 0, width=canvas.width, height=canvas.height)
    context.create_circle(x, y, r, fill="#ff0000")
    context.create_text(x, y, data.latitude, anchor=S)
    context.create_text(x, y, data.longitude, anchor=N)
    context.create_text(canvas.width/2, 0, str(data.touch), anchor=N, fill="#0000FF")

def isOnMobile():
    agent = browser.window.navigator.userAgent.lower()
    android = "android" in agent
    blackberry = "blackberry" in agent
    iOS = ("iphone" in agent) or ("ipad" in agent) or ("ipod") in agent
    opera = "opera mini" in agent
    windows = "iemobile" in agent
    return android or blackberry or iOS or opera or windows

KEY_CODE_NAMES = { 3:"Cancel", 6:"Help", 8:"Backspace", 9:"Tab", 12:"Clear",
                   13:"Return", 14:"Enter", 16:"Shift", 17:"Control", 18:"Alt",
                   19:"Pause", 20:"CapsLock", 27:"Escape", 32:"Space",
                   33:"PageUp", 34:"PageDown", 35:"End", 36:"Home", 37:"Left",
                   38:"Up", 39:"Right", 40:"Down", 44:"PrintScreen",
                   45:"Insert", 46:"Delete", 112:"F1", 113:"F2", 114:"F3",
                   115:"F4", 116:"F5", 117:"F6", 118:"F7", 119:"F8", 120:"F9",
                   121:"F10", 122:"F11", 123:"F12", 144:"NumLock",
                   145:"ScrollLock", 192:"`", 224:"Meta"
                 }

def keyEvent(event, val):
    keyName = KEY_CODE_NAMES.get(event.keyCode)
    if keyName == "Left": data.arrowKeys.left = val
    elif keyName == "Right": data.arrowKeys.right = val
    elif keyName == "Up": data.arrowKeys.up = val
    elif keyName == "Down": data.arrowKeys.down = val

def touchEvent(event):
    if (event.type == "touchstart"):
        data.touch = True
        data.calibrating = True
    elif (event.type == "touchend"):
        data.touch = False

def tilt(event):
    if data.calibrating:
        data.beta = event.beta
        data.gamma = event.gamma
        if data.xVel > 0: data.xVel -= 1
        elif data.xVel < 0: data.xVel += 1
        if data.yVel > 0:   data.yVel -= 1
        elif data.yVel < 0: data.yVel += 1
        if not data.touch: data.calibrating = False
    else:
        beta = event.beta - data.beta
        gamma = event.gamma - data.gamma
        data.yVel += int(beta/10)
        data.xVel += int(gamma/10)
        if abs(gamma) < 3:
            if data.xVel > 0: data.xVel -= 1
            elif data.xVel < 0: data.xVel += 1
        if abs(beta) < 3:
            if data.yVel > 0:   data.yVel -= 1
            elif data.yVel < 0: data.yVel += 1

def run(timerDelay=50, canvasId="brythonCanvas", consoleId=None,
        globalFocus=False):
    global canvas, context, data
    onMobile = isOnMobile()
    canvas = browser.document[canvasId]
    class Struct(): pass
    data = Struct()
    data.mobile = onMobile
    data.ratio = 10
    data.arrowKeys = Struct()
    data.arrowKeys.left = data.arrowKeys.right = False
    data.arrowKeys.up = data.arrowKeys.down = False
    data.timerDelay = timerDelay
    data.latitude = "Searching..."
    data.longitude = ""
    data.video = browser.document['video']
    data.calibrating = True
    data.touch = False
    data.bottomText = str(42)
    def setPos(position):
        coords = position.coords
        data.latitude = str(round(coords.latitude, 2))
        data.longitude = str(round(coords.longitude, 2))
    browser.window.navigator.geolocation.getCurrentPosition(setPos)
    if onMobile:
        data.tilts = Struct()
        browser.document.bind("touchstart", touchEvent)
        browser.document.bind("touchend", touchEvent)
        browser.window.addEventListener("deviceorientation", tilt, True)
    else:
        browser.document.bind("keydown", lambda event: keyEvent(event, True))
        browser.document.bind("keyup", lambda event: keyEvent(event, False))
    context = ContextWrapper(canvas)
    data.radius = min(canvas.width, canvas.height) / 10
    data.x, data.y = canvas.width / 2, canvas.height / 2
    data.xVel = data.yVel = 0
    def timerWrapper():
        onTimer()
        browser.window.setTimeout(timerWrapper, data.timerDelay)
    timerWrapper()

run()