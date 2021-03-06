# PythonOS
A quick and dirty operating system lookalike program made in Python, originally as a joke between myself and a friend in college a few years ago.

**Progress has paused on PythonOS for some time as I haven't had time to develop it.**

**Version 2.1 may be missing the features added as stated in the changelog.**

Prerequisites:
 - Some form of Python 3, but I'd recommend the latest.
 - For Linux, nano is required for the text editor currently. At some point I will add in the ability to ask the user on first run for their editor.
 - Windows has been tested for compatibility, but it *should* work on Linux and macOS as well. Though, it's been a while since I last tested it.
 - Pyobjc is needed for macOS to play sound correctly without spewing errors everywhere. PythonOS will attempt to do this for you, but be warned: this is untested. At worst it just won't install and you'll have no audio in PythonOS.
 - python-gst-1.0 is neede for Linux to play sound correctly. As of the 1/4/19, PythonOS does NOT install this for you.
 
**NOTE: macOS bugs have mostly been ironed out now. Linux remains mostly untested but should work better than version 1.9.**

This program uses some external programs and code:

 - Kinesics Text Editor by the Joe Lowe Project: http://turtlewar.org/projects/editor/
 - Colorama text colouring scripts by Arnon Yaari: https://github.com/tartley/colorama
 - Playsound sound playing script by Taylor Marks: https://github.com/TaylorSMarks/playsound

# Changelog:

2.1 (The Colours and Edit Update):
Colours are fixed now for macOS (and Linux too with any luck)!  
Updated readme.  
Added playsound.pyc to gitignore.
Fixed file editing in macOS.

2.0 (The macOS Update):
Fixed a bunch of issues. I can now test PythonOS properly on a real Mac!  
Fixed playback issues. Unfortunately macOS needs Pyobjc installed, but start.py now checks for this and helps you install it. However, this is currently untested so it may work just fine, or it might explode.  
Fixed permission complaints when resetting PythonOS.  
Fixed *nix directory listings. Someone decided hard-coding "dir" was a good idea...  
Edit command fixed on macOS.  
Added new titles for macOS (and I would imagine Linux too) in start.py and PythonOS.py.  
Fixed user listings (grumble grumble dir on *nix grumble...) . 
Updated build number and time.  
Added a couple more files for git to ignore.  
Updated readme slightly (edit: slightly more).  

1.9:
Various tweaks.

1.8d:
Fixed critical login bug. Reduced the time it takes for the prompt to appear and blank inputs at the prompt no longer trigger the "unknown command" text.

1.8a/b/c:
Added new playback command.
Changed apt-get to apt, like with the recent changes to Linux.
Changed .gitignore to also ignore text adventure save files.
Fixed some spelling errors in the text adventure game.
Changed the way edit works - instead of defaulting to the documents folder, it now allows you to edit any file in any directory.

1.8:
Finally removed the VLC requirement and switched to a much nicer audio player called Playsound. 300K to 4K file size reduction.

1.7g:
Changed file structure. Help files are now .hlp, permanent text files (such as commands.txt) are now .lst files, and temporary text files are still .txt.
ScanDisk was modified to capitalise the "D" to make it just that little bit more like the Windows original.
Users folder was given a .gitignore to make sure GitHub actually sees it and uploads it, otherwise PythonOS will have a fit since it'll be missing.

1.7f:
Uploaded to GitHub, finally. Removed some unnecessary files from the upload and reset the program for first use.
Start of GitHub changelog.

# Known Issues - these may be incorrect currently
- Version number not updated to 2.1.
- Colour issues with Scandisk when run with the "runtests" command. (color not found error in macOS/Linux)
- Sound issues with Linux (tested on Raspbian) - python-gst-1.0 missing (need to implement checks for that)
