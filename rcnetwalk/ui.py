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
    ('greenbg', '', 'dark blue'),
    ('none', '', ''),
]


class BaseClickable(urwid.WidgetWrap):
    def __init__(self, *args, **kwargs):
        self.callback = kwargs.pop('callback', None)
        super(BaseClickable, self).__init__(*args, **kwargs)

    def selectable(self):
        return True

    def keypress(self, size, key):
        return key

    def mouse_event(self, size, event, button, col, row, focus):
        if event == 'mouse press':
            if self.callback:
                self.callback(self)
            self.update()


class BasePipe(BaseClickable):
    content_choices = ()

    def __init__(self, rotate=0, connected=False, **kw):
        if not self.content_choices:
            raise ValueError("You should set content_choices when subclassing BasePipe")
        self.connected = connected
        self.iter_content = cycle(self.content_choices)
        self.text = urwid.Text(u'')
        self.connectors = {}
        self.rotate()
        if rotate > 0:
            for i in range(rotate):
                self.rotate()
        self.update()
        super(BasePipe, self).__init__(self.text, **kw)

    def rotate(self):
        self.connectors, text = next(self.iter_content)
        self._current_text = text.strip()

    def update(self):
        self.text.set_text(self._current_text)

    def __repr__(self):
        return '%s(%r, connected=%r)' % (self.__class__.__name__,
                                         self.connectors, bool(self.connected))


class NoPipe(BasePipe):
    content_choices = [
        ({},
u'''
████████████████████
████████████████████
████████████████████
████████████████████
████████████████████
████████████████████
████████████████████
████████████████████
████████████████████
████████████████████
'''), # NOQA
    ]


class CrossPipe(BasePipe):
    content_choices = [
        ({'left', 'up', 'right', 'down'},
u'''
████████    ████████
████████    ████████
████████    ████████
████████    ████████
                    
                    
████████    ████████
████████    ████████
████████    ████████
████████    ████████
'''), # NOQA
    ]


class TeePipe(BasePipe):
    content_choices = [
        ({'left', 'up', 'right'},
u'''
████████    ████████
████████    ████████
████████    ████████
████████    ████████
                    
                    
████████████████████
████████████████████
████████████████████
████████████████████
'''), # NOQA

({'up', 'right', 'down'}, u'''
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
'''), # NOQA

({'left', 'right', 'down'}, u'''
████████████████████
████████████████████
████████████████████
████████████████████
                    
                    
████████    ████████
████████    ████████
████████    ████████
████████    ████████
'''), # NOQA

({'left', 'up', 'down'}, u'''
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
'''),
    ]


class SimplePipe(BasePipe):
    content_choices = [
({'left', 'right'},
u'''
████████████████████
████████████████████
████████████████████
████████████████████
                    
                    
████████████████████
████████████████████
████████████████████
████████████████████
'''), # NOQA

({'up', 'down'}, u'''
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
'''),
    ]


class ElbowPipe(BasePipe):
    content_choices = [
({'left', 'up'},
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
'''), # NOQA

({'up', 'right'},
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
'''), # NOQA

({'right', 'down'}, u'''
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
'''), # NOQA

({'left', 'down'}, u'''
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
'''),
    ]


class Computer(BaseClickable):
    def __init__(self, connected=False, is_server=False, rotate=0, **kw):
        self.text = urwid.Text(u'')
        self.is_server = is_server
        self.connected = is_server or connected
        self.iter_connector = cycle(['up', 'right', 'down', 'left'])
        self.rotate()
        if rotate:
            for i in range(rotate):
                self.rotate()
        super(Computer, self).__init__(self.text, **kw)

    def rotate(self):
        self.connector_position = next(self.iter_connector)
        self.update()

    def update(self):
        def get_line(index, line, connected):
            if (index == 0 and self.connector_position == 'up'
                    or index == 9 and self.connector_position == 'down'):
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
