import browser, sys, javascript
import browser.timer
from contextWrapper import ContextWrapper

class Struct(): pass

def raw_input(prompt="Enter a value"):
    return browser.prompt(prompt)

def input(prompt="Enter a value"):
    return eval(raw_input(prompt))

KEY_CODE_NAMES = {3:"Cancel", 6:"Help", 8:"Backspace", 9:"Tab", 12:"Clear",
                  13:"Return", 14:"Enter", 16:"Shift", 17:"Control", 18:"Alt",
                  19:"Pause", 20:"CapsLock", 27:"Escape", 32:"Space",
                  33:"PageUp", 34:"PageDown", 35:"End", 36:"Home", 37:"Left",
                  38:"Up", 39:"Right", 40:"Down", 44:"PrintScreen", 45:"Insert",
                  46:"Delete", 112:"F1", 113:"F2", 114:"F3", 115:"F4", 116:"F5",
                  117:"F6", 118:"F7", 119:"F8", 120:"F9", 121:"F10", 122:"F11",
                  123:"F12", 144:"NumLock", 145:"ScrollLock", 224:"Meta"
                 }

def _is_char(keycode):
    if (ord('A') <= keycode <= ord('Z')): return True
    elif (ord('0') <= keycode <= ord('9')): return True
    elif (186 <= keycode <= 192): return True
    elif (219 <= keycode <= 222): return True
    else: return False

CHARS = {(0x30, True): ')',
         (0x31, True): '!',
         (0x32, True): '@',
         (0x33, True): '#',
         (0x34, True): '$',
         (0x35, True): '%',
         (0x36, True): '^',
         (0x37, True): '&',
         (0x38, True): '*',
         (0x39, True): '(',
         (0xba, False): ';', (0xba, True): ':',
         (0xbb, False): '=', (0xbb, True): '+',
         (0xbc, False): ',', (0xbc, True): '<',
         (0xbd, False): '-', (0xbd, True): '_',
         (0xbe, False): '.', (0xbe, True): '>',
         (0xbf, False): '/', (0xbf, True): '?',
         (0xc0, False): '`', (0xc0, True): '~',
         (0xdb, False): '[', (0xdb, True): '{',
         (0xdc, False): '\\', (0xdc, True): '|',
         (0xdd, False): ']', (0xdd, True): '}',
         (0xde, False): "'", (0xde, True): '"',
         }
for char in range(ord('A'), ord('Z') + 1):
    CHARS[(char, False)] = chr(char + ord('a') - ord('A'))
    CHARS[(char, True)] = chr(char)

for char in range(0x30, 0x40):
    CHARS[(char, False)] = chr(char)

def _get_key(event):
    keyCode = event.keyCode
    shift = event.shiftKey
    key = Struct()
    if _is_char(keyCode): 
        key.char = CHARS[(keyCode, shift)]
        key.keysym = key.char
    else:
        key.char = None
        key.keysym = KEY_CODE_NAMES.get(keyCode)
    return key

def _create_touch_dict(touchList):
    touchDict = dict()
    for touch in touchList:
        t = Struct()
        t.x, t.y = touch.pageX, touch.pageY
        touchDict[touch.identifier] = t
    return touchDict

class BrythonAnimation(object):
    def init(self): pass
    def onKeyDown(self, event): pass
    def onKeyRelease(self, event): pass
    def onMouseDown(self, event): pass
    def onMouseRelease(self, event): pass
    def onMouseMove(self, event): pass
    def redrawAll(self): pass
    def onTouch(self, touches): pass
    def onTouchDrag(self, touches): pass
    def onTouchRelease(self, touches): pass
    def onTouchCancel(self, touches): pass
    def onTimerFired(self): pass

    ############################################################################
    ############################################################################
    ## Initialization
    ############################################################################
    ############################################################################

    def _redraw_all(self):
        self.context.clear()
        self.redrawAll()

    def _key_ev(self, event, down=True):
        if down and self._last_key_ev != "down":
            self.onKeyDown(_get_key(event))
            self._last_key_ev = "down"
        elif (not down) and self._last_key_ev != "up":
            self.onKeyRelease(_get_key(event))
            self._last_key_ev = "up"
        self._redraw_all()

    def _touch(self, event):
        changes = _create_touch_dict(event.changedTouches)
        if event.type == "touchstart":
            self.onTouch(changes)
        elif event.type == "touchmove":
            self.onTouchDrag(changes)
        elif event.type == "touchend":
            self.onTouchRelease(changes)
        elif event.type == "touchcancel":
            self.onTouchCancel(changes)
        self._redraw_all()

    def _init_mouse(self):
        def mouseDownWrapper(event):
            self._redraw_all()
            self.onMouseDown(event)
        def mouseUpWrapper(event):
            self._redraw_all()
            self.onMouseRelease(event)
        self.canvas.bind("mousedown", mouseDownWrapper)
        self.canvas.bind("mouseup", mouseUpWrapper)

    def _init_mouseMotion(self):
        def mouseMoveWrapper(event):
            self._redraw_all()
            self.onMouseMove(event)
        browser.document.bind("mousemove", mouseMoveWrapper)

    def _init_keys(self):
        self._last_key_ev = None
        browser.document.bind("keydown", lambda event: self._key_ev(event))
        browser.document.bind("keyup", lambda event: self._key_ev(event, False))

    def _init_touch(self):
        browser.window.addEventListener("touchstart", lambda event: self._touch(event))
        browser.window.addEventListener("touchmove", lambda event: self._touch(event))
        browser.window.addEventListener("touchend", lambda event: self._touch(event))
        browser.window.addEventListener("touchcancel", lambda event: self._touch(event))

    def _init_tilt(self):
        self._tilt_event = None
        def on_tilt(event):
            self._tilt_event = (event.alpha, event.beta, event.gamma)
        browser.window.addEventListener('deviceorientation', on_tilt)

    def tilt_supported(self):
        return self._tilt_enabled and self._tilt_event != None and None not in self._tilt_event

    def get_tilt(self):
        return self._tilt_event

    def _init_geolocation(self):
        self._geolocation_event = None
        self._geolocation_allowed = False
        if not hasattr(browser.window.navigator, 'geolocation'): return

        def on_geolocation(event):
            self._geolocation_allowed = True
            self._geolocation_event = event.coords

        def on_geolocation_error(error):
            self._geolocation_allowed = False

        browser.window.navigator.geolocation.watchPosition(on_geolocation,
                                                           on_geolocation_error)

    def geolocation_supported(self):
        return (self._geolocation_enabled and
                hasattr(browser.window.navigator, 'geolocation') and
                self._geolocation_allowed)

    def get_geolocation(self):
        return self._geolocation_event

    def _init_vibrate(self):
        self._vibrate_fn = None
        for attr in ['vibrate', 'webkitVibrate', 'mozVibrate', 'msVibrate']:
            if hasattr(browser.window.navigator, attr):
                self._vibrate_fn = getattr(browser.window.navigator, attr)
                break

    def vibrate_supported(self):
        return self._vibrate_enabled and self._vibrate_fn != None

    def vibrate(self, duration):
        self._vibrate_fn(duration)

    def stop_vibration(self):
        self._vibrate_fn(0)

    def _init(self):
        self.context = ContextWrapper(self.canvas)
        self.init()

    def onTick(self, timestamp):
        if (timestamp - self._lastFrame >= self.timerDelay):
            self._lastFrame = timestamp
            self.onTimerFired()
            self._redraw_all()
        browser.timer.request_animation_frame(self.onTick)


    def __init__(self, canvasID="brythonCanvas"):
        self.canvas = browser.document[canvasID]
        self.width = self.canvas.width
        self.height = self.canvas.height
        self._init()

    def run(self, timerDelay=250, mouse=False, mouseMotion=False,
            keys=False, touch=False, tilt=False, geolocation=False,
            vibrate=False):
        if mouse: self._init_mouse()
        if mouseMotion: self._init_mouseMotion()
        if keys: self._init_keys()
        if touch: self._init_touch()
        self._tilt_enabled = tilt
        if tilt: self._init_tilt()
        self._geolocation_enabled = geolocation
        if geolocation: self._init_geolocation()
        self._vibrate_enabled = vibrate
        if vibrate: self._init_vibrate()
        # Start the timer
        self.timerDelay = timerDelay
        self._lastFrame = 0
        browser.timer.request_animation_frame(self.onTick)

