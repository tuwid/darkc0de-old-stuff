*****************
Mangle valid file
*****************

MangleFile
==========

To fuzz file parser, you can use MangleFile agent. It takes a valid file on
input and then injects errors to create invalid files. It can generate
multiple files for each session.

Operations
----------

 * replace: replace a byte by a random byte
 * bit: invert one bit value
 * special_value: replace one or more bytes to write a special value,
   eg. four bytes: "0xFF 0xFF 0xFF 0xFF"
 * insert_bytes: insert one or more random bytes
 * delete_bytes: delete one or more bytes


MangleConfig
------------

You can configure some options to help fuzzing using 'config' attribute of
MangleFile. The value is an instance of MangleConfig class. Options:

 * min_op: Minimum number of mangle operations (default: 1)
 * max_op: Maximum number of mangle operations (default: 10)
 * operations: List of operation name (default: ["replace", "bit", "special_value"])
 * max_insert_bytes: Maximum number of insered bytes (default: 8)
 * max_delete_bytes: Maximum number of deleted bytes (default: 8)
 * change_size: Allow operations which change data size (default: False)


Truncate
--------

You can limit maximum file size using 'max_size' attribute of MangleFile.
The value is the maximum number of bytes read from input file.

AutoMangle
==========

AutoMangle is an helper to MangleFile: it tries to find the best parameters
to fuzz the target using session aggressivity. Option attributes:

 * hard_min_op (default: 0): Minimum number of operations
 * hard_max_op (default: 10000): Maximum number of operations
 * fixed_size_factor (default: 1.0): ratio used to compute the number
   of operations depending on the file

IncrMangle
==========

IncrMangle is the incremental mangle agent. Whereas AutoMangle regenerates
all errors for each session, IncrMangle keeps errors between the sessions
and add some new errors. Option attributes:

 * operation_per_version: Maximum number of operations applied
   to new session
 * max_version: Maximum version number for a file, if a file
   is older max_version, the operations are truncated to a random number
   of versions
 * min_offset and max_offset (default None): Minimum and maximum file offset,
   both are optional (use None value)

Default values:

    >>> from fusil.mockup import Project, NullLogger
    >>> logger = NullLogger()
    >>> project = Project(logger)
    >>> from fusil.incr_mangle import IncrMangle
    >>> mangle = IncrMangle(project, 'filename')
    >>> mangle.operation_per_version
    1
    >>> mangle.max_version
    25
    >>> mangle.min_offset, mangle.max_offset
    (None, None)

