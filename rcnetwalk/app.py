import random
import urwid
from functools import partial
from .ui import (
    BasePipe,
    CrossPipe,
    NoPipe,
    SimplePipe,
    TeePipe,
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


def random_position(sequence):
    return random.randint(0, len(sequence) - 1)


class Game:
    def __init__(self):
        self._generate_game()

        for w in self.grid_widgets:
            w.callback = partial(self.play)
        self.statusbar = urwid.Text('Ready')
        self._update_ui()

    def _generate_game(self):
        self.grid_widgets = [None] * 16
        for x in range(5):
            self.place_widget(random_position(self.grid_widgets), Computer())
        self.place_widget(random_position(self.grid_widgets), Computer(is_server=True))

        for i, widget in enumerate(self.grid_widgets):
            if widget is None:
                self.place_widget(i, CrossPipe())
        self._update_connected_state()
        if not self._all_connected():
            self._generate_game()
        self._reduce_to_minimal_connections()
        self._scramble()

    def _reduce_to_minimal_connections(self):
        """Reduce game into minimal connections that is still playable"""

        def generate_for_class(pipe_cls):
            return [
                pipe_cls(rotate=n_rotations)
                for n_rotations
                in range(len(pipe_cls.content_choices))
            ]

        def get_reductions(pipe):
            if isinstance(pipe, CrossPipe):
                return generate_for_class(TeePipe)
            elif isinstance(pipe, TeePipe):
                return generate_for_class(ElbowPipe) + generate_for_class(SimplePipe)
            elif isinstance(pipe, SimplePipe):
                return generate_for_class(NoPipe)

            return []

        def get_random_pipe_widget_position():
            pos = random_position(self.grid_widgets)
            if isinstance(self.grid_widgets[pos], Computer):
                return get_random_pipe_widget_position()
            return pos

        fixed = set()
        while len(fixed) != len(self.pipe_widgets):
            position = get_random_pipe_widget_position()
            while position in fixed:
                position = get_random_pipe_widget_position()

            done = False
            while not done:
                prev_widget = self.grid_widgets[position]
                candidates = get_reductions(prev_widget)
                if not candidates:
                    break
                working = []

                for cand in candidates:
                    self.place_widget(position, cand)
                    self._update_connected_state()
                    if self._all_connected():
                        working.append(cand)
                if working:
                    self.place_widget(position, working[-1])
                else:
                    self.place_widget(position, prev_widget)
                    done = True
                self._update_connected_state()

            fixed.add(position)

    def place_widget(self, index, widget):
        self.grid_widgets[index] = widget
        self.grid_widgets[index]._grid_position = index

    def _scramble(self):
        """Scramble rotation for all non-computer widgets"""
        for pipe in self.pipe_widgets:
            for x in range(random.randint(0, 5)):
                pipe.rotate()
        self._update_connected_state()

    def _update_ui(self):
        for w in self.grid_widgets:
            w.update()
        if self._all_connected():
            self.statusbar.set_text('YAAY, congrats, you win!')
        else:
            self.statusbar.set_text('Try rotating a piece')

    def play(self, clicked_widget):
        if clicked_widget is not None:
            clicked_widget.rotate()
            self.statusbar.set_text('clicked' + str(clicked_widget))
        self._update_connected_state()
        self._update_ui()

    def _all_connected(self):
        return all(c.connected for c in self.computer_widgets)

    def find_neighbours(self, widget):
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
            if (node, direction) in seen:
                return
            seen.add((node, direction))
            neighbours = self.find_neighbours(node)
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
            neighbours = self.find_neighbours(w)
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
