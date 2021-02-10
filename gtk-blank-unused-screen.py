#!/usr/bin/env python3
#
# Copyright (c) 2017 Christian C. Sachs.
# All rights reserved.
#
# Redistribution and use in source and binary forms, with or without
# modification, are permitted provided that the following conditions are met:
#
# 1. Redistributions of source code must retain the above copyright notice, this
#    list of conditions and the following disclaimer.
# 2. Redistributions in binary form must reproduce the above copyright notice,
#    this list of conditions and the following disclaimer in the documentation
#    and/or other materials provided with the distribution.
#
# THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS "AS IS" AND
# ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE IMPLIED
# WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE ARE
# DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT OWNER OR CONTRIBUTORS BE LIABLE FOR
# ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR CONSEQUENTIAL DAMAGES
# (INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR SERVICES;
# LOSS OF USE, DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER CAUSED AND
# ON ANY THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY, OR TORT
# (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE OF THIS
# SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.
#

# see https://github.com/csachs/blank-unused-screen

import gi
gi.require_version('Gtk', '3.0')
gi.require_version('AppIndicator3', '0.1')

from gi.repository import Gtk, Gdk, GObject
from gi.repository.AppIndicator3 import Indicator, IndicatorStatus, IndicatorCategory

IDENTIFIER = 'blank-unused-screens'
POLLING_INTERVAL = 100

__author__ = 'Christian C. Sachs'
__version__ = '0.0.1'
__license__ = 'BSD'

INFO_TEXT = """
gtk-blank-unused-screen.py
——————————————————————————
ver {__version__} by {__author__}.
Licensed under the {__license__} license.

This little utility blanks (i.e. shows a black fullscreen window)
the a chosen screen when the mouse cursor is currently not in them.

Screens can be chosen via the notification area icon menu.
""".format(**locals())


def main():
    screen = Gdk.Screen.get_default()

    screens_list = list(range(screen.get_n_monitors()))

    screens = {n: False for n in screens_list}

    # def toggle(_):
    #     pass

    def info(_):
        dialog = Gtk.MessageDialog(message_format=INFO_TEXT, buttons=Gtk.ButtonsType.OK)
        _ = dialog.run()
        dialog.destroy()

    def quit_app(_):
        Gtk.main_quit()

    def get_switch_screen(the_n):
        def _inner(_):
            screens[the_n] = not screens[the_n]
            add_timout()
        return _inner

    menu = Gtk.Menu()

    items = [
                ("Screen %d" % (n,), get_switch_screen(n), Gtk.CheckMenuItem)
                for n in screens_list] + [
                # maybe add a global on/off for the functionality
                # maybe with hotkey
                # ("Toggle", toggle, Gtk.MenuItem),
                ("Info", info, Gtk.MenuItem),
                ("Quit", quit_app, Gtk.MenuItem)
            ]

    for text, callback, mi in items:
        _item = mi(text)
        _item.connect('activate', callback)
        menu.append(_item)

    menu.show_all()

    indicator = Indicator.new(IDENTIFIER, Gtk.STOCK_LEAVE_FULLSCREEN, IndicatorCategory.SYSTEM_SERVICES)
    indicator.set_status(IndicatorStatus.ACTIVE)
    indicator.set_menu(menu)

    black = Gdk.color_parse('#000')

    window_active = {n: False for n in screens_list}

    def add_timout():
        def _timeout():
            added_window = False

            pointer = screen.get_root_window().get_pointer()
            current_screen_num = screen.get_monitor_at_point(pointer.x, pointer.y)

            for screen_num in screens_list:
                if screens[screen_num] and current_screen_num != screen_num:
                    if not window_active[screen_num]:
                        rect = screen.get_monitor_geometry(screen_num)
                        window = Gtk.Window()

                        window.modify_bg(Gtk.StateType.NORMAL, black)
                        window.set_default_size(rect.width, rect.height)
                        window.move(rect.x, rect.y)
                        window.set_skip_taskbar_hint(True)
                        window.fullscreen()

                        def make_quit_event(the_n):
                            # noinspection PyUnusedLocal
                            def _window_event(window_inner, event):
                                window_inner.destroy()
                                window_active[the_n] = False

                                add_timout()
                            return _window_event

                        window.connect('motion_notify_event', make_quit_event(screen_num))
                        window.set_events(Gdk.EventMask.POINTER_MOTION_MASK)

                        def create_set_override_redirect(w):
                            def set_override_redirect():
                                w.get_window().set_override_redirect(True)
                            return set_override_redirect

                        window.show_all()
                        window_active[screen_num] = True

                        GObject.timeout_add(50, create_set_override_redirect(window))

                        added_window = True
            if not added_window and sum(screens.values()) > 0:
                add_timout()

        GObject.timeout_add(POLLING_INTERVAL, _timeout)

    add_timout()

    Gtk.main()


if __name__ == '__main__':
    main()
