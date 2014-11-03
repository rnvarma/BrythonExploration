import browser

from BrythonAnimation import BrythonAnimation

class DemoApp(BrythonAnimation):
    def init(self):
        self.keyLoc = 10, 10
        self.keyDown = False
        self.lastKey = None

        self.countLoc = 10, 30
        self.count = 0

        self.mousePath = []
        self.mouseDown = False

        self.touchCountLoc = 10, 50
        self.touches = {}

        self.geoLoc = 10, 70
        self.geoText = ""

        self.tiltLoc = 10, 90
        self.tiltText = ""

    def onKeyDown(self, event):
        self.keyDown = True
        self.lastKey = event.keysym

    def onKeyRelease(self, event):
        self.keyDown = False

    def onMouseDown(self, event):
        self.mouseDown = True
        self.mousePath = []

    def onMouseRelease(self, event):
        self.mouseDown = False

    def onMouseMove(self, event):
        if self.mouseDown:
            self.mousePath.append((event.x, event.y))

    def onTimerFired(self):
        self.count += 1

        if self.tilt_supported():
            tilt = self.get_tilt()
            self.tiltText = "alpha: %0.2f\nbeta: %0.2f\ngamma: %0.2f" % (tilt)
        else:
            self.tiltText = "Not available"

        if self.geolocation_supported():
            geo = self.get_geolocation()
            self.geoText = "Lat: %s, Long: %s" % (geo.latitude, geo.longitude)
        else:
            self.geoText = "Not available"

    def onTouch(self, touches):
        self.touches.update(touches)
        if self.vibrate_supported():
            self.vibrate(100)

    def onTouchDrag(self, touches):
        self.touches.update(touches)

    def onTouchRelease(self, touches):
        for identifier in touches:
            del self.touches[identifier]

    def redrawAll(self):
        self.context.create_text(*self.keyLoc, text="Last key: %s" % self.lastKey,
            fill=("#FF0000" if self.keyDown else "#000000"), anchor='e')
        self.context.create_text(*self.countLoc, text="%d" % self.count, 
            anchor='e')
        self.context.create_text(*self.touchCountLoc, text="Touches: %r" % ["%d: %r" % (i, t) for i, t in self.touches.items()],
            anchor='e')
        self.context.create_text(*self.geoLoc, text="Location: %s" % self.geoText, anchor='e')
        self.context.create_text(*self.tiltLoc, text="Tilt: %s" % self.tiltText, anchor='e')
        
        for x, y in self.mousePath:
            self.context.create_circle(x, y, 3)


d = DemoApp()
d.run(keys=True, mouse=True, mouseMotion=True, touch=True,
      tilt=True, geolocation=True, vibrate=True)