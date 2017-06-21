import urwid
from functools import partial
from .ui import (
    BasePipe,
    TeePipe,
    SimplePipe,
    ElbowPipe,
    Computer,
    PALETTE
)


def exit_on_q(key):
    if key in ('q', 'Q', 'esc'):
        raise urwid.ExitMainLoop()
    return key


def find_cols_rows():
    return urwid.raw_display.Screen().get_cols_rows()


def play(all_widgets, statusbar, clicked_widget):
    statusbar.set_text(str(clicked_widget))


def main():
    cols, rows = find_cols_rows()
    if cols < 80 or rows < 40:
        print('Please resize your window to at least 80x40 and try again')
        return
    statusbar = urwid.Text('Ready')
    grid_widgets = [
        Computer(is_server=True, rotate=1), TeePipe(), TeePipe(), Computer(rotate=3),
        ElbowPipe(), TeePipe(), ElbowPipe(), Computer(rotate=3),
        Computer(), TeePipe(), SimplePipe(), Computer(rotate=3),
        Computer(rotate=1), TeePipe(), SimplePipe(), Computer(rotate=3),
    ]
    for w in grid_widgets:
        if isinstance(w, BasePipe):
            w.callback = partial(play, grid_widgets, statusbar)
    widget = urwid.GridFlow(
        grid_widgets,
        cell_width=20,
        h_sep=0,
        v_sep=0,
        align='left',
    )
    widget = urwid.Padding(widget, width=80, align='center')
    widget = urwid.Pile([widget, statusbar])
    widget = urwid.Filler(widget)
    urwid.MainLoop(widget, PALETTE, unhandled_input=exit_on_q).run()


if __name__ == '__main__':
    main()
