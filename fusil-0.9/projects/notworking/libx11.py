from fusil.c_tools import FuzzyFunctionC, CodeC
from fusil.file_watch import FileWatch
from fusil.process.create import CreateProcess
from fusil.process.watch import WatchProcess
from fusil.project_agent import ProjectAgent

def setupProject(project):
    FileWatch(project, open('/var/log/Xorg.0.log'), "Xorg.log", start="end")
    GenerateCode(project, "x11.c")
    process = X11Process(project, name="x11")
    process.env.copy('DISPLAY')
    WatchProcess(process)

class GenerateCode(ProjectAgent):
    def on_session_start(self):
        # Intialize some parameters
        self.buffer_count = 0

        # Create program using C compiler
        code = CodeC()
        code.includes = [
            '<X11/Xlib.h>',
            '<stdio.h>',
            '<stdlib.h>',
        ]
        main = code.addFunction(FuzzyFunctionC('main', type='int'))

        # Open display
        main.variables.append('Display *dpy')
        main.add('dpy = XOpenDisplay(NULL)')
        main.add(r'if (!dpy) { fprintf(stderr, "ERROR: could not open display\n"); exit(1); }')

        # Get elements
        main.variables.append('int scr')
        main.add('scr = DefaultScreen(dpy)')
        main.variables.append('Window rootwin')
        main.add('rootwin = RootWindow(dpy, scr)')

        # Create window and show it
        main.variables.append('Window win')
        main.add('win=XCreateSimpleWindow(dpy, rootwin, 1, 1, 100, 50, 0, BlackPixel(dpy, scr), BlackPixel(dpy, scr))')

        main.variables.append('GC gc')
        main.add('gc=XCreateGC(dpy, win, 0, NULL)')
        if False:
            name, size = main.createRandomBytes()
            main.add('XDrawString(dpy, win, gc, 10, 10, NULL /*%s*/, %s)' % (name, size+10))
        else:
            size = main.createInt()
            main.add('XDrawString(dpy, win, gc, 10, 10, NULL, %sU)' % size)
        self.error("size=%s" % size)

        # Show window
        main.add('XMapWindow(dpy, win)')

        # Close display
        main.add('XCloseDisplay(dpy)');
        main.add('exit(0)')

        # Compile program
        directory = self.project().session.directory
        self.c_filename = directory.uniqueFilename("x11.c")
        self.program_filename = directory.uniqueFilename("x11")
        code.compile(self, self.c_filename, self.program_filename, libraries=['X11'])
        self.send('x11_program', self.program_filename)

class X11Process(CreateProcess):
    def on_x11_program(self, program):
        self.cmdline.arguments = [program]
        self.createProcess()

