"""\
Guitar
By Joe Esposito

Contains classes for storing and manipulating guitar tabs in a structured manor.
"""

from StringIO import StringIO

# TODO: Chord attributes: 1. ____ (play the chord one note at a time instead of all at once)
# 
# TODO: X\\ or X// is shorthand for slide to 0
# TODO:
#      ---0-
#      --0--
#      -0---
#   means strum up slowly
# TODO: --7b9-- and --7b(9)-- mean bend 7 up one whole step
#       --7b9--9r7-- mean bend 7 up one whole step and then release back down
#       --7b-- means bend up half fret's worth, ie. --7b(7.5)--
# TODO: --/7-9-7\-- means swoop in and leave, but slide from 7 to 9 to 7
# TODO: Harmonics with <X>, ex. <12>
# TODO: Optional notes with (X), ex. (3)
# TODO: Get songs with non-tab notation, ex. Am G  D

# Song class
class Song:
  """Class for Guitar Tab songs"""
  def __init__ (self, Artist = "", Title = "", Album = "", Author = "", Url = "", Source = "", Errors = []):
    self.Artist = Artist.title().replace(" Of ", " of ").replace(" A ", " a ").replace(" The ", " the ")
    self.Title = Title.title().replace(" Of ", " of ").replace(" A ", " a ").replace(" The ", " the ")
    self.Album = Album.title().replace(" Of ", " of ").replace(" A ", " a ").replace(" The ", " the ")
    self.Author = Author.title()
    self.Url = Url
    self.Source = Source
    self.Errors = Errors
    self.Staffs = []
    self.StaffsPerScore = 0
    self.ShowMeta = True
    self.ShowUrl = True
  
  def __str__ (self):
    head = ""
    if self.ShowMeta:
        if self.Artist: head += "Artist: %s\n" % self.Artist
        if self.Title: head += "Title: %s\n" % self.Title
        if self.Album: head += "Album: %s\n" % self.Album
        if self.Author: head += "Tabbed By: %s\n" % self.Author
        if self.ShowUrl and self.Url: head += "Url: %s\n" % self.Url
    body = ""
    for staff in self.Staffs:
      if (body != ""): body += "\n\n"
      body += str(staff)
    s = ""
    s += head
    if (head != "") and (body != ""): s += "\n"
    s += body
    return s
  
  def getScores (self):
    """Returns a list of scores"""
    scores = []
    i = 0
    while (i < len(self.Staffs)):
      scores.append(self.Staffs[i:i+self.StaffsPerScore])
      i += self.StaffsPerScore
    return scores
  Scores = property(getScores)
  
  def Score (self, page, staffsPerScore = None):
    """Returns a single score"""
    # FUTURE: Optimize
    return self.Scores[page]
  
  def Save (self, stream):
    """Saves a song to a stream"""
    # TODO: Saving
    raise NotImplementedError("Saving not yet implemented")
  
  def SaveFile (self, filename):
    """Saves a song to a file"""
    fd = open(filename, 'rb')
    Save()
    fd.close()


# Staff class
class Staff:
  """Class for Guitar Tab staffs"""
  def __init__ (self):
    self.BaseNotes = ( 'E', 'B', 'G', 'D', 'A', 'E' )
    self.Measures = []
  
  def __str__ (self):
    s = []
    for i in range(6):
      s.append(self.BaseNotes[i] + "|-")
    for measure in self.Measures:
      m = str(measure).split('\n')
      for i in range(6): s[i] += m[i]
    for i in range(6): s[i] += "-|"
    return '\n'.join(s)
  
  def Save (self, stream):
    # TODO: Saving
    raise NotImplementedError("Saving not yet implemented")
  
  # Saves a song to a file
  def SaveFile (self, filename):
    fd = open(filename, 'rb')
    Save()
    fd.close()


# Measure class
class Measure:
  """Class for Guitar Tab measures"""
  def __init__ (self):
    self.Chords = []
  
  def __str__ (self):
    s = [ "", "", "", "", "", "" ]
    # Find notes
    for chord in self.Chords:
      c = str(chord).split('\n')
      starts_with_digit = False
      for i in range(6):
        if (c[i].isdigit()): starts_with_digit = True
      for i in range(6):
        if (starts_with_digit) and (s[i] != ""): s[i] += "--"
        s[i] += c[i]
    return '\n'.join(s)


# Chord class
class Chord:
  """Class for Guitar Tab chords"""
  def __init__ (self):
    self.Notes = ( None, None, None, None, None, None )
    self.Attributes = ""
  
  def __str__ (self):
    notePre, noteVal, notePost = [], [], []
    sizePre, sizeVal, sizePost =  0,  0,  0
    for i in range(6):
      note = self.Notes[i]
      pre, val, post = "", "", ""
      if (note is not None):
        note, attr = note
        for a in attr:
          if (a == 'h') or (a == 'p') or (a == 'r') or (a == '/'): pre += a
          if (a == 'b') or (a == '~'): post += a
        val = str(note)
      notePre.append( pre )
      noteVal.append( val )
      notePost.append( post )
      sizePre, sizeVal, sizePost = max(len(pre), sizePre), max(len(val), sizeVal), max(len(post), sizePost)
    for i in range(6):
      notePre[i] = notePre[i].rjust(sizePre, '-')
      noteVal[i] = noteVal[i].rjust(sizeVal, '-')
      notePost[i] = notePost[i].ljust(sizePost, '-')
    s = ""
    for i in range(6):
      if (s != ""): s += "\n"
      s += notePre[i]
      s += noteVal[i]
      s += notePost[i]
    return s
  
  def getNoteAttributes (self):
    """Gets a 6-tuple of note attributes"""
    attr = ( None, None, None, None, None, None )
    for i in range(6):
      if (self.Notes[i] is None): continue
      attr[i] = self.Notes[i][1]
  NoteAttributes = property(getNoteAttributes)
  
  def getNoteValues (self):
    """Gets a 6-tuple of note values"""
    attr = ( None, None, None, None, None, None )
    for i in range(6):
      if (self.Notes[i] is None): continue
      attr[i] = self.Notes[i][0]
  NoteValues = property(getNoteValues)


def CreateSong (text, url = ""):
  """Creates a guitar tab song from a text fragment"""
  errors = []
  artist, title, album, author = "", "", "", ""
  
  def checkkey (line, *keys):
    """Local function to check a line for a key and return the value or None if not available"""
    lline = line.lower()
    for key in keys:
      if (lline.startswith(key.lower())):
        return line[len(key):].strip()
    return None
  
  # Parse loop
  fd = StringIO(text)
  staffstrings = []
  staffs = []
  while (True):
    line = fd.readline()
    if (line == ""): break
    line = line.strip()
    if (line == ""): continue
    
    # Find song artist
    s = checkkey(line, "artist:", "artist :", "artist-", "artist -")
    if (s): artist = s
    # Find song title
    s = checkkey(line, "song:", "song :", "song-", "song -", "title:", "title :", "title-", "title -")
    if (s): title = s
    # Find song album
    s = checkkey(line, "album:", "album :", "album-", "album -")
    if (s): album = s
    # Find song title
    s = checkkey(line, "tabbed by:", "tabbed by :", "tabbed by-", "tabbed by -")
    if (s): author = s
    line = line.lower()
    
    # Find song tabs
    if ((line.startswith("|-")
      or line.startswith("a-") or line.startswith("b-") or line.startswith("c-") or line.startswith("d-") or line.startswith("e-") or line.startswith("f-") or line.startswith("g-")
      or line.startswith("a:-") or line.startswith("b:-") or line.startswith("c:-") or line.startswith("d:-") or line.startswith("e:-") or line.startswith("f:-") or line.startswith("g:-")
      or line.startswith("a|-") or line.startswith("b|-") or line.startswith("c|-") or line.startswith("d|-") or line.startswith("e|-") or line.startswith("f|-") or line.startswith("g|-")
      or line.startswith("a||-") or line.startswith("b||-") or line.startswith("c||-") or line.startswith("d||-") or line.startswith("e||-") or line.startswith("f||-") or line.startswith("g||-")
      )):
      staffstrings.append( line[2:] )
      if (len(staffstrings) == 6):
        staffs.append( staffstrings )
        staffstrings = []
  fd.close()
  
  # Create guitar tab song
  song = Song(artist, title, album, author, url, text)
  # Create staffs
  for staff in staffs:
    s, e = CreateStaff(staff)
    song.Staffs.append( s )
    song.Errors.extend(errors)
  # Return song
  return song


def CreateStaff (staffstrings):
  """Creates a guitar tab staff from a text fragment"""
  errors = []
  
  # Failsafe
  if (len(staffstrings) != 6): raise ValueError("Parameter staffstrings should be a list of length 6; one line for each tab string on the staff")
  size = max(len(staffstrings[0]), len(staffstrings[1]), len(staffstrings[2]), len(staffstrings[3]), len(staffstrings[4]), len(staffstrings[5]))
  for j in range(len(staffstrings)): staffstrings[j] = staffstrings[j].ljust(size, ' ')
  
  # Find measures
  measurestrings = [ "", "", "", "", "", "" ]
  measures = []
  for i in range(size):
    if (staffstrings[0][i] == '|') and (staffstrings[1][i] == '|') and (staffstrings[2][i] == '|') and (staffstrings[3][i] == '|') and (staffstrings[4][i] == '|') and (staffstrings[5][i] == '|'):
      if (len(measurestrings[0]) > 0):
        measures.append( measurestrings )
        measurestrings = [ "", "", "", "", "", "" ]
    else:
      for j in range(6): measurestrings[j] += staffstrings[j][i]
  if (len(measurestrings[0]) > 0):
    measures.append( measurestrings )
  # Create guitar tab staff
  staff = Staff()
  # Create measures
  for measure in measures:
    m, e = CreateMeasure(measure)
    staff.Measures.append( m )
    errors.extend( e )
  return staff, errors


def CreateMeasure (measurestrings):
  """Creates a guitar tab staff from a text fragment"""
  errors = []
  
  # Failsafe
  if (len(measurestrings) != 6): raise ValueError("Parameter measurestrings should be a list of length 6; one line for each tab string on the staff")
  size = max(len(measurestrings[0]), len(measurestrings[1]), len(measurestrings[2]), len(measurestrings[3]), len(measurestrings[4]), len(measurestrings[5]))
  for j in range(len(measurestrings)): measurestrings[j] = measurestrings[j].ljust(size, ' ')
  
  def isempty (A):
    """Local function to determine whether or not a list is empty"""
    for a in A:
      if (a): return False
    return True
  
  # Find chords
  attr = [ "", "", "", "", "", "" ]
  attrs = [ attr[:] ]
  chord = [ "", "", "", "", "", "" ]
  chords = []
  for i in range(size):
    isbar = True
    isspace = True
    for j in range(6):
      ch = measurestrings[j][i].lower()
      if (ch != ' ') and (ch != '\t') and (ch != '\n'): isspace = False
      if (ch.isdigit()) or (ch == 'x') or (ch == 't') or (ch == '.'):
        chord[j] += ch
        isbar = False
      elif (ch == '-') or (ch == ' ') or (ch == '\t'):
        continue
      # Check for attributes
      elif (ch == 'h'): attr[j] += 'h'
      elif (ch == 'p'): attr[j] += 'p'
      elif (ch == 'b'): attrs[-1][j] += 'b'
      elif (ch == 'r'): attr[j] += 'r'
      elif (ch == '~'): attrs[-1][j] += '~'
      elif (ch == 'v'): attrs[-1][j] += '~'
      elif (ch == '/'): attr[j] += '/'
      elif (ch == '\\'):attr[j] += '/'
      elif (ch == 's'): attr[j] += '/'
      else: errors.append( "'%s' found in measure and is not recognized; tab may not be accurately formatted" % ch )
    if (isbar):
      if (not isempty(chord)):
        chords.append( chord )
        chord = [ "", "", "", "", "", "" ]
        attrs.append( attr )
        attr = [ "", "", "", "", "", "" ]
    if (isspace): break
  if (not isempty(chord)):
    chords.append( chord )
  for j in range(6): attrs[-1][j] += attr[j]
  # Create guitar tab measure
  measure = Measure()
  # Create measures
  for i in range(len(chords)):
    c, e = CreateChord(chords[i], attrs[i])
    measure.Chords.append( c )
    errors.extend( e )
  return measure, errors


def CreateChord (chordnotes, chordattrs):
  """Creates a guitar tab staff from a text fragment"""
  errors = []
  
  # Failsafe .. be sure chord has 6 strings (possible notes/attributes)
  if (len(chordattrs) != 6):
    errors.append( "attribute didnt have exactly 6 strings; tab may not be accurately formatted - %s" % str(chordattrs) )
    for k in range(6-len(chordattrs)): chordattrs.append( "" )
  if (len(chordnotes) != 6):
    errors.append( "chord didnt have exactly 6 strings; tab may not be accurately formatted - %s" % str(chordnotes) )
    for k in range(6-len(chordnotes)): chordnotes.append( "" )
  
  # Find notes
  notes = []
  for i in range(6):
    if (not chordnotes[i]):
      notes.append( None )
    else:
      ch = chordnotes[i]
      try:
        ch = int(chordnotes[i])
      except ValueError: pass
      notes.append( (ch, chordattrs[i]) )
  
  # Create the chord
  chord = Chord()
  chord.Notes = ( notes[0], notes[1], notes[2], notes[3], notes[4], notes[5] )
  return chord, errors
