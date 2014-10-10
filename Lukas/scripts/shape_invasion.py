from drawObjects import *
import struct

def onTimer(ticks):
    if data.playing:
        for shape in data.fallingShapes:
            shape.y += 3
        if checkForWin(): win()
        elif checkForLoss(): lose()
    draw()

def onKeyDown(key):
    if key == 'r': onInit()
    elif key == 'b': assert False

def onMouseDown(x, y):
    if data.playing:
        for i, shape in enumerate(data.shapes):
            if shape.intersects(x, y):
                if data.selected == None:
                    data.selected = i
                elif shape == data.shapes[data.selected]:
                    data.selected = None
                else:
                    swapShapes(shape, data.shapes[data.selected], data.shapes)
                    data.shapes[data.selected].selected = False
                    data.selected = None

def onMouseMove(x, y): pass
def onMouseUp(x, y):
    writeToConsole(data.image.width)
 #draw()
def onKeyUp(key): print(key)
def onResize(): pass

def checkForWin():
    for i in range(len(data.shapes)):
        if data.fallingShapes[i].n != data.shapes[i].n:
            #writeToConsole((i, data.fallingShapes[i].n, data.shapes[i].n))
            return False
    return True

def win():
    data.playing = False
    data.won = True

def checkForLoss():
    return data.fallingShapes[0].y >= data.shapes[0].y

def lose():
    data.playing = False

def draw():
    context.clearRect(0, 0, canvas.width, canvas.height)
    context.fillStyle = "#00FF00"
    x, y = 100, 50
    drawShapes()
    context.drawImage(data.image, 0, 0)
    if not data.playing:
        drawGameOverText()

def drawGameOverText():
    context.font = "30px Arial"
    context.textAlign = "center"
    text = ("You %s Press 'r' to play again." %
            ("win!" if data.won else "lose :("))
    context.fillStyle = "#000000"
    context.strokeStyle = "#000000"
    context.fillText(text, canvas.width/2, canvas.height/2)
    #writeToConsole(context.measureText(text).height)

def drawShapes():
    for shape in data.shapes:
        shape.draw()
    for shape in data.fallingShapes:
        shape.draw()

def initFallingShapes():
    data.fallingShapes = initShapes()
    for shape in data.fallingShapes:
        shape.y = 0
    shuffleShapes(data.fallingShapes)

def shuffleShapes(a):
    for _ in range(10):
        shape1 = randomChoice(a)
        shape2 = randomChoice(a)
        swapShapes(shape1, shape2, a)

def initShapes():
    y = canvas.height * 9 / 10
    margin = 25
    separation = 15
    shapeCount = 5
    shapeWidth = ((canvas.width -
                  (2 * margin + (shapeCount - 1) * separation))
                  / shapeCount)
    r = shapeWidth / 2
    sx = margin + r
    ns = [3, 4, 5, 6, 8]
    colors = ["#0000FF", "#00FF00", "#FFFF00", "#FF0000", "#8000FF"]
    pi = jsmath.PI
    angles = [pi/2, pi/4, pi/2, 0, pi/8]
    shapes = []
    csep = separation + shapeWidth
    for i in range(shapeCount):
        x = sx + (csep * i)
        n = ns[i]
        color = colors[i]
        newShape = Shape(x, y, r, n, color, angles[i])
        shapes.append(newShape)
    return shapes

def onInit():
    with open("file.txt") as f:
        writeToConsole(f.read())
    data.won = False
    data.playing = True
    data.selected = None
    data.shapes = initShapes()
    data.image = loadImage("imgs/megaman.png")
    initFallingShapes()

class Shape(object):
    def __repr__(self):
        return "%d" % self.n

    def __init__(self, x, y, r, sides, color, start=0):
        self.x, self.y = x, y
        self.r = r
        self.n = sides
        self.color = color
        self.startAngle = start

    def draw(self):
        selected = (data.selected != None and
                    data.shapes[data.selected] == self)
        drawPolygon(self.x, self.y, self.r,
                    self.n, self.startAngle, self.color, selected)

    def intersects(self, x, y):
        distance = ((x - self.x)**2 + (y - self.y)**2)**0.5
        return distance < self.r

def swapShapes(shape1, shape2, a):
    shape1.x, shape2.x = shape2.x, shape1.x
    shape1.y, shape2.y = shape2.y, shape1.y
    shape1i = a.index(shape1)
    shape2i = a.index(shape2)
    a[shape1i] = shape2
    a[shape2i] = shape1
    
def drawPolygon(cx, cy, r, n, startAngle, fillStyle, goldStroke=False):
    stroke = "#FFAA00" if goldStroke else "#000000"
    create_ngon(context, n, cx, cy, r, fill=fillStyle, outline=stroke, width=4)
    # circle = 2*jsmath.PI
    # innerAngle = circle / n
    # pts = []
    # for point in range(n):
    #     angle = startAngle + innerAngle*point
    #     x, y = cx + r*jsmath.cos(angle), cy - r*jsmath.sin(angle)
    #     pts.append((x, y))
    # context.fillStyle = fillStyle
    # context.strokeStyle = stroke
    # context.beginPath()
    # context.moveTo(pts[0][0], pts[0][1])
    # for pt in pts[1:]:
    #     context.lineTo(pt[0], pt[1])
    # context.fill()
    # context.closePath()
    # context.stroke()

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
    img.src = imageURL
    writeToConsole("(%d, %d)" % (img.width, img.height))
    print(img.html)
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

run(timerDelay=10, canvasId="brythonCanvas", consoleId=None, globalFocus=True)