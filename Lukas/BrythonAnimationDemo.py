from BrythonAnimation import BrythonAnimation
import browser

def rgbString(r, g, b):
    return "#%2X%2X%2X" % (r, g, b)

class Demo(BrythonAnimation):
    def init(self):
        self.ovals = dict()

    def onKeyDown(self, event):
        browser.window.alert(event.keysym)

    def redrawAll(self):
        self.context.create_rectangle(self.width/2, self.height/2, self.width, self.height, fill="#ff0000")
        for identifier in self.ovals:
            coords = self.ovals[identifier]
            self.context.create_circle(coords.x, coords.y, 30, fill=rgbString(0, 0, 100))

browser.window.alert("Starting!")
Demo(touch=True, keys=True)