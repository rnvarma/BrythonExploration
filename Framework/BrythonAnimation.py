import browser, sys, javascript
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
    def onDrag(self, event): pass
    def redrawAll(self): pass
    def onTouch(self, touches): pass
    def onTouchDrag(self, touches): pass
    def onTouchRelease(self, touches): pass
    def onTouchCancel(self, touches): pass

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
        pass

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
        pass

    def _init_geolocation(self):
        pass

    def _init_vibrate(self):
        pass

    def _init(self):
        self.context = ContextWrapper(self.canvas)
        self.init()

    def __init__(self, canvasID="brythonCanvas", mouse=False, keys=False,
                 touch=False, tilt=False, geolocation=False, vibrate=False):
        self.canvas = browser.document[canvasID]
        self.width = self.canvas.width
        self.height = self.canvas.height
        if mouse: self._init_mouse()
        if keys: self._init_keys()
        if touch: self._init_touch()
        if tilt: self._init_tilt()
        if geolocation: self._init_geolocation()
        if vibrate: self._init_vibrate()
        self._init()

#BrythonAnimation(keys=True, touch=True)