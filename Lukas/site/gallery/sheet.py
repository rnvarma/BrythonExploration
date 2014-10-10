from browser import document, html, alert,local_storage

current_cell = None

def entry_keydown(ev):
    target = ev.target
    is_arrow = ev.keyCode in [9, #tab
        37, # left
        39, # right
        38, #up
        40, #down
        13  # CR
        ]

    if is_arrow:
        value = ev.target.value
        cell = ev.target.parent
        row = cell.parent
        cell_num = row.children.index(cell)
        row_num = row.parent.children.index(row)
        
        # jump to next cell
        if ev.keyCode==39 or (ev.keyCode==9 and not ev.shiftKey) or ev.keyCode==13:
            if cell_num<len(row.children)-1:
                next_cell = row.children[cell_num+1]
                make_input(next_cell)
        elif ev.keyCode==37 or (ev.keyCode==9 and ev.shiftKey):
            if cell_num>1:
                next_cell = row.children[cell_num-1]
                make_input(next_cell)
        elif ev.keyCode == 40:
            if row_num<len(row.parent.children)-1:
                next_cell = row.parent.children[row_num+1].children[cell_num]
                make_input(next_cell)
        elif ev.keyCode == 38:
            if row_num>1:
                next_cell = row.parent.children[row_num-1].children[cell_num]
                make_input(next_cell)

        ev.preventDefault()
        ev.stopPropagation()

def entry(ev):
    make_input(ev.target)

def make_input(cell):
    global current_cell
    if current_cell is not None:
        value = current_cell.get(selector='INPUT')[0].value
        current_cell.clear()
        current_cell.text = value
    value = cell.text.strip()
    cell.clear()
    input = html.INPUT(value=value,
        style={'padding':'0px'})
    input.style.width = '%spx' %100
    cell <= input
    input.bind('keydown', entry_keydown)
    input.focus()
    #input.select()
    current_cell = cell
    
# returns an HTML table with specified rows and columns

def over_menu(ev):
    ev.target.style.backgroundColor='#DDD'

def out_menu(ev):
    ev.target.style.backgroundColor='#FFF'

def sub_menu(ev):
    
    left, top, height = ev.target.left, ev.target.top, ev.target.height
    ev.target.style.borderColor = '#777'
    
    if ev.target.text=='File':
        menu = html.DIV(style=dict(position='absolute',
            left=left,top=top+height,zIndex=99,padding='5px',backgroundColor='#FFF',
            borderStyle='solid', borderWidth='1px', borderColor="#777"))

        m_new = html.DIV('New', style=dict(padding='10px'))
        m_new.bind('mouseover', over_menu)
        m_new.bind('mouseout', out_menu)
        menu <= m_new
        
        m_open = html.DIV('Open...', style=dict(padding='5px 10px 5px 2px'))
        m_open.bind('mouseover', over_menu)
        m_open.bind('mouseout', out_menu)
        menu <= m_open
        
        document <= menu        

class BarItem:

    def __init__(self, parent, label):
        self.item = html.DIV(label,style=dict(float='left',
            padding='5px 7px 5px 7px',
            borderWidth='1px', borderStyle='solid', borderColor='#FFF')
            )
        self.item.bind('click', self.open)
        parent <= self.item
        self.children = []

    def open(self, ev):
        global current_menu
        stop_menu()
        self.menu = html.DIV(style=dict(position='absolute',
            left=self.item.left,
            top=self.item.top+self.item.height,
            zIndex=99,padding='5px',backgroundColor='#FFF',
            borderStyle='solid', borderWidth='1px', borderColor="#777"))
        for child in self.children:
            self.menu <= child
        self.item.style.borderColor = '#777'
        document <= self.menu
        current_menu = self
        ev.stopPropagation()

    def close(self):
        self.item.style.borderColor = '#FFF'
        document.remove(self.menu)
        
class MenuListItem:

    def __init__(self, parent, label, action=None):
        item = html.DIV(label, style=dict(padding='10px'))
        item.bind('mouseover', over_menu)
        item.bind('mouseout', out_menu)
        if action is not None:
            item.bind('click', action)
        parent.children.append(item)

def select_sheet(ev):
    sheet_names = [ name for name in local_storage.LocalStorage().keys()
        if name.startswith('brython_sheet')]
    names = [name[13:] for name in sheet_names]
    names.sort()
    div = html.DIV(style=dict(position='absolute',
        top = ev.target.top,
        left = ev.target.left+ev.target.width+10,
        padding = "40px",
        borderWidth="1px", borderStyle="solid", borderColor="#777",
        backgroundColor="#FFF", zIndex=99))
    if names:
        sel = html.SELECT()
        for name in names:
            sel <= html.OPTION(name)
        div <= sel
    else:
        div <= html.DIV("No file found")
        b = html.BUTTON("Ok")
        b.bind('click', lambda ev:document.remove(div))
        div <= b
    document <= div

def save_as(ev):
    sheet_names = [ name for name in local_storage.LocalStorage().keys()
        if name.startswith('brython_sheet')]
    names = [name[13:] for name in sheet_names]
    names.sort()
    div = html.DIV(style=dict(position='absolute',
        top = ev.target.top,
        left = ev.target.left+ev.target.width+10,
        padding = "40px",
        borderWidth="1px", borderStyle="solid", borderColor="#777",
        backgroundColor="#FFF", zIndex=99))
    div <= html.DIV("Name",style=dict(float='left', padding="8px"))    
    _input = html.INPUT()
    _input.bind('blur', save)
    div <= _input
    b = html.BUTTON("Cancel")
    b.bind('click', lambda ev:document.remove(div))
    div <= b

    document <= div

def save(ev):
    print('save', ev.target.value)
    
current_menu = None

def stop_menu(*args):
    global current_menu
    if current_menu:
        current_menu.close()
    current_menu = None

document.bind('click', stop_menu)

def load(sheet_name=None):
    document.clear()
    
    if sheet_name is None:
        sheet_name = 'New document'
    
    title = html.DIV(style=dict(width='auto'))
    title <= html.H2(sheet_name)
    
    document <= title
    
    menu = html.DIV(style=dict(paddingBottom='5px'))

    menu_file = BarItem(menu, 'File')
    MenuListItem(menu_file, 'New')
    MenuListItem(menu_file, 'Open...', select_sheet)
    MenuListItem(menu_file, 'Save as...', save_as)
  
    document <= menu
    
    t = html.TABLE()
    srow = -1
    rows, cols = 20, 20
    col_widths = [100 for i in range(rows)]
    
    line = html.TR()
    line <= html.TH()
    for i in range(cols):
        col_name = chr(65+i)
        line <= html.TH(col_name, style={'min-width':'%spx' %col_widths[i]})
    t <= line
        
    for i in range(rows*cols):
        row, column = divmod(i, cols)
        if row>srow:
            line = html.TR()
            line <= html.TH(row+1)
            t <= line
            srow = row
        cell = html.TD('',id='c%s_%s' %(row,column))
        cell.bind('click', entry)
        line <= cell

    puzzle = html.DIV(style=dict(float='left'))
    puzzle <= t
    document <= puzzle
    make_input(t.get(selector='TD')[0])

load()