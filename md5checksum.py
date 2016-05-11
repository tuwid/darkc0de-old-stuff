#!/usr/bin/python

"""Check file integrity using md5sum.txt files, with progress feedback.

Usage: md5sum.py [options] file ...

    -h, --help
        Print this help text.
        
    -o, --output file
        Write output to "file".
        
    -c, --check
        Check checksum files, instead of creating them.

    -t, --trim
        Trim away the longest common directory prefix of filenames when
        creating a checksum file. This allows the command
        "md5sum.py -t ~/public_html > md5sum.txt" to work as expected:
        inside md5sum.txt filenames are relative to ~/public_html and not
        absolute.

    -b, --base directory
        When checking, make relative pathnames be relative to 'directory',
        not the directory in which md5sum.txt is found. This is sort of
        the reverse of --trim. If md5sum.txt has been created as in the
        example for --trim, the command "md5sum.py -c
        --base b ~/public_html md5sum.txt" works correctly.

    -q, --quiet
        Do not report progress.

    -v, --verbose
        Report progress with more detail when checking.

Input filenames can be directories, the program will automatically recurse
into them and find files within. When checking, the input file should be
of similar format as what this program outputs, though some heuristics are
applied to ignore obvious problems.

Version: $Revision: 1.18 $

Lars Wirzenius <liw@iki.fi>"""


import md5
import sys
import os
import string
import re
import getopt
import time


# Verbosity values.
QUIET = 0
NORMAL = 1
VERBOSE = 2


# Format a size in bytes in a form easily read by a human.

def format_size(bytes):
    units = [
        # tuples: (unit name, unit size, significant decimals)
        # we want enough decimals to make the output change often so the
        # user sees action happening
        ("GB", 1024.0 * 1024.0 * 1024.0, 3),
        ("MB", 1024.0 * 1024.0, 2),
        ("kB", 1024.0, 0),
    ]
    
    for name, size, decimals in units:
        if bytes >= size:
            return "%.*f %s" % (decimals, bytes / size, name)
    return "%d B" % bytes


# Parse a line in an md5sum.txt file. Return (checksum, filename) if found,
# (None, None) otherwise. There seems to be no official spec for the format,
# but this parsing worked with many files.

def parse_line(line):
    m = re.match(r"^(?P<md5>[0-9a-zA-Z]{32})\s+(?P<filename>.+)$", line)
    if m:
    	return m.group("md5"), m.group("filename")
    else:
    	return None, None


# Parse an md5sum.txt file (e.g., our own output). Ignore lines that don't
# look like checksum lines. Return a list of (checksum, filename) pairs.

def parse_md5sum_txt(base_dir, md5sum_txt):
    list = []
    for line in md5sum_txt.split("\n"):
    	md5sum, filename = parse_line(line)
	if not md5sum:
	    continue
        # Some programs (on Windows?) seem to add an asterix in some cases.
        if filename[:1] == "*" and len(filename) > 1:
            filename = filename[1:]
	if os.path.isabs(filename):
	    abspath = filename
	else:
	    abspath = os.path.abspath(os.path.join(base_dir, filename))
    	abspath = os.path.normpath(abspath)
    	list.append((md5sum, abspath))
    return list


# Stuff for writing out status messages to a terminal (needs to obey
# backspace character). These fail if the terminal width is shorter than
# the status message, but who cares.

status_file = sys.stderr
latest_status = ""
latest_status_time = 0.0

def unprint_status():
    if status_file:
        global latest_status
        status_file.write("\b \b" * len(latest_status))
        status_file.flush()
        latest_status = ""

def print_status(msg):
    if status_file:
        global latest_status
        unprint_status()
        latest_status = msg
        status_file.write(latest_status)
        status_file.flush()
        global latest_status_time
        latest_status_time = time.time()

# Sometimes it is useful to restrict the rate of status updating, so that 
# things are more readable and less disturbing. Also, this reduces the
# amount of work a terminal emulator has to do, which is good for not
# wasting cycles, since drawing text is a tad slow.

def print_timed_status(msg):
    if time.time() - latest_status_time >= 1.0:
        print_status(msg)


# Compute the checksum for a file. Most of the arguments have to do with
# reporting progress to user. Return the checksum and total amount of
# bytes read.

def compute_md5(prefix, filename, files_done, files_total, bytes_done, 
                bytes_total, suffix):
    m = md5.new()
    f = open(filename, "rb")
    while 1:
	data = f.read(4*1024)
	if not data:
	    break
	m.update(data)
	bytes_done += len(data)
    	print_timed_status(("%s: file %d of %d, %s of %s, " +
    	                    "%d %% done%s") %
   		  	   (prefix, files_done + 1, 
   		  	   files_total, 
   		  	   format_size(bytes_done),
   		  	   format_size(bytes_total),
			   100.0 * float(bytes_done) / bytes_total, 
			   suffix))
    f.close()
    return m.hexdigest(), bytes_done


# Figure out the total size of a set of files.

def find_total_size(filenames):
    total_size = 0
    for i in range(len(filenames)):
        print_timed_status("Finding file sizes: file %d of %d" % 
        	           (i+1, len(filenames)))
    	try:
	    total_size += os.path.getsize(filenames[i])
	except os.error:
	    pass
    return total_size


# Check files against an md5sum.txt file. Report errors to user.

def check(base_dir, md5sum_txt, verbosity):
    pairs = parse_md5sum_txt(base_dir, md5sum_txt)
    
    filenames = map(lambda pair: pair[1], pairs)
    total_size = find_total_size(filenames)

    bytes_done = 0
    error_count = 0
    for i in range(len(pairs)):
    	md5sum, filename = pairs[i]
	try:
	    computed, bytes_done = compute_md5("Checking", 
	                                       filename, 
	                                       i, 
                                               len(pairs), 
                                               bytes_done,
                                               total_size, 
                                               ", %d errors" % error_count)
    	except IOError:
	    unprint_status()
	    sys.stderr.write("Error: I/O error reading %s\n" % filename)
	    error_count += 1
	else:
	    if md5sum.lower() != computed.lower():
	        error_count += 1
		unprint_status()
		sys.stderr.write("Error: MD5 checksum mismatch for %s\n" % 
		    	    	 filename)
            elif verbosity == VERBOSE:
                unprint_status()
                sys.stderr.write("%s\tOK\n" % filename)

    unprint_status()
    if verbosity != QUIET:
        sys.stderr.write("Checked %d files, %d errors.\n" % 
                         (len(pairs), error_count))


# Expand list of filenames so that the names that are actually files are
# replaced with the list of files in the directories.

def expand_directories(filenames):
    list = []
    total = len(filenames)
    for i in range(total):
        filename = filenames[i]
        print_timed_status("Finding files in subdirectories (%d of %d)" % 
                           (i+1, total))
        if os.path.isdir(filename):
            for dirname, subdirs, basenames in os.walk(filename):
                for basename in basenames:
                    list.append(os.path.join(dirname, basename))
        else:
            list.append(filename)
    return list


# Find the length of the longest common directory name prefix for a list
# of filenames.

def find_trim_length(filenames):
    commonprefix = os.path.commonprefix(filenames)
    if commonprefix == "":
        return 0
    if commonprefix[-1] == os.sep:
        return len(commonprefix)
    i = commonprefix.rfind(os.sep)
    return i + 1


# Create an md5sum.txt file.

def create(output_name, trim_p, filenames):
    filenames = expand_directories(filenames)
    total_size = find_total_size(filenames)
    trim_length = find_trim_length(filenames)
    bytes_done = 0
    checksums = []

    # We need to create the output file only after finding all input files!
    # However, we'll create it before computing the checksums so that an
    # error will be noticed faster.
    if output_name:
        output = file(output_name, "w")
    else:
        output = sys.stdout

    for i in range(len(filenames)):
	try:
	    checksum, bytes_done = compute_md5("Computing",
	                                       filenames[i], i, len(filenames), 
	    	    	    	    	       bytes_done, total_size, "")
    	except IOError:
	    unprint_status()
	    sys.stderr.write("Error: I/O error reading %s\n" % filenames[i])
        else:
            checksums.append((checksum, filenames[i][trim_length:]))
    unprint_status()
    for checksum, filename in checksums:
        output.write("%s  %s\n" % (checksum, filename))

    if output != sys.stdout:
        output.close()


def main():
    settings = {
        "create": 1,
        "output": None,
        "verbosity": NORMAL,
        "trim": 0,
        "base": "",
    }
    
    try:
        opts, args = getopt.getopt(sys.argv[1:], 
                                   "hcqvto:b:", 
                                   ["help", "check", "quiet", "verbose", 
                                    "trim", "output=", "base="])
    except getopt.GetoptError, detail:
        sys.stderr.write("Error: %s\n" % detail)
        sys.exit(1)
    for opt, optarg in opts:
        if opt in ["-c", "--check"]:
            settings["create"] = 0
        elif opt in ["-b", "--base"]:
            settings["base"] = optarg
        elif opt in ["-o", "--output"]:
            settings["output"] = optarg
        elif opt in ["-q", "--quiet"]:
            settings["verbosity"] = QUIET
        elif opt in ["-v", "--verbose"]:
            settings["verbosity"] = VERBOSE
        elif opt in ["-t", "--trim"]:
            settings["trim"] = 1
        elif opt in ["-h", "--help"]:
            print __doc__,
            sys.exit(0)

    if not args:
        sys.stderr.write(__doc__)
        sys.exit(1)

    if settings["verbosity"] == QUIET:
        global status_file
        status_file = None

    if settings["create"]:
        create(settings["output"], settings["trim"], args)
    else:
        for filename in args:
            f = open(filename, "r")
            data = f.read()
            f.close()
            check(settings["base"] or os.path.dirname(filename) or ".", data, 
                  settings["verbosity"])


if __name__ == "__main__":
    main()
