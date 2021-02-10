# {gtk-}blank-unused-screen.py

This repository contains two tiny utilities to blank the screen which is currently not in use. Quite often one wants to focus on one screen, and regularly but not permanently look at some reference materials on the other one. To blank it, e.g. to have less distraction or less eye strain due to brightness, these utilities can be used. Handy as well if one wants to watch a movie or play a game in a multi monitor setup and rather have non-main screens dark.

The repository contains two versions:

- `blank-unused-screen.py `written using Xlib. Reacts fast, but has few options. Licensed LGPL as Xlib.
- `gtk-blank-unused-screen.py` written using Gtk3, has a notification area icon and menu. Reacts a bit slower. Licensed BSD.

The tools are alpha quality and come without warranty whatsoever. Tested under Ubuntu Focal Fossa. (Try package `python3-xlib` for the first, and `gir1.2-appindicator3-0.1` for the second)