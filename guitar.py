"""\
Guitar
By Joe Esposito

Contains classes for storing and manipulating guitar tabs in a structured manor.
"""

from collections import OrderedDict
from itertools import product
from StringIO import StringIO

# TODO: str(song), len(song.staffs), song.song_info, song.errors
# def __str__(self):
#     head = str(self.song_info) if self.show_meta else ''
#     body = '\n\n'.join(map(str, self.Staffs))
#     return head + ('\n' if head and body else '') + body


class Song(object):
    """Represents a guitar tablature."""
    def __init__(self, staffs=[], show_meta=True):
        self.staffs = staffs
    
    @staticmethod
    def parse(s):
        """Parses the specified string and creates a guitar tab song."""
        postfixes = ':', ' :', '-', ' -'
        errors = []
        staffs = []
        fd = StringIO(s)
        try:
            staffstrings = []
            for line in fd:
                line = line.strip()
                if line == '': continue
                # Find song tabs
                line = line.lower()
                staff_prefixes = ['|-'] + map(''.join, product('abcdefg', ['-', ':-', '|-', '||-']))
                if not starts_with_any(line, staff_prefixes):
                    continue
                staffstrings.append(line[2:])
                if len(staffstrings) < 6:
                    continue
                staff, staff_errors = Staff.create(staffstrings)
                staffs.append(staff); errors += staff_errors
                staffstrings = []
        finally:
            fd.close()
        return Song(staffs), errors
    
    def __str__(self):
        return '\n\n'.join(map(str, self.staffs))


class SongInfo(object):
    """Contains information about a song."""
    def __init__(self, artist=None, title=None, album=None, author=None, url=None):
        self.artist = artist
        self.title = title
        self.album = album
        self.author = author
        self.url = url
        self.show_url = False
    
    @staticmethod
    def extract(s):
        """Extracts song information from a string."""
        def value_of_any(line, keys):
            """Local function to check a line for a key and return the value or None if not available"""
            lowerline = line.lower()
            for key in keys:
                if lowerline.startswith(key.lower()):
                    return line[len(key):].strip()
            return None
        song_info = SongInfo()
        fd = StringIO(s)
        try:
            for line in fd:
                line = line.strip()
                if line == '': continue
                # Parse song info
                s = value_of_any(line, map(''.join, product(['artist'], postfixes)))
                if s: song_info.artist = s
                s = value_of_any(line, map(''.join, product(['song', 'title'], postfixes)))
                if s: song_info.title = s
                s = value_of_any(line, map(''.join, product(['album'], postfixes)))
                if s: song_info.album = s
                s = value_of_any(line, map(''.join, product(['tabbed by'], postfixes)))
                if s: song_info.author = s
        finally:
            fd.close()
        return song_info
    
    def __str__(self):
        labels = OrderedDict([('artist', 'Artist'), ('title', 'Title'), ('album', 'Album'), ('author', 'Tabbed by'), ('url', 'Url')])
        values = map(lambda key: getattr(self, key), labels)
        items = filter(lambda x: x[1], zip(labels.keys(), values))
        return '\n'.join(map(lambda item: ': '.join(item), items))


class Staff(object):
    """Class for Guitar Tab staffs."""
    def __init__(self, measures=[]):
        self.measures = measures
    
    # TODO: Tuning
    base_notes = 'E', 'B', 'G', 'D', 'A', 'E'
    
    @staticmethod
    def create(staffstrings):
        """Creates a guitar tab staff from a text fragment."""
        if len(staffstrings) != 6:
            raise ValueError('Parameter staffstrings should be a list of length 6, one line for each tab string on the staff.')
        
        # Find max staff size and normalize
        size = max(map(len, staffstrings))
        staffstrings = map(lambda s: s.ljust(size), staffstrings)
        
        # Find measures
        errors = []
        measurestrings = [''] * 6
        measures = []
        for i in range(size):
            if not any(map(lambda s: s[i] == '|', staffstrings)):
                for j in range(6):
                    measurestrings[j] += staffstrings[j][i]
            elif len(measurestrings[0]) > 0:
                measure, measure_errors = Measure.create(measurestrings)
                if not measure.is_empty:
                    measures.append(measure)
                errors += measure_errors
                measurestrings = [''] * 6
        if len(measurestrings[0]) > 0:
            measure, measure_errors = Measure.create(measurestrings)
            if not measure.is_empty:
                measures.append(measure)
            errors += measure_errors
        return Staff(measures), errors
    
    def __str__(self):
        start = map(''.join, product(Staff.base_notes, ['|-']))
        ends = ['-|'] * 6
        s = [''] * 6
        for measure in self.measures:
            m = str(measure).split('\n')
            for i in range(len(s)):
                if s[i] != '': s[i] += '-|-'
                s[i] += m[i]
        s = map(''.join, zip(start, s, ends))
        return '\n'.join(s)


class Measure(object):
    """Class for Guitar Tab measures."""
    def __init__(self, chords=[]):
        self.chords = chords or []
        self.is_empty = len(self.chords) == 0 or all(map(lambda note_list: not note_list, self.chords))
    
    @staticmethod
    def create(measurestrings):
        """Creates a guitar tab staff from a text fragment."""
        if len(measurestrings) != 6:
            raise ValueError('Parameter measurestrings should be a list of length 6, one line for each tab string on the staff.')
        size = max(map(len, measurestrings))
        measurestrings = map(lambda s: s.ljust(size), measurestrings)
        
        # Find chords
        errors = []
        note_attr_list = [''] * 6
        note_attr_lists = [list(note_attr_list)]
        note_list = [''] * 6
        note_lists = []
        for i in range(size):
            isbar = True
            isspace = True
            for j in range(6):
                ch = measurestrings[j][i].lower()
                if ch != ' ' and ch != '\t' and ch != '\n': isspace = False
                if ch.isdigit() or ch == 'x' or ch == 't' or ch == '.':
                    note_list[j] += ch
                    isbar = False
                elif ch == '-' or ch == ' ' or ch == '\t':
                    continue
                # Check for attributes
                elif ch == 'h': note_attr_list[j] += 'h'
                elif ch == 'p': note_attr_list[j] += 'p'
                elif ch == '^': note_attr_list[j] += 'p'
                elif ch == 'b': note_attr_lists[-1][j] += 'b'
                elif ch == 'r': note_attr_list[j] += 'r'
                elif ch == '~': note_attr_lists[-1][j] += '~'
                elif ch == 'v': note_attr_lists[-1][j] += '~'
                elif ch == '/': note_attr_list[j] += '/'
                elif ch == '\\':note_attr_list[j] += '/'
                elif ch == 's': note_attr_list[j] += '/'
                else: errors.append("'%s' found in measure and is not recognized; tab may not be accurately formatted" % ch)
            if isbar and any(note_list):
                note_lists.append(note_list)
                note_list = [''] * 6
                note_attr_lists.append(note_attr_list)
                note_attr_list = [''] * 6
            if isspace:
                break
        if any(note_list):
            note_lists.append(note_list)
        for j in range(len(note_attr_list)):
            note_attr_lists[-1][j] += note_attr_list[j]
        # Create chords
        chords = []
        for i in range(len(note_lists)):
            chord, chord_errors = Chord.create(note_lists[i], note_attr_lists[i])
            chords.append(chord)
            errors += chord_errors
        return Measure(chords), errors
    
    def __str__(self):
        s = [''] * 6
        for chord in self.chords:
            note_list = str(chord).split('\n')
            starts_with_digit = any(map(lambda x: starts_with_any(x, '0123456789'), note_list))
            for i in range(6):
                if starts_with_digit and s[i] != '': s[i] += "--"
                s[i] += note_list[i]
        return '\n'.join(s)


class Chord(object):
    """Class for Guitar Tab chords."""
    def __init__(self, notes_and_attributes=None):
        self.notes_and_attributes = tuple(notes_and_attributes) if notes_and_attributes else (None,) * 6
    
    @staticmethod
    def create(note_list, note_attr_list):
        """Creates a guitar tab staff from a text fragment."""
        errors = []
        if len(note_attr_list) != 6:
            errors.append('attribute didnt have exactly 6 strings; tab may not be accurately formatted - ' + str(note_attr_list))
            note_attr_list = note_attr_list[:6] + [''] * (6 - len(note_attr_list[:6]))
        if len(note_list) != 6:
            errors.append('chord didnt have exactly 6 strings; tab may not be accurately formatted - ' + str(note_list))
            note_list = note_list[:6] + [''] * (6 - len(note_list[:6]))
        return Chord(zip(map(parse_int_or_string, note_list), note_attr_list)), errors
    
    def __str__(self):
        notePre, noteVal, notePost = [], [], []
        sizePre, sizeVal, sizePost =  0,  0,  0
        for i in range(6):
            note_and_attribute = self.notes_and_attributes[i]
            pre, val, post = '', '', ''
            if note_and_attribute is not None:
                note, attr = note_and_attribute
                for a in attr:
                    if a == 'h' or a == 'p' or a == 'r' or a == '/':
                        pre += a
                    if a == 'b' or a == '~':
                        post += a
                val = str(note)
            notePre.append(pre)
            noteVal.append(val)
            notePost.append(post)
            sizePre, sizeVal, sizePost = max(len(pre), sizePre), max(len(val), sizeVal), max(len(post), sizePost)
        for i in range(6):
            notePre[i] = notePre[i].rjust(sizePre, '-')
            noteVal[i] = noteVal[i].rjust(sizeVal, '-')
            notePost[i] = notePost[i].ljust(sizePost, '-')
        s = ''
        for i in range(6):
            if s != '':
                s += '\n'
            s += notePre[i]
            s += noteVal[i]
            s += notePost[i]
        return s


def parse_int_or_string(s):
    """Parse an integer or return the original string if it cannot be done."""
    try:
        return int(s)
    except ValueError:
        return s


def starts_with_any(s, prefixes):
    for prefix in prefixes:
        if s.startswith(prefix):
            return True
    return False
