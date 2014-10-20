import browser
import math
import javascript

#import random
jsmath = javascript.JSObject(browser.window["Math"])
random = jsmath.random
def __randomChoice(a):
    return a[int(jsmath.random()*len(a)) % len(a)]
random.choice = __randomChoice

def __randint(low, hi):
    return random.choice(range(low, hi))
random.randint = __randint


class Vector(object):
    def __init__(self, i, j):
        self.i, self.j = i, j

    def __add__(self, other):
        return Vector(self.i + other.i, self.j + other.j)


class Ball(object):
    def __init__(self, x, y):
        self.x, self.y = x, y
        self.r = 15
        self.velocity = Vector(0, 0)
        self.bounceVelocity = Vector(0, -5)
        self.img = javascript.JSConstructor(Image)()
        self.img.src = 'ball.png'
        self.audioSrc = 'bounce.mp3'

    def olddraw(self, context, screenTop):
        context.beginPath()
        context.arc(self.x, self.y - screenTop, self.r, 0, 2*math.pi, False)
        context.fillStyle = "black"
        context.fill()
        context.closePath()

    def draw(self, context, screenTop):
        context.drawImage(self.img, self.x-self.r, self.y-self.r - screenTop,
                          2*self.r, 2*self.r)

    def update(self, accel):
        self.velocity += accel
        self.x += self.velocity.i
        self.y += self.velocity.j

    def bounce(self):
        self.velocity = self.bounceVelocity + Vector(self.velocity.i, 0)
        if hasattr(browser.window.navigator, 'vibrate'):
            browser.window.navigator.vibrate(50)
        javascript.JSConstructor(Audio)(self.audioSrc).play()

    def bounceOnWall(self, wall):
        return (self.velocity.j > 0 and
                wall.x0 < self.x < wall.x1 and
                self.y < wall.y < self.y + self.r)

class Wall(object):
    def __init__(self, x0, width, y):
        self.x0, self.x1, self.y = x0, x0 + width, y

    def draw(self, context, screenTop):
        context.beginPath()
        context.moveTo(self.x0, self.y - screenTop)
        context.lineTo(self.x1, self.y - screenTop)
        context.stroke()


canvas = browser.document['canvas']
canvas.style.width = '100%'
canvas.style.maxWidth = '400px'
canvas.style.height = '100%'
canvas.style.maxHeight = '400px'

def onResize(event=None):
    canvas.width = canvas.offsetWidth
    canvas.height = canvas.offsetHeight

browser.window.addEventListener('resize', onResize, False)
onResize()

context = canvas.getContext('2d')

gravity = Vector(0, 0.1)
gamma = 0


screenTop = 0
scrollBoundary = canvas.height / 3

ball = Ball(100, 100)
wallCount = 7
walls = set(Wall(random.randint(0, canvas.width-50), 50, random.randint(0, canvas.height))
         for _ in range(wallCount))


KEY_CODE_NAMES = {
    3:"Cancel", 6:"Help", 8:"Backspace", 9:"Tab", 12:"Clear", 13:"Return",
    14:"Enter", 16:"Shift", 17:"Control", 18:"Alt", 19:"Pause", 20:"CapsLock",
    27:"Escape", 32:"Space", 33:"PageUp", 34:"PageDown", 35:"End", 36:"Home",
    37:"Left", 38:"Up", 39:"Right", 40:"Down", 44:"PrintScreen", 45:"Insert",
    46:"Delete", 112:"F1", 113:"F2", 114:"F3", 115:"F4", 116:"F5", 117:"F6",
    118:"F7", 119:"F8", 120:"F9", 121:"F10", 122:"F11", 123:"F12",
    144:"NumLock", 145:"ScrollLock", 224:"Meta"
}


def getKey(event):
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

keys = [False, False]

def onKeyDown(event):
    key = getKey(event)
    if key == "Right":
        keys[1] = True
    elif key == "Left":
        keys[0] = True

def onKeyUp(event):
    key = getKey(event)
    if key == "Right":
        keys[1] = False
    elif key == "Left":
        keys[0] = False

browser.document.bind('keydown', onKeyDown)
browser.document.bind('keyup', onKeyUp)


def onOrientation(event):
    global gamma
    gamma = event.gamma
browser.window.addEventListener('deviceorientation', onOrientation)

def loop(timestamp):
    global screenTop
    context.clearRect(0, 0, canvas.width, canvas.height)
    netAccel = gravity
    if keys[0]:
        netAccel += Vector(-0.1, 0)
    elif keys[1]:
        netAccel += Vector(0.1, 0)
    elif gamma:
        netAccel += Vector(0.1 * gamma / 20, 0)

    ball.update(netAccel)
    if ball.y - screenTop < scrollBoundary:
        screenTop = int(ball.y - scrollBoundary)

    for wall in walls:
        if wall.y - screenTop > canvas.height:
            walls.remove(wall)
            walls.add(Wall(random.randint(0, canvas.width), 50, random.randint(scrollBoundary/3 + screenTop, ball.y)))
        wall.draw(context, screenTop)
        if ball.bounceOnWall(wall):
            ball.bounce()
    
    ball.x %= canvas.width
    if ball.y - screenTop > canvas.height:
        return

    ball.draw(context, screenTop)

    browser.window.requestAnimationFrame(loop)

browser.window.requestAnimationFrame(loop)
