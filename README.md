# PythonOS
A quick and dirty operating system lookalike program made in Python, originally as a joke between myself and a friend in college a couple of years ago.

Prerequisites:
 - Some form of Python 3, but I'd recommend the latest.
 - For Linux, nano is required for the text editor, because I detest Vim. Sorry. And since macOS has it by default it makes things easier.
 - Windows has been tested for compatibility, but it *should* work on Linux and macOS as well.** Though, it's been a while since I last tested it.
 
**NOTE: There are a lot of bugs when used in Linux, macOS untested. I'll get on to fixing those as soon as I can.

This program uses some external programs and code:

 - Kinesics Text Editor by the Joe Lowe Project: http://turtlewar.org/projects/editor/
 - Colorama text colouring scripts by Arnon Yaari: https://github.com/tartley/colorama
 - Playsound sound playing script by Taylor Marks: https://github.com/TaylorSMarks/playsound

Note: I am currently looking into removing the Kinesics text editor requirement. No ETA on this however.

Changelog:

1.8d:
Fixed critical login bug. Reduced the time it takes for the prompt to appear and blank inputs at the prompt no longer trigger the "unknown command" text.

1.8a/b/c:
Added new playback command.
Changed apt-get to apt, like with the recent changes to Linux.
Changed .gitignore to also ignore text adventure save files.
Fixed some spelling errors in the text adventure game.
Changed the way edit works - instead of defaulting to the documents folder, it now allows you to edit any file in any directory.

1.8:
Finally removed the VLC requirement and switched to a much nicer audio player called Playsound. From over 300K to 4K, perfect.
Sorry for all the commits, still working this thing out :P
Some bugs may have crept in because of this, but it's currently 1:37am and I'm very tired.

1.7g:
Changed file structure. Help files are now .hlp, permanent text files (such as commands.txt) are now .lst files, and temporary text files are still .txt.
ScanDisk was modified to capitalise the "D" to make it just that little bit more like the Windows original.
Users folder was given a .gitignore to make sure GitHub actually sees it and uploads it, otherwise PythonOS will have a fit since it'll be missing.

1.7f:
Uploaded to GitHub, finally. Removed some unnecessary files from the upload and reset the program for first use.
Start of changelog. Sorry ;-;
