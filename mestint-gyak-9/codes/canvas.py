# ______________________________________________________________________________


_canvas = """
<script type="text/javascript" src="./js/canvas.js"></script>
<div>
<canvas id="{0}" width="{1}" height="{2}" style="background:rgba(158, 167, 184, 0.2);" onclick='click_callback(this, event, "{3}")'></canvas>
</div>

<script> var {0}_canvas_object = new Canvas("{0}");</script>
"""  # noqa


class Canvas:
    """Inherit from this class to manage the HTML canvas element in jupyter notebooks.
    To create an object of this class any_name_xyz = Canvas("any_name_xyz")
    The first argument given must be the name of the object being created.
    IPython must be able to reference the variable name that is being passed."""

    def __init__(self, varname, width=800, height=600, cid=None):
        self.name = varname
        self.cid = cid or varname
        self.width = width
        self.height = height
        self.html = _canvas.format(self.cid, self.width, self.height, self.name)
        self.exec_list = []
        display_html(self.html)

    def mouse_click(self, x, y):
        """Override this method to handle mouse click at position (x, y)"""
        raise NotImplementedError

    def mouse_move(self, x, y):
        raise NotImplementedError

    def execute(self, exec_str):
        """Stores the command to be executed to a list which is used later during update()"""
        if not isinstance(exec_str, str):
            print("Invalid execution argument:", exec_str)
            self.alert("Received invalid execution command format")
        prefix = "{0}_canvas_object.".format(self.cid)
        self.exec_list.append(prefix + exec_str + ';')

    def fill(self, r, g, b):
        """Changes the fill color to a color in rgb format"""
        self.execute("fill({0}, {1}, {2})".format(r, g, b))

    def stroke(self, r, g, b):
        """Changes the colors of line/strokes to rgb"""
        self.execute("stroke({0}, {1}, {2})".format(r, g, b))

    def strokeWidth(self, w):
        """Changes the width of lines/strokes to 'w' pixels"""
        self.execute("strokeWidth({0})".format(w))

    def rect(self, x, y, w, h):
        """Draw a rectangle with 'w' width, 'h' height and (x, y) as the top-left corner"""
        self.execute("rect({0}, {1}, {2}, {3})".format(x, y, w, h))

    def rect_n(self, xn, yn, wn, hn):
        """Similar to rect(), but the dimensions are normalized to fall between 0 and 1"""
        x = round(xn * self.width)
        y = round(yn * self.height)
        w = round(wn * self.width)
        h = round(hn * self.height)
        self.rect(x, y, w, h)

    def line(self, x1, y1, x2, y2):
        """Draw a line from (x1, y1) to (x2, y2)"""
        self.execute("line({0}, {1}, {2}, {3})".format(x1, y1, x2, y2))

    def line_n(self, x1n, y1n, x2n, y2n):
        """Similar to line(), but the dimensions are normalized to fall between 0 and 1"""
        x1 = round(x1n * self.width)
        y1 = round(y1n * self.height)
        x2 = round(x2n * self.width)
        y2 = round(y2n * self.height)
        self.line(x1, y1, x2, y2)

    def arc(self, x, y, r, start, stop):
        """Draw an arc with (x, y) as centre, 'r' as radius from angles 'start' to 'stop'"""
        self.execute("arc({0}, {1}, {2}, {3}, {4})".format(x, y, r, start, stop))

    def arc_n(self, xn, yn, rn, start, stop):
        """Similar to arc(), but the dimensions are normalized to fall between 0 and 1
        The normalizing factor for radius is selected between width and height by
        seeing which is smaller."""
        x = round(xn * self.width)
        y = round(yn * self.height)
        r = round(rn * min(self.width, self.height))
        self.arc(x, y, r, start, stop)

    def clear(self):
        """Clear the HTML canvas"""
        self.execute("clear()")

    def font(self, font):
        """Changes the font of text"""
        self.execute('font("{0}")'.format(font))

    def text(self, txt, x, y, fill=True):
        """Display a text at (x, y)"""
        if fill:
            self.execute('fill_text("{0}", {1}, {2})'.format(txt, x, y))
        else:
            self.execute('stroke_text("{0}", {1}, {2})'.format(txt, x, y))

    def text_n(self, txt, xn, yn, fill=True):
        """Similar to text(), but with normalized coordinates"""
        x = round(xn * self.width)
        y = round(yn * self.height)
        self.text(txt, x, y, fill)

    def alert(self, message):
        """Immediately display an alert"""
        display_html('<script>alert("{0}")</script>'.format(message))

    def update(self):
        """Execute the JS code to execute the commands queued by execute()"""
        exec_code = "<script>\n" + '\n'.join(self.exec_list) + "\n</script>"
        self.exec_list = []
        display_html(exec_code)


def display_html(html_string):
    display(HTML(html_string))


################################################################################


class Canvas_TicTacToe(Canvas):
    """Play a 3x3 TicTacToe game on HTML canvas"""

    def __init__(self, varname, player_1='human', player_2='random',
                 width=300, height=350, cid=None):
        valid_players = ('human', 'random', 'alpha_beta')
        if player_1 not in valid_players or player_2 not in valid_players:
            raise TypeError("Players must be one of {}".format(valid_players))
        super().__init__(varname, width, height, cid)
        self.ttt = TicTacToe()
        self.state = self.ttt.initial
        self.turn = 0
        self.strokeWidth(5)
        self.players = (player_1, player_2)
        self.font("20px Arial")
        self.draw_board()

    def mouse_click(self, x, y):
        player = self.players[self.turn]
        if self.ttt.terminal_test(self.state):
            if 0.55 <= x / self.width <= 0.95 and 6 / 7 <= y / self.height <= 6 / 7 + 1 / 8:
                self.state = self.ttt.initial
                self.turn = 0
                self.draw_board()
            return

        if player == 'human':
            x, y = int(3 * x / self.width) + 1, int(3 * y / (self.height * 6 / 7)) + 1
            if (x, y) not in self.ttt.actions(self.state):
                # Invalid move
                return
            move = (x, y)
        elif player == 'alpha_beta':
            move = alpha_beta_player(self.ttt, self.state)
        else:
            move = random_player(self.ttt, self.state)
        self.state = self.ttt.result(self.state, move)
        self.turn ^= 1
        self.draw_board()

    def draw_board(self):
        self.clear()
        self.stroke(0, 0, 0)
        offset = 1 / 20
        self.line_n(0 + offset, (1 / 3) * 6 / 7, 1 - offset, (1 / 3) * 6 / 7)
        self.line_n(0 + offset, (2 / 3) * 6 / 7, 1 - offset, (2 / 3) * 6 / 7)
        self.line_n(1 / 3, (0 + offset) * 6 / 7, 1 / 3, (1 - offset) * 6 / 7)
        self.line_n(2 / 3, (0 + offset) * 6 / 7, 2 / 3, (1 - offset) * 6 / 7)

        board = self.state.board
        for mark in board:
            if board[mark] == 'X':
                self.draw_x(mark)
            elif board[mark] == 'O':
                self.draw_o(mark)
        if self.ttt.terminal_test(self.state):
            # End game message
            utility = self.ttt.utility(self.state, self.ttt.to_move(self.ttt.initial))
            if utility == 0:
                self.text_n('Game Draw!', offset, 6 / 7 + offset)
            else:
                self.text_n('Player {} wins!'.format("XO"[utility < 0]), offset, 6 / 7 + offset)
                # Find the 3 and draw a line
                self.stroke([255, 0][self.turn], [0, 255][self.turn], 0)
                for i in range(3):
                    if all([(i + 1, j + 1) in self.state.board for j in range(3)]) and \
                            len({self.state.board[(i + 1, j + 1)] for j in range(3)}) == 1:
                        self.line_n(i / 3 + 1 / 6, offset * 6 / 7, i / 3 + 1 / 6, (1 - offset) * 6 / 7)
                    if all([(j + 1, i + 1) in self.state.board for j in range(3)]) and \
                            len({self.state.board[(j + 1, i + 1)] for j in range(3)}) == 1:
                        self.line_n(offset, (i / 3 + 1 / 6) * 6 / 7, 1 - offset, (i / 3 + 1 / 6) * 6 / 7)
                if all([(i + 1, i + 1) in self.state.board for i in range(3)]) and \
                        len({self.state.board[(i + 1, i + 1)] for i in range(3)}) == 1:
                    self.line_n(offset, offset * 6 / 7, 1 - offset, (1 - offset) * 6 / 7)
                if all([(i + 1, 3 - i) in self.state.board for i in range(3)]) and \
                        len({self.state.board[(i + 1, 3 - i)] for i in range(3)}) == 1:
                    self.line_n(offset, (1 - offset) * 6 / 7, 1 - offset, offset * 6 / 7)
            # restart button
            self.fill(0, 0, 255)
            self.rect_n(0.5 + offset, 6 / 7, 0.4, 1 / 8)
            self.fill(0, 0, 0)
            self.text_n('Restart', 0.5 + 2 * offset, 13 / 14)
        else:  # Print which player's turn it is
            self.text_n("Player {}'s move({})".format("XO"[self.turn], self.players[self.turn]),
                        offset, 6 / 7 + offset)

        self.update()

    def draw_x(self, position):
        self.stroke(0, 255, 0)
        x, y = [i - 1 for i in position]
        offset = 1 / 15
        self.line_n(x / 3 + offset, (y / 3 + offset) * 6 / 7, x / 3 + 1 / 3 - offset, (y / 3 + 1 / 3 - offset) * 6 / 7)
        self.line_n(x / 3 + 1 / 3 - offset, (y / 3 + offset) * 6 / 7, x / 3 + offset, (y / 3 + 1 / 3 - offset) * 6 / 7)

    def draw_o(self, position):
        self.stroke(255, 0, 0)
        x, y = [i - 1 for i in position]
        self.arc_n(x / 3 + 1 / 6, (y / 3 + 1 / 6) * 6 / 7, 1 / 9, 0, 360)