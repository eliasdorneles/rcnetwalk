#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import urwid


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


def exit_on_q(key):
    if key in ('q', 'Q', 'esc'):
        raise urwid.ExitMainLoop()
    return key


def find_cols_rows():
    return urwid.raw_display.Screen().get_cols_rows()


def main():
    cols, rows = find_cols_rows()
    if cols < 80 or rows < 40:
        print('Please resize your window to at least 80x40 and try again')
        return
    widget = urwid.GridFlow(
        [
             RCLogo(lighted=0),
             RCLogo(lighted=1),
             RCLogo(lighted=0),
             RCLogo(lighted=1),

             RCLogo(lighted=1),
             RCLogo(lighted=1),
             RCLogo(lighted=1),
             RCLogo(lighted=0),

             RCLogo(lighted=0),
             RCLogo(lighted=1),
             RCLogo(lighted=0),
             RCLogo(lighted=1),

             RCLogo(lighted=1),
             RCLogo(lighted=0),
             RCLogo(lighted=1),
             RCLogo(lighted=0),
        ],
        cell_width=20,
        h_sep=0,
        v_sep=0,
        align='left',
    )
    widget = urwid.Padding(widget, width=80, align='center')
    widget = urwid.Filler(widget)
    urwid.MainLoop(widget, PALETTE, unhandled_input=exit_on_q).run()


if __name__ == '__main__':
    main()
