#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import urwid
from itertools import cycle


LOGO = u'''
████████████████████
████ ▄▄▄▄▄▄▄▄▄▄ ████
████ █▄ ▄ ▄   █ ████
████ █ ▄▄ ▄▄  █ ████
████ █        █ ████
████ ▀▀▀▀▀▀▀▀▀▀ ████
█████▀▀▀    ▀▀▀█████
████  ▄▀▄▀▄▀▄▀  ████
████▄▄▄▄▄▄▄▄▄▄▄▄████
████████████████████
'''.strip()


PALETTE = [
    ('green', 'dark green', ''),
    ('none', '', ''),
]


class BasePipe(urwid.WidgetWrap):
    content_choices = ()

    def __init__(self, rotate=0, connected=False):
        if not self.content_choices:
            raise ValueError("You should set content_choices when subclassing BasePipe")
        self.connected = connected
        self.iter_content = cycle([c.strip() for c in self.content_choices])
        self.text = urwid.Text(u'')
        self.rotate()
        if rotate > 0:
            for i in range(rotate):
                self.rotate()
        super(BasePipe, self).__init__(self.text)

    def rotate(self):
        self.text.set_text(next(self.iter_content))

    def selectable(self):
        return True

    def keypress(self, size, key):
        return key

    def mouse_event(self, size, event, button, col, row, focus):
        if event == 'mouse press':
            self.rotate()


class TeePipe(BasePipe):
    content_choices = (
u'''
████████    ████████
████████    ████████
████████    ████████
████████    ████████
                    
                    
████████████████████
████████████████████
████████████████████
████████████████████
''', # NOQA

u'''
████████    ████████
████████    ████████
████████    ████████
████████    ████████
████████            
████████            
████████    ████████
████████    ████████
████████    ████████
████████    ████████
''', # NOQA

u'''
████████████████████
████████████████████
████████████████████
████████████████████
                    
                    
████████    ████████
████████    ████████
████████    ████████
████████    ████████
''', # NOQA

u'''
████████    ████████
████████    ████████
████████    ████████
████████    ████████
            ████████
            ████████
████████    ████████
████████    ████████
████████    ████████
████████    ████████
''',
    )


class SimplePipe(BasePipe):
    content_choices = [
u'''
████████████████████
████████████████████
████████████████████
████████████████████
                    
                    
████████████████████
████████████████████
████████████████████
████████████████████
''', # NOQA

u'''
████████    ████████
████████    ████████
████████    ████████
████████    ████████
████████    ████████
████████    ████████
████████    ████████
████████    ████████
████████    ████████
████████    ████████
''',
    ]


class ElbowPipe(BasePipe):
    content_choices = [
u'''
████████    ████████
████████    ████████
████████    ████████
████████    ████████
            ████████
            ████████
████████████████████
████████████████████
████████████████████
████████████████████
''', # NOQA

u'''
████████    ████████
████████    ████████
████████    ████████
████████    ████████
████████            
████████            
████████████████████
████████████████████
████████████████████
████████████████████
''', # NOQA

u'''
████████████████████
████████████████████
████████████████████
████████████████████
████████            
████████            
████████    ████████
████████    ████████
████████    ████████
████████    ████████
''', # NOQA

u'''
████████████████████
████████████████████
████████████████████
████████████████████
            ████████
            ████████
████████    ████████
████████    ████████
████████    ████████
████████    ████████
''',
    ]


class Computer(urwid.WidgetWrap):
    def __init__(self, connected=False, is_server=False, rotate=0):
        self.text = urwid.Text(u'')
        self.connected = is_server or connected
        self.iter_connector = cycle(['up', 'right', 'down', 'left'])
        self._rotate()
        if rotate:
            for i in range(rotate):
                self._rotate()
        super(Computer, self).__init__(self.text)

    def _rotate(self):
        self.connector_position = next(self.iter_connector)
        self.update()

    def update(self):
        def get_line(index, line, connected):
            if (index == 0 and self.connector_position == 'up'
                    or index == 19 and self.connector_position == 'down'):
                line = line[:8] + '    ' + line[12:]
            if index in (4, 5):
                if self.connector_position == 'left':
                    line = '    ' + line[4:]
                elif self.connector_position == 'right':
                    line = line[:-5] + '    '
            if index == 4 and self.connector_position == 'left':
                line = '    ' + line[4:]
            if index in (2, 3):
                if connected:
                    return [
                        ('none', line[:6]),
                        ('green', line[6:14]),
                        line[14:]
                    ]
                else:
                    return line[:6] + ' ' * 8 + line[14:]
            return line

        logo_lines = [
            get_line(index, line, self.connected)
            for index, line in enumerate(LOGO.splitlines(keepends=True))
        ]
        self.text.set_text(logo_lines)
