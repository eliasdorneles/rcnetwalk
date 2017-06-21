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


class Game:
    def __init__(self):
        self.grid_widgets = [
            Computer(is_server=True, rotate=1), TeePipe(), TeePipe(), Computer(rotate=3),
            ElbowPipe(connected=1), TeePipe(), ElbowPipe(), Computer(rotate=3),
            Computer(), TeePipe(), SimplePipe(), Computer(rotate=3),
            Computer(rotate=1), TeePipe(), SimplePipe(), Computer(rotate=3),
        ]
        self.statusbar = urwid.Text('Ready')

        for i, w in enumerate(self.grid_widgets):
            w._grid_position = i

        for w in self.pipe_widgets:
            w.callback = partial(self.play)

    def play(self, clicked_widget):
        self._update_connected_state()
        for w in self.grid_widgets:
            w.update()
        if self.won():
            self.statusbar.set_text('YAAY, congrats, you win!')

    def won(self):
        return all(c.connected for c in self.computer_widgets)

    def neighbours(self, widget):
        i = widget._grid_position
        width, height = 4, 4
        return {
            'up': None if i < width else self.grid_widgets[i - width],
            'down': None if i > (width * (height - 1)) - 1 else self.grid_widgets[i + height],
            'left': None if i % width == 0 else self.grid_widgets[i - 1],
            'right': None if (i + 1) % width == 0 else self.grid_widgets[i + 1],
        }

    def _reset_connected_state(self):
        for c in self.computer_widgets:
            if not c.is_server:
                c.connected = False
        for w in self.pipe_widgets:
            w.connected = False

    def _update_connected_state(self):
        DIRECTION_FROM = {'up': 'down', 'down': 'up', 'left': 'right', 'right': 'left'}
        self._reset_connected_state()
        seen = set()

        def set_connected(node, direction):
            if node in seen:
                return
            seen.add(node)
            neighbours = self.neighbours(node)
            if isinstance(node, Computer):
                if node.is_server:
                    return
                if node.connector_position == direction:
                    node.connected = True
            if isinstance(node, BasePipe):
                if direction not in node.connectors:
                    return
                node.connected = True
                for conn in node.connectors:
                    if neighbours[conn]:
                        set_connected(neighbours[conn], DIRECTION_FROM[conn])

        for w in self.server_widgets:
            neighbours = self.neighbours(w)
            conn = w.connector_position
            if neighbours[conn]:
                set_connected(neighbours[w.connector_position], DIRECTION_FROM[conn])

    @property
    def pipe_widgets(self):
        return [w for w in self.grid_widgets if isinstance(w, BasePipe)]

    @property
    def server_widgets(self):
        return [w for w in self.grid_widgets if isinstance(w, Computer) and w.is_server]

    @property
    def computer_widgets(self):
        return [w for w in self.grid_widgets if isinstance(w, Computer)]

    def start(self):
        cols, rows = find_cols_rows()
        if cols < 80 or rows < 40:
            print('Please resize your window to at least 80x40 and try again')
            return

        widget = urwid.GridFlow(
            self.grid_widgets,
            cell_width=20,
            h_sep=0,
            v_sep=0,
            align='left',
        )
        widget = urwid.Padding(widget, width=80, align='center')
        widget = urwid.Pile([widget, self.statusbar])
        widget = urwid.Filler(widget)
        urwid.MainLoop(widget, PALETTE, unhandled_input=exit_on_q).run()


if __name__ == '__main__':
    g = Game()
    g.start()
