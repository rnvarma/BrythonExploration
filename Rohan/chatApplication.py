
# blob-catch.py
# A very simple demo of a Brython browser-based game
# By David Kosbie

import math, browser, time, javascript, json

from browser import ajax

# Use jsmath.random (since "import random" is not working very well)
jsmath = javascript.JSObject(browser.window["Math"])
random = jsmath.random

def send(msg, callback):
  POST_URL = "http://128.237.212.209:8080/"
  req = ajax.ajax()
  req.bind('complete', callback)
  req.open('POST', POST_URL, True)
  req.send(msg)

def recieve(callback):
  GET_URL = "http://128.237.212.209:8080/"
  req = ajax.ajax()
  req.bind('complete', callback)
  req.open('GET', GET_URL, True)
  req.send({"woooho":"woo"})

def onMessageSend(req):
  print("got here")
  print(req.text)

def onMessageRecieve(req):
  msg = req.text
  msg = msg.split("|")
  for individual in msg:
    individual = individual.split(":")
    sender = individual[0]
    message = "".join(individual[1:])
    data.chatLog.append((message, sender))

def getMessages():
  GET_URL = "http://127.0.0.1:8080"
  req = ajax.ajax()
  req.bind('complete', onMessageRecieve)
  req.open('GET', GET_URL, True)
  req.send({"woooho":"woo"})

def onTimer(ticks):
  draw()
  getMessages()

def onKeyDown(key):
  if data.chatFocused:
    if key == "Backspace" and data.message:
      data.message = data.message[:-1]
    elif key != "Backspace" and key in "ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz1234567890":
      data.message += key
      data.cursorX += 15
    elif key == "Space":
      data.message += " "
    elif key == "Return" and data.message:
      if not data.name:
        data.name = data.message
        data.message = ""
      else:
        data.chatLog.insert(0, (data.message, data.name))
        if len(data.chatLog) > 9: data.chatLog.pop()
        POST_URL = "http://127.0.0.1:8080/"
        req = ajax.ajax()
        req.bind('complete', onMessageSend)
        req.open('POST', POST_URL, True)
        msg = {'sender': data.name, 'message': data.message}
        req.send(msg)
        data.message = ""
  draw()

def onMouseDown(x, y): pass

def onMouseMove(x, y): pass

def onMouseUp(x, y): pass

def onKeyUp(key): pass

def onResize(): pass

def onInit():
  data.name = ""
  data.width = browser.window.innerWidth
  data.height = browser.window.innerHeight
  data.hmargin = data.width / 5
  data.vmargin = data.height / 6
  data.chatSize = 50
  data.message = ""
  data.textVAlign = 15
  data.textHAlign = 10
  data.chatFocused = True
  data.cursorX = data.hmargin + data.textHAlign
  data.cursorUpY = data.height - data.vmargin - data.chatFocused
  data.cursorDownY = data.height - data.vmargin
  data.chatLog = [] # [("hello", "me"),("hows it going", "me"), ("I'm good, you?", "other"), ("thanks", "me")]
  data.lineSize = 40
  data.name = ""

def drawChatBackground():
  context.beginPath()
  context.rect(data.hmargin, data.vmargin, data.width - data.hmargin*2,
    data.height - data.vmargin*2)
  context.lineWidth = 2
  context.fillStyle = "#CCFFFF"
  context.fill()
  context.strokeStyle = "black"
  context.stroke()
  context.closePath()

def drawChatTypeArea():
  context.beginPath()
  context.rect(data.hmargin, data.height - data.vmargin - data.chatSize,
    data.width - data.hmargin*2, data.chatSize)
  context.lineWidth = 2
  context.fillStyle = "white"
  context.fill()
  context.stroke()
  context.closePath()

def drawChatText():
  context.fillStyle = "black"
  context.font = "30px courier"
  context.textAlign = "start"
  context.fillText(data.message, data.hmargin + data.textHAlign,
    data.height - data.vmargin - data.textVAlign)

def drawChatCursor():
  context.beginPath()
  context.lineWidth = 4
  context.fillStyle = "black"
  context.moveTo(data.cursorX, data.cursorUpY)
  context.lineTo(data.cursorX, data.cursorDownY)
  context.stroke()
  context.closePath()

def drawMessages():
  currLine = data.height - data.vmargin - data.chatSize - 20
  for i in range(len(data.chatLog)):
    message = data.chatLog[i]
    if message[1] == data.name:
      context.textAlign = "end"
      context.fillText(message[0], data.width - data.hmargin - data.textHAlign, currLine)
      currLine -= data.lineSize
    else:
      context.textAlign = "start"
      context.fillText(message[0], data.hmargin + data.textHAlign, currLine)
      currLine -= data.lineSize


def draw():
  drawChatBackground()
  drawChatTypeArea()
  drawChatCursor()
  drawChatText()
  drawMessages()

##################################################################
# Do Not Edit Code Below Here
##################################################################

import browser #from browser import alert, confirm, document, prompt, timer, window
import sys
import javascript

print("sys.path =", sys.path)
SCRIPT_PATH = sys.path[0]


# Use jsmath.random (since "import random" is not working very well)
jsmath = javascript.JSObject(browser.window["Math"])
random = jsmath.random
def randomChoice(a):
  return a[int(jsmath.random()*len(a)) % len(a)]

# image support
def loadImage(imageURL):
  img = browser.document.createElement('img')
  img.src = SCRIPT_PATH + "/" + imageURL
  return img

# There should be a better way to play audio,
# but access to browser.window["Audio"] not working right
def loadAudio(audioURL):
  audio = browser.document.createElement('audio')
  audio.src = SCRIPT_PATH + "/" + audioURL
  return audio

# Deal with active/inactive window/tab
WIN_IS_ACTIVE = True
def winIsActive():
  return WIN_IS_ACTIVE
def setWinIsActive(winIsActive):
  global WIN_IS_ACTIVE
  WIN_IS_ACTIVE = winIsActive
  # print("winIsActive =", winIsActive)
browser.document.onfocusin = browser.window.onfocus = (lambda *args: setWinIsActive(True))
browser.document.onfocusout = browser.window.onblur = (lambda *args: setWinIsActive(False))

LAST_EVENT = None
console = None

def writeToConsole(data, color="black"):
  if (console == None):
    print(data)
  else:
    text = str(data).replace("&", "&amp;").replace('"', "&quot;").replace("<", "&lt;").replace(">", "&gt;")
    text = '<font color="%s">%s</font>' % (color, text)
    console.innerHTML += "%s<br>" % text
    console.scrollTop = console.scrollHeight

def raw_input(prompt="Enter a value"):
  result = browser.prompt(prompt)
  writeToConsole("%s --> %s" % (prompt, result), "blue")
  return result

def input(prompt="Enter a value"):
  return eval(raw_input(prompt))

def initConsole(consoleId):
  if (consoleId != None):
    global console
    console = browser.document[consoleId]
    def writeErrToConsole(data): writeToConsole(data, "red")
    sys.stdout.write = writeToConsole
    sys.stderr.write = writeErrToConsole

KEY_CODE_NAMES = { 3:"Cancel", 6:"Help", 8:"Backspace", 9:"Tab", 12:"Clear", 13:"Return",
           14:"Enter", 16:"Shift", 17:"Control", 18:"Alt", 19:"Pause", 20:"CapsLock",
           27:"Escape", 32:"Space", 33:"PageUp", 34:"PageDown", 35:"End", 36:"Home",
           37:"Left", 38:"Up", 39:"Right", 40:"Down", 44:"PrintScreen", 45:"Insert",
           46:"Delete", 112:"F1", 113:"F2", 114:"F3", 115:"F4", 116:"F5", 117:"F6",
           118:"F7", 119:"F8", 120:"F9", 121:"F10", 122:"F11", 123:"F12",
           144:"NumLock", 145:"ScrollLock", 224:"Meta"
         }

def getLastEvent():
  return LAST_EVENT

def getKey(event):
  LAST_EVENT = event
  key = None
  if (event.type == "keypress"):
    if (event.ctrlKey or (0 < event.charCode < 27)):
      # It's a ctrl key, return something like "ctrl-a" or "ctrl-A"
      baseKey = "A" if event.shiftKey else "a"
      # On some browsers, charCode is <27, on others, it's not
      key = "ctrl-" + chr(ord(baseKey) + (event.charCode % 32) - 1)
    else:
      key = chr(event.charCode)
  else:
    key = KEY_CODE_NAMES.get(event.keyCode)
  return key

def getMouseXY(event):
  LAST_EVENT = event
  rect = canvas.getBoundingClientRect()
  return (event.clientX - rect.left, event.clientY - rect.top)

def run(timerDelay=2000, canvasId="brythonCanvas", consoleId=None, globalFocus=False):
  global canvas, context, data
  canvas = browser.document[canvasId]
  canvas.style.width ='100%'
  canvas.style.height='100%'
  def onResizeWrapper(event=None):
    canvas.width  = canvas.offsetWidth
    canvas.height = canvas.offsetHeight
    if (event): onResize()
  browser.window.addEventListener('resize', onResizeWrapper, False)
  onResizeWrapper()
  context = canvas.getContext('2d')
  class Struct(): pass
  data = Struct()
  data.timerTicks = 0
  data.timerDelay = timerDelay
  data.timerPaused = False
  data.timerPauseKey = "ctrl-p"
  data.timerStepKey = "ctrl-s"
  initConsole(consoleId)
  onInit()
  canvas.bind("mousedown", lambda event: onMouseDown(*getMouseXY(event)))
  canvas.bind("mousemove", lambda event: onMouseMove(*getMouseXY(event)))
  canvas.bind("mouseup",   lambda event: onMouseUp(*getMouseXY(event)))
  def doTick():
    # if (winIsActive() == False): return
    data.timerTicks += 1
    onTimer(data.timerTicks)
  def dispatchKeyEvent(event):
    if (winIsActive() == False): return
    key = getKey(event)
    if ((key == None) and (event.type != "keyup")): return
    event.preventDefault()
    if (event.type == "keypress"):
      if (key == data.timerPauseKey):
        data.timerPaused = not data.timerPaused
      elif (key == data.timerStepKey):
        doTick()
      onKeyDown(key)
    elif (event.type == "keydown"):
      onKeyDown(key)
    elif (event.type == "keyup"):
      onKeyUp(key)
  if (globalFocus):
    keySink = browser.document
  else:
    keySink = canvas
    canvas.setAttribute('tabindex','0')
    canvas.setAttribute('outline','none')
    canvas.focus()
  keySink.bind("keypress", dispatchKeyEvent)
  keySink.bind("keydown", dispatchKeyEvent)
  keySink.bind("keyup", dispatchKeyEvent)
  def timerWrapper():
    if (not data.timerPaused):
      doTick()
    browser.window.setTimeout(timerWrapper, data.timerDelay)
    # browser.timer.request_animation_frame(animate)
  timerWrapper()

run(globalFocus=True)