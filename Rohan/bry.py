
# blob-catch.py
# A very simple demo of a Brython browser-based game
# By David Kosbie

import math, browser, time

# from browser import ajax
# def on_complete(req):
#     print(req)


# url = "http://www.kritikalstats.com/1/tournament/"
# req = ajax.ajax()
# req.bind('complete',on_complete)
# req.open('GET',url,True)
# # req.set_header('content-type','application/x-www-form-urlencoded')
# req.send()

class Blob(object):
  def __init__(self, x=None, y=None):
    a = ["CMU", "Carnegie", "Mellon", "Python",
       "Lists", "Loops", "Recursion", "Classes", "Graphics", "Algorithms",
       "Strings", "Functions", "Fractals"]
    self.text = "15-112" if (random()<0.5) else randomChoice(a) 
    fontHeight = int(10+random()*30)
    self.fillStyle = randomChoice(["red", "yellow", "green", "blue"])
    self.font = context.font = str(fontHeight) + "px Arial"
    self.width = 2 * context.measureText(self.text).width
    self.height = fontHeight * 1.5
    def randomx(): return jsmath.random()*(canvas.width - self.width)
    # now set the direction, by choosing the exit point
    if (y != None):
      (x1, y1) = (x - self.width/2, y - self.height/2)
    else:
      (x1, y1) = (randomx(), 0)
    (x2, y2) = (randomx(), canvas.height)
    d = ((x2 - x1)**2 + (y2 - y1)**2)**0.5
    speed = 5 + random()*15
    (self.dx, self.dy) = (speed/d * (x2 - x1), speed/d * (y2 - y1))
    (self.x, self.y) = (x1, y1)
    self.isEaten = False

def rectanglesIntersect(ax0, ay0, ax1, ay1,
            bx0, by0, bx1, by1):
  return ((ax0 < bx1) and (ax1 > bx0) and
      (ay0 < by1) and (ay1 > by0))

def changeScore(dscore):
  data.score = max(0, data.score + dscore)
  sound = None
  if (dscore > 0):
    sound = data.goodSound
  elif (dscore == data.eatRedPenalty):
    sound = data.badSound
  if (sound and not data.soundPaused):
    sound.play()

def checkForNewScores():
  (px0, py0) = (data.playerX, data.playerY)
  (px1, py1) = (px0 + data.playerWidth, py0 + data.playerHeight)
  for blob in data.blobs:
    if (blob.isEaten == False):
      (bx0, by0) = (blob.x, blob.y)
      (bx1, by1) = (bx0 + blob.width, by0 + blob.height)
      if (rectanglesIntersect(px0, py0, px1, py1, bx0, by0, bx1, by1)):
        # wahoo, we ate one
        blob.isEaten = True
        if (blob.fillStyle == "red"):
          # well, not wahoo, we ate a red one...
          changeScore(data.eatRedPenalty)
          blob.fillStyle = "black"
        else:
          changeScore(data.eatNonRedScore)
          blob.fillStyle = "lightGray"

def onTimer(ticks):
  # check if sound should be paused
  elapsedTime = time.time() - data.lastKeyOrMouseEventTime
  data.soundPaused = (elapsedTime > data.soundInactivityTimeout)
  # descend blobs
  deadBlobs = [ ]
  for blob in data.blobs:
    blob.x += blob.dx
    blob.y += blob.dy
    if ((blob.x > canvas.width) or (blob.y > canvas.height)):
      deadBlobs.append(blob)
      if ((blob.isEaten == False) and (blob.fillStyle != "red")):
        changeScore(data.missedBlobPenalty)
  # check for new scores
  checkForNewScores()
  # remove blobs past the bottom
  for blob in deadBlobs:
    data.blobs.remove(blob)
  # add new blob if it's time
  data.ticksToNextBlob -= 1
  if (data.ticksToNextBlob <= 0):
    data.ticksToNextBlob = data.ticksBetweenBlobs
    data.blobs.append(Blob())
  draw()

def onKeyDown(key):
  data.lastKeyOrMouseEventTime = time.time()
  if (key == "Left"):
    data.playerX = max(0, data.playerX - data.playerSpeed)
  elif (key == "Right"):
    data.playerX = min(canvas.width - data.playerWidth,
               data.playerX + data.playerSpeed)
  checkForNewScores()
  draw()

def onMouseDown(x, y):
  data.lastKeyOrMouseEventTime = time.time()
  data.blobs.append(Blob(x, y))
  draw()

def onMouseMove(x, y): pass
def onMouseUp(x, y): pass
def onKeyUp(key): pass
def onResize(): pass

def onInit():
  data.lastKeyOrMouseEventTime = time.time()
  data.score = 0
  data.ticksBetweenBlobs = 5
  data.ticksToNextBlob = data.ticksBetweenBlobs
  data.blobs = [ Blob() ]
  data.playerWidth = 48
  data.playerHeight = 48
  data.playerY = canvas.height - data.playerHeight - 10
  data.playerX = canvas.width/2 - data.playerWidth/2
  data.playerSpeed = 20
  data.eatNonRedScore = 10
  data.missedBlobPenalty = -1
  data.eatRedPenalty = -50
  data.soundInactivityTimeout = 5 # seconds
  data.soundPaused = False
  # from: https://www.iconfinder.com/icons/66960/sumi_icon#size=48
  data.pi = loadImage("1409624199_sumi.png", 100, 100)
  # from: http://soundbible.com/1669-Robot-Blip-2.html
  data.goodSound = loadAudio('Robot_blip_2-Marianne_Gagnon-299056732.mp3')
  # from: http://soundbible.com/121-Computer-Error.html
  data.badSound = loadAudio('Computer Error-SoundBible.com-69768060.mp3')
  draw()

def fillEllipse(x, y, w, h):
  (cx, cy) = (x+w/2, y+h/2)
  (x0, y0, x1, y1) = (x, y, x+w, y+h)
  context.beginPath();
  context.moveTo(cx, y0)
  context.bezierCurveTo(x1, y0, x1, y1, cx, y1)
  context.bezierCurveTo(x0, y1, x0, y0, cx, y0) 
  context.fill();
  context.closePath();

def draw():
  context.clearRect(0, 0, canvas.width, canvas.height) # clear the canvas
  drawBlobs()
  drawPlayer()
  drawText()

def drawBlobs():
  context.textAlign = 'center'   # center horizontally
  context.textBaseline = 'middle'  # center vertically
  for blob in data.blobs:
    if (blob.isEaten == True):
      context.fillStyle = blob.fillStyle
    else:
      (cx, cy) = (blob.x + blob.width/2, blob.y + blob.height/2)
      gradient = context.createRadialGradient(cx, cy, 3, cx, cy, 0.75*max(blob.width, blob.height))
      gradient.addColorStop(1, blob.fillStyle)
      gradient.addColorStop(0, 'white')
      context.fillStyle = gradient
    fillEllipse(blob.x, blob.y, blob.width, blob.height)
    # now the text
    context.font = blob.font
    context.fillStyle = "black"
    (cx, cy) = (blob.x + blob.width/2, blob.y + blob.height/2)
    context.fillText(blob.text, cx, cy)

def drawPlayer():
  #context.fillStyle = "purple"
  #context.fillRect(data.playerX, data.playerY, data.playerWidth, data.playerHeight)
  context.drawImage(data.pi.image, data.playerX, data.playerY, data.pi.width, data.pi.height)

def drawText():
  # the directions and the score and such
  context.fillStyle = "purple"
  context.textAlign = 'right'
  context.textBaseline = 'top'
  context.font = "12px Arial"
  context.fillText("Use left/right arrows to catch blobs!", canvas.width, 0)
  context.fillText("Missed blobs lose points!", canvas.width, 15)
  context.fillText("And don't catch red blobs!", canvas.width, 30)
  context.fillText("ctrl-p pauses and ctrl-s steps, for superhero play!", canvas.width, 45)
  context.font = "20px Arial"
  context.fillText("Score: " + str(data.score), canvas.width, 60)
  context.textAlign = 'left'
  context.fillText("Blob Catch: A simple Python game!", 0, 0)
  context.font = "12px Arial"
  context.fillText("Well, Brython, a flavor of Python for browsers.  Sweet!", 0, 22)  
  context.fillText("Try 'view page source' to check out the code!", 0, 37)
  context.fillText("Soon, you'll make games like this, only much better!", 0, 52)
  if (data.timerPaused):
    context.fillStyle = "blue"
    context.textAlign = 'center'
    context.textBaseline = 'middle'
    context.font = "48px Arial"
    context.fillText("Paused!", canvas.width/2, canvas.height/2)
    context.font = "14px Arial"
    context.fillText(data.timerPauseKey + " to un-pause",
             canvas.width/2, canvas.height/2 + 30)
  if (data.soundPaused):
    context.fillStyle = "red"
    context.textAlign = 'right'
    context.textBaseline = 'bottom'
    context.font = "14px Arial"
    context.fillText("Sound muted due to inactivity", canvas.width, canvas.height)

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

class ImageObject(object):
  def __init__(self, url, width, height):
    self.imgSrc = url
    self.image = browser.document.createElement('img')
    self.image.src = SCRIPT_PATH + "/" + url
    self.width = width
    self.height = height


# image support
def loadImage(imageURL, width, height):
  img = ImageObject(imageURL, width, height)
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
    if (winIsActive() == False): return
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