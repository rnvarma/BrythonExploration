import javascript, browser
math = javascript.JSObject(browser.window["Math"])

def create_oval(context, cx, cy, w, h, fill=None,
                width=1, outline="#000000", angle=0):
    """
    context - HTML5 canvas context to draw on
    cx, cy - coordinates for center of oval
    w, h - width and height of oval before rotation
    fill - fill style for oval (color / gradient)
    width - width of stroke (<= 0 for no stroke)
    outline - stroke style for oval (color / gradient)
    angle - angle (in radians) to rotate by
    """
    w, h = w/2, h/2
    magic = 0.551784
    a = angle
    a1 = math.atan(magic*h/w)
    a2 = math.atan(magic*w/h)
    cos, sin = math.cos, math.sin
    r2 = h / (cos(a2))
    r1 = w / (cos(a1))
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
    if fill != None:
        context.fillStyle = fill
        context.fill()
    if width != 0 and outline != None:
        context.strokeStyle = outline
        context.lineWidth = width
        context.stroke()
    context.closePath()

def create_circle(context, cx, cy, r, fill=None,
                  width=1, outline="#000000"):
    """
    context - HTML5 canvas context to draw on
    cx, cy - coordinates for center of circle
    w, h - width and height of circle before rotation
    fill - fill style for circle (color / gradient)
    width - width of stroke (<= 0 for no stroke)
    outline - stroke style for circle (color / gradient)
    """
    context.beginPath()
    context.arc(cx, cy, r, 0, 2*math.PI)
    if fill != None:
        context.fillStyle = fill
        context.fill()
    if width != 0 and outline != None:
        context.strokeStyle = outline
        context.lineWidth = width
        context.stroke()
    context.closePath()

def create_rectangle(context, cx, cy, w, h, fill=None,
                     width=1, outline="#000000", angle=0):
    """
    context - HTML5 canvas context to draw on
    cx, cy - coordinates for center of rectangle
    w, h - width and height of rectangle before rotation
    fill - fill style for rectangle (color / gradient)
    width - width of stroke (<= 0 for no stroke)
    outline - stroke style for rectangle (color / gradient)
    angle - angle (in radians) to rotate rectangle by
    """
    w, h = w/2, h/2
    cos, sin = math.cos, math.sin
    a = math.atan(h/w)
    r = w/cos(a)
    context.beginPath()
    context.moveTo(cx + r*cos(angle+a), cy - r*sin(angle+a))
    context.lineTo(cx + r*cos(angle-a), cy - r*sin(angle-a))
    context.lineTo(cx - r*cos(angle+a), cy + r*sin(angle+a))
    context.lineTo(cx - r*cos(angle-a), cy + r*sin(angle-a))
    context.closePath()
    if fill != None:
        context.fillStyle = fill
        context.fill()
    if width != 0 and outline != None:
        context.strokeStyle = outline
        context.lineWidth = width
        context.stroke()

def create_polygon(context, wtc, *points, **kwargs):
    """
    context - canvas context to draw on
    points - a set of points to draw a polygon:
        x0, y0, x1, y1, x2, y2, ...  OR
        (x0, y0), (x1, y1), (x2, y2), ...
    kwargs - all options
        fill - fill style
        width - stroke width
        outline - stroke style
    """
    if len(points) == 0: return
    points = parse_points(*points)
    if points == -1: return
    context.beginPath()
    context.moveTo(points[0][0], points[0][1])
    for point in points[1:]:
        context.lineTo(point[0], point[1])
    context.closePath()
    fill = kwargs.get("fill", -1)
    width, outline = kwargs.get("width"), kwargs.get("outline", -1)
    fill = None if fill == -1 else fill
    width = 1 if width == None else width
    outline = "#000000" if outline == -1 else outline
    if fill != None:
        context.fillStyle = fill
        context.fill()
    if width != 0 and outline != None:
        context.strokeStyle = outline
        context.lineWidth = width
        context.stroke()

def create_ngon(context, n, cx, cy, r, fill="#FFFFFF", width=1,
                outline="#000000", angle=0):
    """
    regular ngon centered at (cx, cy) with radius r
    """# circle = 2*jsmath.PI
    pts = []
    circle = 2 * math.PI
    innerAngle = circle / n
    angle += math.PI/2
    for point in range(n):
        a = angle + innerAngle * point
        x, y = cx + r*math.cos(a), cy - r*math.sin(a)
        pts.append((x, y))
    context.beginPath()
    context.moveTo(pts[0][0], pts[0][1])
    for pt in pts[1:]:
        context.lineTo(pt[0], pt[1])
    context.closePath()
    if fill != None:
        context.fillStyle = fill
        context.fill()
    if width != 0 and outline != None:
        context.strokeStyle = outline
        context.lineWidth = width
        context.stroke()
    #create_polygon(context, None, *points, fill=fill, width=width, outline=outline)

def create_star(context, cx, cy, rOuter, rInner=None, n=5, fill="#FFFFFF",
                width=1, outline="#000000", angle=0):
    angle += math.PI/2
    points = []
    circle = 2 * math.PI
    if rInner == None:
        thetaInner = math.PI/2 + circle / (2*n)
        thetaOuter = math.PI/2 + 2*circle / (2*n)
        rInner = rOuter*math.sin(thetaOuter) / math.sin(thetaInner)
    for step in range(2*n):
        a = math.PI/2 + step*circle / (2*n)
        r = rOuter if step % 2 == 0 else rInner
        x = cx + r*math.cos(a)
        y = cy - r*math.sin(a)
        points.append((x, y))
    create_polygon(context, None, *points, fill=fill, width=width, outline=outline)

###########################################################
####  IGNORE THE REST OF THIS FILE - HELPER FUNCTIONS  ####
###########################################################

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
