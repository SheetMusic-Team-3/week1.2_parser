""" To generate a PDF version of sheet music from the info generated from the semantic model:
    1. Download LilyPond (http://lilypond.org/index.html)
    2. Copy the output of the semantic model into plain text (you can just paste it into spotlight or the google search bar to do this)
    3. Run the generate_music function with the plain text output
    4. Open the generated .ly (LilyPond) file, and compile (command + R)
"""

## Test input:

"""
clef-treble
    
keySignature-EbM
    
timeSignature-2/4
    
multirest-23
    
barline
    
rest-quarter
    
rest-eighth
    
note-Bb4_eighth
    
barline
    
note-Bb4_quarter.
    
note-G4_eighth
    
barline
    
note-Eb5_quarter.
    
note-D5_eighth
    
barline
    
note-C5_eighth
    
note-C5_eighth
    
rest-quarter
    
barline
"""


""" Dictionary to translate fraction to int """
lengthToNum = {
    "whole"        : 1,
    "half"         : 2,
    "quarter"      : 4,
    "eighth"       : 8,
    "sixteenth"    : 16,
    "thirtysecond" : 32,
    "sixtyfourth"  : 64
}

""" Dictionary to translate model representation of notes
    to LilyPond representation of notes"""
letterToNote = {
    "C"  : "c",
    "C#" : "cis",
    "Cb" : "ces",
    "D"  : "d",
    "D#" : "dis",
    "Db" : "des",
    "E"  : "e",
    "E#" : "eis",
    "Eb" : "ees",
    "F"  : "f",
    "F#" : "fis",
    "Fb" : "fes",
    "G"  : "g",
    "G#" : "gis",
    "Gb" : "ges",
    "A"  : "a",
    "A#" : "ais",
    "Ab" : "aes",
    "B"  : "b",
    "B#" : "bis",
    "Bb" : "bes"
} # need to add double sharps double flats etc.


def parser(string):
    """Parses each command output of the semantic model. Returns the equivalent LilyPond command
    """
    divided_string = string.split("-")

    # I'm not sure how clefs
    if divided_string[0] == "clef":
        if divided_string[1] == "C1"
        return "\\clef soprano \n"
        else
        return "\\clef " + divided_string[1] + " \n"
    
    elif divided_string[0] == "keySignature":
        if len(divided_string[1]) == 1:
            return "\\key " + divided_string[1] + "\n"
        elif (len(divided_string[1]) == 2) and (divided_string[1][1] == "M"):
            return "\\key " + divided_string[1][1] + " \\major \n"
        elif (len(divided_string[1]) == 2) and (divided_string[1][1] == "m"):
            return "\\key " + divided_string[1][1] + " \\minor \n"
        elif (len(divided_string[1]) == 2) and (divided_string[1][1] == "m"):
            return "\\key " + divided_string[1] + "\n"
        elif (len(divided_string[1]) == 3) and (divided_string[1][2] == "M"):
            return "\\key " + divided_string[1][1:2] + " \\major \n"
        elif (len(divided_string[1]) == 3) and (divided_string[1][2] == "m"):
            return "\\key " + divided_string[1][1:2] + " \\minor \n"
    
    elif divided_string[0] == "timeSignature":
        return "\\time " + divided_string[1] + "\n"

    # is this the number of beats or the number of measures??
    elif divided_string[0] == "multirest":
        return "\\compressMMRest { \n \t R1*" + divided_string[1] + "\n } "
    
    elif divided_string[0] == "barline":
        return " "

    elif divided_string[0] == "rest":
        return "r" + str(lengthToNum[divided_string[1]]) + " "

    elif divided_string[0] == "note":
        note_info = divided_string[1].split("_")
        if int(note_info[0][-1]) == 3:
            return letterToNote[note_info[0][:-1]] + str(lengthToNum[note_info[1]])
        elif int(note_info[0][-1]) < 3:
            return letterToNote[note_info[0][:-1]] + (3 - int(note_info[0][-1])) * "\," + str(lengthToNum[note_info[1]])
        elif int(note_info[0][-1]) > 3:
            return letterToNote[note_info[0][:-1]] + (int(note_info[0][-1]) - 3) * "\'" + str(lengthToNum[note_info[1]])


def generate_music(model_output, piece_title):
    """generate_music calls the parser to parse the input and sends it to a LilyPond file to generate a PDF
       Model_output is the string output produced by the semantic model, unedited
       Piece_title provides the title of the piece, which becomes the filename
    """
    element_list = model_output.split(" \t ")
    print(element_list)

    f = open(piece_title + ".ly", "w+")
    f.write("\\version \"2.20.0\" \n\header{\n  title = \"" + piece_title + "\"\n}\n{\n")

    for x in range(len(element_list)):
        f.write(parser(element_list[x]))

    f.write("}") 
    f.close()
