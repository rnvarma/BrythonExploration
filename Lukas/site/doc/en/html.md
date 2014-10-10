module **browser.html**
-----------------------

This module exposes the HTML tags. The tag name is in uppercase letters

The classes defined are :

- HTML4 tags : `A, ABBR, ACRONYM, ADDRESS, APPLET,AREA, B, BASE, BASEFONT, BDO, BIG, BLOCKQUOTE, BODY, BR, BUTTON, CAPTION, CENTER, CITE, CODE, COL, COLGROUP, DD, DEL, DFN, DIR, DIV, DL, DT, EM, FIELDSET, FONT, FORM, FRAME, FRAMESET,H1, H2, H3, H4, H5, H6, HEAD, HR, HTML, I, IFRAME, IMG, INPUT, INS, ISINDEX, KBD, LABEL, LEGEND, LI, LINK, MAP, MENU, META, NOFRAMES, NOSCRIPT, OBJECT,OL, OPTGROUP, OPTION, P, PARAM, PRE, Q, S, SAMP, SCRIPT, SELECT, SMALL, SPAN, STRIKE, STRONG, STYLE, SUB, SUP, TABLE, TBODY, TD, TEXTAREA, TFOOT, TH, THEAD, TITLE, TR, TT, U, UL, VAR`

> In the following [link](http://www.w3.org/TR/html4/index/elements.html) you can find the index of HTML4 tags with references. Some of the above tags are deprecated in HTML4.01.

- HTML5 tags : `ARTICLE, ASIDE, AUDIO, BDI, CANVAS, COMMAND, DATALIST, DETAILS, DIALOG, EMBED, FIGCAPTION, FIGURE, FOOTER, HEADER, HGROUP, KEYGEN, MARK, METER, NAV, OUTPUT, PROGRESS, RP, RT, RUBY, SECTION, SOURCE, SUMMARY, TIME, TRACK, VIDEO, WBR`

> In the following [link](http://www.w3.org/TR/html5-author/index.html#elements-1) you can find the index of HTML5 tags with references (DRAFT).

[Note: In the following examples we assume that the **browser.html** module has been imported as follows: `from brower import html`]

The syntax to create an object (e.g. a hyperlink) is :

`A(`*[content,[attributes]]*`)`

> *content* is the child node of the the object ; it can be a Python object such as a string, a number, a list etc., or an instance of another class in the **html** module

> *attributes* is a sequence of keywords corresponding to the [attributes](http://www.w3.org/TR/html5-author/index.html#attributes-1) of the HTML tag. These attributes must be provided as Javascript syntax, not CSS (e.g., *backgroundColor* instead of *background-color*)

If an attribute is not a valid Python name (eg _data-type_) it can't be 
passed as argument ; the method `setAttribute` must be used :

>    form = html.FORM()
>    form.setAttribute("data-type", "confirm")

For the *style* attribute, the value must be a dictionary :

>    d = html.DIV('Brython', style={'height':100, 'width':200})

or

>    d = html.DIV('Brython', style=dict(height=100, width=200))

To avoid conflicts with the Python keyword, the attribute *class* must be capitalized :

>    d = html.DIV('Brython', Class="container")

You can also create an object without argument, then build it up:

- to add a child node, use the **<=** operator
- to add attributes, use the classic Python syntax : `object.attribute = value`
Example :    
>    link = html.A()
>    link <= html.B('connexion')
>    link.href = 'http://example.com'

You can also create multiple elements at the same level by using the plus (+) sign :

>    row = html.TR(html.TH('LastName') + html.TH('FirstName'))

Here is how to create a selection box from a list (by combining these operators and Python syntax) :

>    items = ['one', 'two', 'three']
>    sel = html.SELECT()
>    for i, elt in enumerate(items):
>        sel <= html.OPTION(elt, value = i)
>    document <= sel

It is important to note that the creation of an instance of a class involves creating HTML from a single DOM object. If we assign the instance to a variable, you can not use it in several places. For example, with this code :

>    link = html.A('Python', href='http://www.python.org')
>    document <= 'Official Python Website: ' + link
>    document <= html.P() + 'I repeat: the site is ' + link

the link will only show in the second line. One solution is to clone the original object :

>    link = html.A('Python', href='http://www.python.org')
>    document <= 'Official Python Website: ' + link
>    document <= html.P() + 'I repeat: the site is ' + link.clone()

As a rule of thumb, instances of HTML classes have the same attribute names as the corresponding DOM objects. For example, it can retrieve the option selected by the `selectedIndex` attribute of the `SELECT` object. Brython adds a few things to make the manipulation a bit more Pythonic

Let's see a more complete example. The code below have created the structure in the blue panel. The blue panel is a `div` element with `id="container"` attribute.
We will use this `div` to create an 'ugly' html structure inside with a div, a table, a form and a HTML5 canvas:

<div style="padding-left:50px;">
<table cellpadding=10>
<tr>
<td style="width:100px;">
<div id="html-doc" style="background-color:#dddddd;">
    # First of all, the import of some libraries
    from browser import document as doc
    from browser import html
    
    # All the elements will be inserted in the div with the "container" id
    container = doc['container']
    
    # We create a new div element
    newdiv = html.DIV(id = "new-div")
    # Now we add some style
    newdiv.style = {"padding": "5px", 
                   "backgroundColor": "#ADD8E6"}
    
    # Now, lets add a table with a column with numbers and a
    # column with a word on each cell
    text = "Brython is really cool"
    textlist = text.split()
    table = html.TABLE()
    for i, word in enumerate(textlist):
        table <= html.TR(html.TD(i + 1) + 
                         html.TD(word))
    # Now we add some style to the table
    table.style = {"padding": "5px", 
                   "backgroundColor": "#aaaaaa",
                   "width": "100%"}
    # Now we add the table to the new div previously created
    newdiv <= table + html.BR()
    
    # a form? why not?
    form = html.FORM()
    input1 = html.INPUT(type="text", name="firstname", value="First name")
    input2 = html.INPUT(type="text", name="lastname", value="Last name")
    input3 = html.BUTTON("Button with no action!")
    form <= input1 + html.BR() + input2 + html.BR() + input3
    
    newdiv <= form + html.BR()
    
    # Finally, we will add something more 'HTML5istic', a canvas with
    # a color gradient in the newdiv previously created and below the form
    canvas = html.CANVAS(width = 300, height = 300)
    canvas.style = {"width": "100%"}
    ctx = canvas.getContext('2d')
    ctx.rect(0, 0, 300, 300)
    grd = ctx.createRadialGradient(150, 150, 10, 150, 150, 150)
    grd.addColorStop(0, '#8ED6FF')
    grd.addColorStop(1, '#004CB3')
    ctx.fillStyle = grd
    ctx.fill()
    
    newdiv <= canvas
    
    # And finally we append the newdiv element
    # to the parent, in this case the div with the "container" id
    container <= newdiv
    
</div>
</td>
<td>
<div id="container"></div>
</td>
</tr>
</table>
</div>

<script type="text/python">
exec(doc["html-doc"].text)
</script>







