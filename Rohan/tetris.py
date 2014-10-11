
# blob-catch.py
# A very simple demo of a Brython browser-based game
# By David Kosbie

import math, browser, time, javascript

# Use jsmath.random (since "import random" is not working very well)
jsmath = javascript.JSObject(browser.window["Math"])
random = jsmath.random

def placeCurrPiece():
  for prow in range(len(data.pieces[data.currPiece])):
    for pcol in range(len(data.pieces[data.currPiece][0])):
      row = prow + data.fallingPieceY
      col = pcol + data.fallingPieceX
      if data.pieces[data.currPiece][prow][pcol]:
        data.board[row][col] = data.currPiece

def collidedWithPiece(row):
  for pcol in range(len(data.pieces[data.currPiece][0])):
    col = data.fallingPieceX + pcol
    if data.board[row][col] >= 0:
      return True
  return False

def pieceCollided():
  curPieceBottom = data.fallingPieceY + len(data.pieces[data.currPiece])
  if curPieceBottom == data.rows or collidedWithPiece(curPieceBottom):
    placeCurrPiece()
    newCurrPiece()

def getCurrPos(pos):
  xyz = pos.coords
  data.loc = "Your position: %f,%f" % (xyz.latitude, xyz.longitude)

def recordOrientation(eventData):
  tiltLR = eventData.gamma
  tiltFB = eventData.beta
  theDir = eventData.alpha
  data.stuff = "%f, %f, %f" % (tiltLR, tiltFB, theDir)

def onTimer(ticks):
  if ticks % 2 == 0:
    data.fallingPieceY += 1
  pieceCollided()
  browser.window.navigator.geolocation.getCurrentPosition(getCurrPos)
  if (browser.window.DeviceOrientationEvent):
    # pass
    browser.window.addEventListener('deviceorientation', recordOrientation, false)
  else:
    print("not supported")
  draw()

def onKeyDown(key):
  if key == "Left":
    data.fallingPieceX -= 1
  elif key == "Right":
    data.fallingPieceX += 1
  elif key == "Down":
    data.fallingPieceY += 1

def onMouseDown(x, y): pass
def onMouseMove(x, y): pass
def onMouseUp(x, y): pass
def onKeyUp(key): pass
def onResize(): pass

def initializeBoard(rows, cols):
  board = [ ([-1]) * cols for i in range(rows)]
  return board

def initializePieces():
  data.pieces = [
    [ [1, 1, 0],
      [0, 1, 1]
    ],
    [ [0, 1, 0],
      [1, 1, 1]
    ],
    [ [1, 0, 0],
      [1, 1, 1]
    ],
    [ [0, 0, 1],
      [1, 1, 1]
    ],
    [ [1, 1],
      [1, 1]
    ],
    [ [1, 1, 1, 1] ]
  ]

def getRandomPiece():
  return int(jsmath.random() * 1000) % 6

def newCurrPiece():
  data.currPiece = getRandomPiece()
  data.fallingPieceX = data.cols // 2 - 1
  data.fallingPieceY = 0

def onInit():
  data.w = browser.window.innerWidth
  data.h = browser.window.innerHeight
  data.blockHeight = min(data.h / 15, data.w / 10)
  data.blockWidth = data.blockHeight
  data.topMargin = data.h - data.blockHeight * 15 - 5 
  data.rows = 15
  data.cols = 10
  data.boardHeight = data.blockHeight * data.rows
  data.boardWidth = data.blockWidth * data.cols
  data.leftMargin = (canvas.width - data.boardWidth) / 2
  data.board = initializeBoard(data.rows, data.cols)
  data.loc = ""
  data.stuff = ""
  data.colors = {
    -1: "white",
    0: "purple",
    1: "blue",
    2: "rgb(255,0,0)",
    3: "rgb(0,255,0)",
    4: "orange",
    5: "yellow",
  }
  initializePieces()
  newCurrPiece()


def drawBoard():
  context.fillStyle = "white"
  context.fillRect(data.leftMargin, data.topMargin, data.boardWidth,
    data.boardHeight)
  for row in range(data.rows):
    for col in range(data.cols):
      top = data.topMargin + row * data.blockHeight
      left = data.leftMargin + col * data.blockWidth
      upperboardY = data.fallingPieceY + len(data.pieces[data.currPiece])
      upperboardX = data.fallingPieceX + len(data.pieces[data.currPiece][0])
      if (data.fallingPieceY <= row < upperboardY and 
          data.fallingPieceX <= col < upperboardX):
        if data.pieces[data.currPiece][row - data.fallingPieceY][col - data.fallingPieceX]:
          context.fillStyle = data.colors[data.currPiece]
      else:
        context.fillStyle = data.colors[data.board[row][col]]
      context.beginPath()
      context.rect(left, top, data.blockWidth, data.blockHeight)
      context.fill()
      context.strokeStyle = "black"
      context.stroke()
      context.closePath()
  context.fillStyle = "purple"
  context.fillText(data.loc, canvas.width/2, 100)
  context.fillText(data.stuff, canvas.width/2, 200)

def draw():
  context.clearRect(0, 0, canvas.width, canvas.height) # clear the canvas
  context.fillStyle = "black"
  context.fillRect(0,0,canvas.width,canvas.height)
  drawBoard()

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