from Xlib.X import NONE, KeyPress, KeyRelease, AnyPropertyType, CurrentTime
from Xlib.display import Display
from Xlib.protocol.event import (KeyPress as KeyPressEvent,
    KeyRelease as KeyReleaseEvent)
from Xlib.protocol.request import InternAtom
from re import compile as compileRegex, IGNORECASE

def listWindows(root):
    children = root.query_tree().children
    for window in children:
        yield window
    for window in children:
        for window in listWindows(window):
            yield window

def findWindowById(root, window_id):
    for window in listWindows(root):
        if window.id == window_id:
            return window
    raise KeyError("Unable to find Window 0x%08x" % window_id)

def findWindowByNameRegex(root, name_regex, ignore_case=True):
    if ignore_case:
        flags = IGNORECASE
    else:
        flags = 0
    match = compileRegex(name_regex, flags).search
    for window in listWindows(root):
        name = window.get_wm_name()
        if name and match(name):
            return window
    raise KeyError("Unable to find window with name regex: %r" % name_regex)

def formatWindow(window):
    name = window.get_wm_name()
    info = []
    if name:
        info.append(name)

    geometry = window.get_geometry()
    info.append('%sx%sx%s at (%s,%s)' % (
        geometry.width, geometry.height, geometry.depth,
        geometry.x, geometry.y))

    atom = InternAtom(display=window.display, name="_NET_WM_PID", only_if_exists=1)
    pid = window.get_property(atom.atom, AnyPropertyType, 0, 10)
    if pid:
        pid = int(pid.value.tolist()[0])
        info.append('PID=%r' % pid)

    info.append("ID=0x%08x" % window.id)
    return '; '.join(info)

def displayWindows(root, level=0):
    tree = root.query_tree()
    children = tree.children
    if not children:
        return
    indent = ("   "*level)
    print indent + "|== %s ===" % formatWindow(root)
    parent = tree.parent
    if parent:
        print indent + "|-- parent: %s" % formatWindow(parent)
    for window in children:
        print indent + "|-> %s" % formatWindow(window)
        displayWindows(window, level+1)

def sendKey(window, keycode, modifiers=0, released=True):
    if released:
        type = KeyRelease
        event_class = KeyReleaseEvent
    else:
        type = KeyPress
        event_class = KeyPressEvent
    event = event_class(
        type=type,
        detail=keycode,
        time=CurrentTime,
        root=NONE,
        window=window,
        child=NONE,
        root_x=0,
        root_y=0,
        event_x=0,
        event_y=0,
        state=modifiers,
        same_screen=1)
    window.send_event(event)
    window.display.flush()

def getDisplay():
    return Display()

def setupX11Process(process):
    process.env.copy('HOME')
    process.env.copy('DISPLAY')

