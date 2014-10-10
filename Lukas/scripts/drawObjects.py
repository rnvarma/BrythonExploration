def rgbString(red, green, blue):
    exc = "Invalid value for %s: %d\nMust be between 0 and 255"
    if not (0 <=  red  <= 255):
        raise Exception(exc % ("red", red))
    if not (0 <= green <= 255):
        raise Exception(exc % ("green", green))
    if not (0 <=  blue <= 255):
        raise Exception(exc % ("blue", blue))
    return "#%02x%02x%02x" % (red, green, blue)

def create_oval(context, x0, y0, x1=None, y1=None, fill="#FFFFFF",
                width=1, outline="#000000"):
    """
    Draw an oval in the rectangle defined by (x0, y0) and (x1, y1).

    context: HTML5 canvas context
    x0, y0 - coordinates of top-left corner if (x1, y1) != (None, None)
        else bottom-right corner
    x1, y1 - coordinates of bottom-right corner
    fill - fill style for oval (color / gradient)
    width - width of stroke (<= 0 for no stroke)
    outline - stroke style for oval (color / gradient)
    """
    cx, cy = (x0 + x1) / 2, (y0 + y1) / 2
    context.beginPath()
    return 0