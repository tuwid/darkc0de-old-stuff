"""
HTTP server serving fuzzy JPEG image or Flash animation.

Project is currently specific to Firefox on Linux.
"""

PORT = 8080
NB_FILES = 8
HOMEPAGE_URL = "http://localhost:%s/" % PORT
ROWS = 4

def setupProject(project):
    MAX_MEMORY = 200*1024*1024

    if True:
        firefox = FirefoxProcess(project, ["firefox", '-safe-mode', HOMEPAGE_URL], timeout=None)
        setupX11Process(firefox)
        firefox.max_memory = MAX_MEMORY
        WatchProcess(firefox)
    else:
        fireboxbin = AttachProcess(project, 'firefox-bin')
        fireboxbin.max_memory = MAX_MEMORY

    orig_filename = project.application().getInputFilename("JPEG image filename")
    filename_ext = filenameExtension(orig_filename)
    AutoMangle(project, orig_filename, nb_file=NB_FILES)
    FuzzyHttpServer(project, PORT, filename_ext, rows=ROWS)
    FirefoxWindow(project)

from fusil.file_tools import filenameExtension
from fusil.network.http_server import HttpServer

from fusil.process.attach import AttachProcess
from fusil.process.create import CreateProcess
from fusil.process.watch import WatchProcess

from fusil.project_agent import ProjectAgent
from fusil.auto_mangle import AutoMangle
from datetime import datetime
from time import time
from fusil.x11 import (sendKey, getDisplay, findWindowByNameRegex,
    setupX11Process)
from Xlib.keysymdef.miscellany import XK_F5
import re
from os.path import basename

class FirefoxProcess(CreateProcess):
    def on_project_start(self):
        CreateProcess.init(self)
        self.createProcess()

    def on_project_done(self):
        self.destroyProcess()

    def init(self):
        if 1 < self.project().session_index:
            self.send('process_create', self)

    def deinit(self):
        pass

class HtmlPage:
    def __init__(self):
        self.title = None
        self.headers = []
        self.body = ''

    def __str__(self):
        html = ['<html>\n']
        if self.title or self.headers:
            html.append('  <head>\n')
            if self.title:
                html.append('    <title>%s</title>\n' % self.title)
            html.append('  </head>\n')
        html.append('<body>\n')
        html.append(self.body+"\n")
        html.append('</body>\n')
        html.append('</html>\n')
        return ''.join(html)

class FuzzyHttpServer(HttpServer):
    def __init__(self, project, name, filename_ext, rows=5):
        HttpServer.__init__(self, project, name)

        prefix = "file-"
        suffix = filename_ext
        if filename_ext in (".jpeg", ".jpg"):
            self.content_type = "image/jpeg"
            self.file_html_format = '<img src="%s" alt="%s">'
        elif filename_ext == ".swf":
            self.content_type = "application/x-shockwave-flash"
            self.file_html_format = '<embed src="%s" name="%s"></embed>'
        else:
            raise ValueError("Unknown file extension: %r" % filename_ext)
        self.file_url_format = prefix + "%04u" + suffix
        self.file_url_match = re.compile(re.escape(prefix) + "([0-9]+)" + re.escape(suffix)).match
        self.timeout = 2.0
        self.rows = rows

    def init(self):
        HttpServer.init(self)
        self.pages = set()
        self.filenames = None
        self.is_done = False
        self.done_at = None

    def on_mangle_filenames(self, filenames):
        self.filenames = filenames
        self.send('http_server_ready')

    def serveRequest(self, client, request):
        url = request.uri[1:]
        if not url:
            url = "index.html"

        page = url
        self.error("Serve URL=%r" % url)
        match = self.file_url_match(url)
        if match:
            file_index = int(match.group(1))
            filename = self.filenames[file_index]
            data = open(filename, 'rb').read()
            self.serveData(client, 200, "OK", data=data, content_type=self.content_type)
        elif url == "index.html":
            self.createHomepage(client)
        else:
            page = None
            self.error404(client, url)
        if page:
            self.pages.add(page)

        if (1+NB_FILES) <= len(self.pages) and not self.is_done:
            self.is_done = True
            self.done_at = time() + self.timeout

    def createHomepage(self, client):
        self.error("Serve homepage")
        page = HtmlPage()
        page.title = 'Fusil HTTP server'
        page.body = '<h1>Fuzzing</h1>'
        page.body += '<table border="1">'
        tr_open = False
        count = len(self.filenames)
        for index in xrange(count):
            url = self.file_url_format % index
            filename = basename(self.filenames[index])
            alt = "[%s]" % filename

            if (index % self.rows) == 0:
                if tr_open:
                    page.body += '</tr>'
                page.body += '<tr>'
                tr_open = True
            span = ''
            if index == (count-1):
                colspan = (index+1) % self.rows
                if colspan:
                    span += ' colspan="%s"' % (self.rows - colspan + 1)
            content = self.file_html_format % (url, alt)
            page.body += '<td%s>%s</td>' % (span, content)
        page.body += '</tr>'
        page.body += '</table>'
        page.body += '<p>Created: %s</p>' % datetime.now()
        page.body += '<p>Session: %s</p>' % self.project().session_index

        self.serveData(client, 200, "OK", data=str(page), content_type="text/html")

    def live(self):
        HttpServer.live(self)
        if not self.is_done:
            return
        if time() < self.done_at:
            return
        self.error("DONE")
        self.is_done = False
        self.send('session_stop')

class FirefoxWindow(ProjectAgent):
    def __init__(self, project):
        ProjectAgent.__init__(self, project, "firefox_window")
        self.display = getDisplay()
        self.root_window = self.display.screen().root
        self.F5_keycode = self.display.keysym_to_keycode(XK_F5)
        self.window = None

    def findWindow(self):
        if self.window:
            return
        self.window = findWindowByNameRegex(self.root_window, r"Mozilla Firefox$")

    def on_http_server_ready(self):
        if self.project().session_index == 1:
            return
        self.error("HTTP SERVER READY")
        self.findWindow()
        self.error("Send key F5 (%s) to Firefox window!" % self.F5_keycode)
        sendKey(self.window, self.F5_keycode, released=False) # 71=keycode of "F5" key (reload page)

