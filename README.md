# PythonOS
A quick and dirty operating system lookalike program made in Python, originally as a joke between myself and a friend in college a couple of years ago.

Prerequisites:
 - Some form of Python 3, but I'd recommend the latest.
 - VLC is optional, but the program will report sound playback issues at startup.
 - Make sure you install the VLC version appropriate for your architecture (32bit VLC on 64bit Windows will not work for some reason).
 - For Linux, nano is required for the text editor, because I detest Vim. Sorry. And since macOS has it by default it makes things easier.
 - Windows has been tested for compatibility, but it *should* work on Linux and macOS as well. Though, it's been a while since I last tested it.

This program uses some external programs and code:

 - VLC loader program by the VideoLan Project: https://wiki.videolan.org/PythonBinding
 - Kinesics Text Editor by the Joe Lowe Project: http://turtlewar.org/projects/editor/

Note: I am currently looking into removing the VLC requirement as it's clunky and very big. No ETA on this however.

Changelog:

1.7g:
Changed file structure. Help files are now .hlp, permanent text files (such as commands.txt) are now .lst files, and temporary text files are still .txt.
ScanDisk was modified to capitalise the "D" to make it just that little bit more like the Windows original.
Users folder was given a .gitignore to make sure GitHub actually sees it and uploads it, otherwise PythonOS will have a fit since it'll be missing.

1.7f:
Uploaded to GitHub, finally. Removed some unnecessary files from the upload and reset the program for first use.
Start of changelog. Sorry ;-;