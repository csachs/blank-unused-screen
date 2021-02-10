#!/usr/bin/env python3
#
# Copyright (C) 2017 Christian C. Sachs.
# 
# This library is free software; you can redistribute it and/or
# modify it under the terms of the GNU Lesser General Public
# License as published by the Free Software Foundation; either
# version 2.1 of the License, or (at your option) any later version.
# 
# This library is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the GNU
# Lesser General Public License for more details.
# 
# You should have received a copy of the GNU Lesser General Public
# License along with this library; if not, write to the Free Software
# Foundation, Inc., 51 Franklin Street, Fifth Floor, Boston, MA  02110-1301  USA
# 
# based upon Xlib examples, hence licensed LGPL

# see https://github.com/csachs/blank-unused-screen

__version__ = '0.0.1'

import sys
import time
from Xlib import X, display


def main():
    if len(sys.argv) == 1:
        print("Usage: %s <screen num>" % (sys.argv[0],))
        raise SystemExit

    screen_to_blank = int(sys.argv[1])

    print("Will show a black window on screen %d if it is not in use, press ctrl-c to end..." % (screen_to_blank,))

    d = display.Display()

    assert d.has_extension('XINERAMA')

    stb = d.xinerama_query_screens()._data['screens'][screen_to_blank]

    stb_x, stb_y, stb_w, stb_h = stb['x'], stb['y'], stb['width'], stb['height']
    stb_xmax, stb_ymax = stb_x+stb_w, stb_y+stb_h

    s = d.screen()
    sr = s.root

    while True:
        position = sr.query_pointer()._data
        x, y = (position['root_x'], position['root_y'])

        if stb_x <= x < stb_xmax and stb_y <= y < stb_ymax:
            pass
        else:
            window = sr.create_window(
                stb_x, stb_y, stb_w, stb_h, 0, s.root_depth,
                X.InputOutput,
                X.CopyFromParent,
                background_pixel=s.black_pixel,
                event_mask=(X.EnterWindowMask | 0),
                colormap=X.CopyFromParent,
                override_redirect=True,
            )

            window.map()
            d.next_event()
            window.destroy()

        time.sleep(0.1)


if __name__ == '__main__':
    main()

