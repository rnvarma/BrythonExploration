from BrythonAnimation import BrythonAnimation
import browser

def rgbString(r, g, b):
    if not(0 <= r < 256 and 0 <= g < 256 and 0 <= b < 256):
        return "#000000"
    r = "{0:x}".format(r)
    if (len(r) == 1): r = "0" + r
    g = "{0:x}".format(g)
    if (len(g) == 1): g = "0" + g
    b = "{0:x}".format(b)
    if (len(b) == 1): b = "0" + b
    return "#" + r + g + b

class Demo(BrythonAnimation):
    def init(self):
        self.ovals = dict()

    def onTouch(self, touches):
        for touchID in touches:
            self.ovals[touchID] = touches[touchID]

    def onTouchDrag(self, touches):
        self.onTouch(touches)

    def onTouchRelease(self, touches):
        for touchID in touches:
            del self.ovals[touchID]

    def onTouchCancel(self, touches):
        self.onTouchRelease(touches)

    def onKeyDown(self, event):
        print(event.keysym)

    def redrawAll(self):
        for identifier in self.ovals:
            coords = self.ovals[identifier]
            self.context.create_circle(coords.x, coords.y, 30, fill="#0000ff")

Demo(touch=True, keys=True)