
# blob-catch.py
# A very simple demo of a Brython browser-based game
# By David Kosbie

import math, browser, time, javascript

# Use jsmath.random (since "import random" is not working very well)
jsmath = javascript.JSObject(browser.window["Math"])
random = jsmath.random

def onTimer(ticks):
  draw()

def onKeyDown(key):
  try:
    data.currNumber = int(key)
  except:
    if key == "Up":
      data.selectRow = (data.selectRow - 1) % data.rows
    elif key == "Down":
      data.selectRow = (data.selectRow + 1) % data.rows
    elif key == "Right":
      data.selectCol = (data.selectCol + 1) % data.cols
    elif key == "Left":
      data.selectCol = (data.selectCol - 1) % data.cols
    elif key == "Return":
      if not data.board[data.selectRow][data.selectCol][1]:
        data.board[data.selectRow][data.selectCol] = [data.currNumber, True]

def onMouseDown(x, y): pass

def onMouseMove(x, y): pass

def onMouseUp(x, y):
  x,y = x - data.xMargin, y - data.yMargin
  row, col= int(y //data.boxH), int(x //data.boxW)
  if row >= 0 and row < data.rows and col >=0 and col < data.cols:
    if not data.board[row][col][1]:
      data.board[row][col] = [data.currNumber, False]
    data.selectRow, data.selectCol = row, col

def onKeyUp(key): pass

def onResize(): pass

def onInit():
  data.board = [[[0, False],
  [8, True],
  [0, False],
  [9, True],
  [1, True],
  [0, False],
  [5, True],
  [4, True],
  [0, False]],
 [[0, False],
  [5, True],
  [0, False],
  [0, False],
  [0, False],
  [4, True],
  [6, True],
  [0, False],
  [3, True]],
 [[7, True],
  [0, False],
  [0, False],
  [0, False],
  [0, False],
  [5, True],
  [1, True],
  [0, False],
  [0, False]],
 [[0, False],
  [0, False],
  [6, True],
  [0, False],
  [3, True],
  [0, False],
  [0, False],
  [5, True],
  [9, True]],
 [[3, True],
  [0, False],
  [0, False],
  [7, True],
  [0, False],
  [6, True],
  [0, False],
  [0, False],
  [2, True]],
 [[4, True],
  [7, True],
  [0, False],
  [0, False],
  [2, True],
  [0, False],
  [8, True],
  [0, False],
  [0, False]],
 [[0, False],
  [0, False],
  [9, True],
  [3, True],
  [0, False],
  [0, False],
  [0, False],
  [0, False],
  [4, True]],
 [[1, True],
  [0, False],
  [7, True],
  [6, True],
  [0, False],
  [0, False],
  [0, False],
  [8, True],
  [0, False]],
 [[0, False],
  [2, True],
  [4, True],
  [0, False],
  [9, True],
  [7, True],
  [0, False],
  [6, True],
  [0, False]]]
  data.w = browser.window.innerWidth
  data.h = browser.window.innerHeight
  data.boxW = data.boxH = min((data.w - 100)/9.0, (data.h-100)/9.0)
  data.rows, data.cols = len(data.board), len(data.board[0])
  data.boardW = data.boardH = data.rows * data.boxH
  data.xMargin = (data.w - (data.cols * data.boxW))/2
  data.yMargin = (data.h - (data.rows * data.boxH))/2
  data.currNumber = 1
  data.currNumX = data.xMargin/2
  data.currNumY = data.h/2
  data.currNumText = "Currently Selected Number:"
  data.selectRow = 0
  data.selectCol = 0

def drawBoard():
  context.beginPath()
  context.strokeStyle = "black"
  context.font = "30px Arial"
  context.lineWidth = 2
  for row in range(data.rows):
    for col in range(data.cols):
      top = data.yMargin + row * data.boxH
      left = data.xMargin + col * data.boxW
      context.rect(left,top,data.boxW,data.boxH)
      textx, texty = top + data.boxH/2, left + data.boxW/2
      if data.board[row][col][0] != 0:
        context.fillText(str(data.board[row][col][0]), texty,textx)
  context.stroke()
  context.closePath()

def drawBoardLines():
  context.beginPath()
  context.strokeStyle = "black"
  context.lineWidth = 4
  for i in range(4):
    upx = data.xMargin + i * 3 * data.boxW
    sidey = data.yMargin + i * 3 * data.boxH
    context.moveTo(upx, data.yMargin)
    context.lineTo(upx, data.yMargin + data.boardH)
    context.moveTo(data.xMargin, sidey)
    context.lineTo(data.xMargin + data.boardW, sidey)
    context.stroke()
  context.closePath()

def drawCurrNum():
  context.fillText(str(data.currNumber), data.currNumX, data.currNumY)
  context.font = "20px Arial"
  context.fillText(data.currNumText, data.currNumX, data.currNumY - data.boxH)
  context.beginPath()
  context.strokeStyle = "black"
  context.rect(data.currNumX - data.boxW/2, data.currNumY - data.boxH/2,
    data.boxW, data.boxH)
  context.stroke()
  context.closePath()

def drawSelectedBox():
  context.beginPath()
  context.strokeStyle = "red"
  context.lineWidth = 5
  x = data.selectCol * data.boxW + data.xMargin
  y = data.selectRow * data.boxH + data.yMargin
  context.rect(x,y,data.boxW, data.boxH)
  context.stroke()
  context.closePath()

def draw():
  context.textAlign = "center"
  context.clearRect(0, 0, canvas.width, canvas.height)
  drawBoard()
  drawBoardLines()
  drawCurrNum()
  drawSelectedBox()
  


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

def run(timerDelay=100, canvasId="brythonCanvas", consoleId=None, globalFocus=False):
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