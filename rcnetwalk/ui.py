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

    def __init__(self, rotate=0):
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
''',
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
u'''
████████████████████
████████████████████
████████████████████
████████████████████
                    
                    
████████    ████████
████████    ████████
████████    ████████
████████    ████████
''',
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
''',
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
''',

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
''',

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


class RCLogo(urwid.WidgetWrap):
    def __init__(self, lighted=False):
        self.text = urwid.Text(u'')
        self.lighted = lighted
        self.update()
        super(RCLogo, self).__init__(self.text)

    def update(self):
        def get_line(index, line, lighted):
            if index in (2, 3):
                if lighted:
                    return [
                        ('none', line[:6]),
                        ('green', line[6:14]),
                        line[14:]
                    ]
                else:
                    return line[:6] + ' ' * 8 + line[14:]
            return line

        logo_lines = [
            get_line(index, line, self.lighted)
            for index, line in enumerate(LOGO.splitlines(keepends=True))
        ]
        self.text.set_text(logo_lines)
