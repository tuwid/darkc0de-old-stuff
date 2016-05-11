   >>> filename = 'test.txt'
   >>> from fusil.mockup import Project
   >>> from fusil.file_watch import FileWatch
   >>> from StringIO import StringIO
   >>> output = open(filename, 'w', 0)
   >>> input = open(filename, 'r', 0)
   >>> project = Project()
   >>> watch = FileWatch(project, input, 'test')
   >>> watch.read_size = 1
   >>> watch.init()
   >>> list(watch.readlines())
   []
   >>> output.write('da'); output.flush()
   >>> list(watch.readlines())
   []
   >>> output.write('t'); output.flush()
   >>> list(watch.readlines())
   []
   >>> output.write('a\n'); output.flush()
   >>> list(watch.readlines())
   ['data']
   >>> output.write('linea\nlineb\n'); output.flush()
   >>> list(watch.readlines())
   ['linea', 'lineb']
   >>> output.write('line1\nline2\nline'); output.flush()
   >>> list(watch.readlines())
   ['line1', 'line2']
   >>> output.write('3\n'); output.flush()
   >>> list(watch.readlines())
   ['line3']

