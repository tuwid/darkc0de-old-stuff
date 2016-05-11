from random import choice, randint

# ASCII codes 0..255
ASCII8 = set(''.join( chr(code) for code in xrange(0, 255+1) ))

# ASCII codes 1..255
ASCII0 = set(''.join( chr(code) for code in xrange(1, 255+1) ))

# ASCII codes 1..127
ASCII7 = set(''.join( chr(code) for code in xrange(1, 127+1) ))

# ASCII codes 32..127
PRINTABLE_ASCII = set(''.join( chr(code) for code in xrange(32, 127+1) ))

# Letters and digits
UPPER_LETTERS = set('ABCDEFGHIJKLMNOPQRSTUVWXYZ')
LOWER_LETTERS = set('abcdefghijklmnopqrstuvwxyz')
LETTERS = UPPER_LETTERS | LOWER_LETTERS
DECIMAL_DIGITS = set('0123456789')
HEXADECIMAL_DIGITS = DECIMAL_DIGITS | set('abcdefABCDEF')
PUNCTUATION = set(' .,-;?!:(){}[]<>\'"/\\')

class BytesGenerator:
    def __init__(self, min_length, max_length, bytes_set=ASCII8):
        self.min_length = min_length
        self.max_length = max_length
        self.bytes_set = bytes_set

    def createLength(self):
        return randint(self.min_length, self.max_length)

    def createValue(self, length=None):
        if length is None:
            length = self.createLength()
        bytes_list = list(self.bytes_set)
        return ''.join( choice(bytes_list) for index in xrange(length) )

class UnsignedGenerator(BytesGenerator):
    """Unsigned integer"""
    def __init__(self, max_length=40, bytes_set=DECIMAL_DIGITS):
        # 2^32 length in decimal: 10 digits
        # 2^64 length in decimal: 20 digits
        # 2^128 length in decimal: 39 digits
        BytesGenerator.__init__(self, 1, max_length, bytes_set)

    def createValue(self, length=None):
        if length is None:
            length = self.createLength()
        first_digit = list(self.bytes_set - set('0'))
        bytes_list = list(self.bytes_set)
        if 2 <= length:
            return choice(first_digit) + ''.join( choice(bytes_list) for index in xrange(length-1) )
        else:
            return ''.join( choice(bytes_list) for index in xrange(length) )

class IntegerGenerator(UnsignedGenerator):
    """Signed integer"""
    def __init__(self, max_length=40, bytes_set=DECIMAL_DIGITS):
        # 2^32 length in decimal: 10 digits
        # 2^64 length in decimal: 20 digits
        # 2^128 length in decimal: 39 digits
        UnsignedGenerator.__init__(self, max_length)

    def createValue(self, length=None):
        value = UnsignedGenerator.createValue(self, length=length)
        if randint(0, 1) == 1:
            return "-" + value
        else:
            return value

class LengthGenerator(BytesGenerator):
    def __init__(self, max_length):
        BytesGenerator.__init__(self, 1, max_length, set('A'))

class UnixPathGenerator(BytesGenerator):
    def __init__(self, max_length=None):
        if not max_length:
            max_length = 5000
        BytesGenerator.__init__(self, 1, max_length)
        charset = PRINTABLE_ASCII - set('/\x7f')
        charset = UPPER_LETTERS | LOWER_LETTERS | DECIMAL_DIGITS | set('-_.')
        self.filename_length = 100
        self.filename_generator = BytesGenerator(1, 1, charset)
        self.change_dir = (".", "..")

    def createValue(self, length=None):
        if length is None:
            length = self.createLength()
        path = []
        path_len = 0
        while path_len < length:
            if not path:
                # Absolute path? (25%)
                use_slash = (randint(0, 4) == 0)
            elif path[-1] == '/':
                # Add double slash, eg. /a/b// ? (10%)
                use_slash = (randint(0, 9) == 0)
            else:
                use_slash = True

            if use_slash:
                part = '/'
            else:
                filelen = min(randint(1, length - path_len), self.filename_length)
                if randint(0, 9) != 0:
                    # Filename
                    part = self.filename_generator.createValue(length=filelen)
                else:
                    # "." or ".."
                    part = choice(self.change_dir)
            path.append(part)
            path_len += len(part)
        return ''.join(path)

        bytes_list = list(self.bytes_set)
        return ''.join( choice(bytes_list) for index in xrange(length) )

