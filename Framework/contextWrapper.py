import javascript, browser
math = javascript.JSObject(browser.window["Math"])

N = 'n'
E = 'e'
S = 's'
W = 'w'
NE = 'ne'
SE = 'se'
SW = 'sw'
C = ''

class ContextWrapper(object):
    def __init__(self, canvas):
        self.context = canvas.getContext('2d')
        self.canvas = canvas

    def clear(self):
        self.context.clearRect(0, 0, self.canvas.width, self.canvas.height)

    def create_rectangle(self, cx, cy, w, h, fill=None,
                         width=1, outline="#000000", angle=0):
        w, h = w/2, h/2
        cos, sin = math.cos, math.sin
        a = math.atan(1.0 * h / w)
        r = w / cos(a)
        context = self.context
        context.beginPath()
        context.moveTo(cx + r*cos(angle+a), cy - r*sin(angle+a))
        context.lineTo(cx + r*cos(angle-a), cy - r*sin(angle-a))
        context.lineTo(cx - r*cos(angle+a), cy + r*sin(angle+a))
        context.lineTo(cx - r*cos(angle-a), cy + r*sin(angle-a))
        self.colorize(fill, outline, lineWidth)
        context.closePath()

    def create_oval(self, cx, cy, w, h, fill=None,
                    width=1, outline="#000000", angle=0):
        w, h = w/2, h/2
        magic = 0.551784 
        a = angle
        a1 = math.atan(magic*h/w)
        a2 = math.atan(magic*w/h)
        cos, sin = math.cos, math.sin
        r1 = w / cos(a1)
        r2 = h / cos(a2)
        context = self.context
        context.beginPath()
        context.moveTo(cx + w*cos(a), cy - w*sin(a))
        context.bezierCurveTo(cx + r1*cos(a-a1), cy - r1*sin(a-a1),
                              cx + r2*sin(a+a2), cy + r2*cos(a+a2),
                              cx + h*sin(a), cy + h*cos(a))
        context.bezierCurveTo(cx + r2*sin(a-a2), cy + r2*cos(a-a2),
                              cx - r1*cos(a+a1), cy + r1*sin(a+a1),
                              cx - w*cos(a), cy + w*sin(a))
        context.bezierCurveTo(cx - r1*cos(a-a1), cy + r1*sin(a-a1),
                              cx - r2*sin(a+a2), cy - r2*cos(a+a2),
                              cx - h*sin(a), cy - h*cos(a))
        context.bezierCurveTo(cx - r2*sin(a-a2), cy - r2*cos(a-a2),
                              cx + r1*cos(a+a1), cy - r1*sin(a+a1),
                              cx + w*cos(a), cy - w*sin(a))
        self.colorize(fill, outline, width)
        context.closePath()

    def create_circle(self, cx, cy, r, fill=None,
                      width=1, outline="#000000"):
        context = self.context
        context.beginPath()
        context.arc(cx, cy, r, 0, 2*math.PI)
        self.colorize(fill, outline, width)
        context.closePath()

    def create_polygon(context, *points, **kwargs):
        if len(points) == 0: return
        points = parse_points(*points)
        if points == -1: return
        context = self.context
        context.beginPath()
        context.moveTo(points[0][0], points[0][1])
        for point in points[1:]:
            context.lineTo(point[0], point[1])
        fill = kwargs.get("fill", None)
        width = kwargs.get("width", 1)
        outline = kwargs.get("outline", "#000000")
        self.colorize(fill, outline, width)
        context.closePath()

    def create_ngon(self, n, cx, cy, r, fill="#FFFFFF", width=1,
                    outline="#000000", angle=0):
        pts = []
        circle = 2 * math.PI
        innerAngle = circle / n
        angle += math.PI/2
        for point in range(n):
            a = angle + innerAngle * point
            x, y = cx + r*math.cos(a), cy - r*math.sin(a)
            pts.append((x, y))
        context = self.context
        context.beginPath()
        context.moveTo(pts[0][0], pts[0][1])
        for pt in pts[1:]:
            context.lineTo(pt[0], pt[1])
        colorize(fill, outline, width)
        context.closePath()

    def create_text(self, x, y, text, font="Arial", size=24, anchor='',
                    fill="#000000"):
        context = self.context
        context.font = "%dpx %s" % (size, font)
        if ('e' in anchor):   context.textAlign = "left"
        elif ('w' in anchor): context.textAlign = "right"
        else:                 context.textAlign = "center"
        if ('n' in anchor):       y = y + size
        elif ('s' not in anchor): y = y + size/2
        context.fillStyle = fill
        context.fillText(text, x, y)

    def drawImage(self, img, x, y, sx=None, sy=None, swidth=None, sheight=None,
                  width=None, height=None):
        context = self.context
        if (sx == None):
            if (width == None):
                context.drawImage(img, x, y)
            else:
                assert (height != None)
                context.drawImage(img, x, y, width, height)
        else:
            assert (sy != None)
            assert (swidth != None)
            assert (sheight != None)
            if (width == None):
                context.drawImage(img, x, y, sx, sy, swidth, sheight)
            else:
                assert (height != None)
                context.drawImage(img, x, y, sx, xy, swidth, sheight,
                                  width, height)

    def colorize(self, fill, outline, width):
        context = self.context
        if fill != None:
            context.fillStyle = fill
            context.fill()
        if width != 0 and outline != None:
            context.strokeStyle = outline
            context.lineWidth = width
            context.stroke()

def parse_points(*pts):
    a = [type(pt) == int for pt in pts]
    b = [type(pt) in (tuple, list) for pt in pts]
    ints, iters = all(a), all(b)
    if not (ints or iters):
        raise Exception("All points for create_polygon should be same format")
        return -1
    if ints:
        if len(a) % 2 == 0:
            c = []
            for i in range(0, len(a), 2):
                c.append((pts[i], pts[i+1]))
            return c
        else:
            raise Exception("create_polygon requires an" +
                            "even number of individual coordinates")
            return -1
    else:
        return pts
