from colors import Colors
import subprocess

class TGutils:
    """
    Basic methods for use in my apps.

    version 0.1a
    """
    def __init__(self):
        pass

    # ------------------------------------------------------------------------
    # --- bytes to human readable
    # ------------------------------------------------------------------------
    def bytes_to_human_readable(self, size_in_bytes=0):
        units = ['B', 'KiB', 'MiB', 'GiB', 'TiB']
        size = float(size_in_bytes)
        for unit in units:
            if size < 1024:
                return f"{size:.2f} {unit}"
            size /= 1024

    # ------------------------------------------------------------------------
    # --- cli utils
    # ------------------------------------------------------------------------
    def header(self, message, col='%c', clear=False, ascii=False, colors=False, nl=False):
        if ascii:
            chars = ['+', '+', '+', '+', '-', '|']
        else:
            chars = ['┌', '┐', '└', '┘', '─', '│']

        width = len(self.colorize(message, remove_colors=True)) + 2
        horline = width * chars[4]

        if clear:
            subprocess.call('clear')
        self.printf(f"{col}{chars[0]}{horline}{chars[1]}%R", remove_colors=not colors)
        self.printf(f"{col}{chars[5]}%R {message} {col}{chars[5]}%R", remove_colors=not colors)
        self.printf(f"{col}{chars[2]}{horline}{chars[3]}%R", remove_colors=not colors, nl=nl)

    def colorize(self, message, remove_colors=False):
        for color in Colors.colors:
            replacement = '' if remove_colors else color[1]
            message = message.replace(color[0], replacement)
        return message

    def printf(self, message, remove_colors=False, nl=False):
        end = '\n\n' if nl else '\n'
        line = self.colorize(message, remove_colors=remove_colors)
        print(line, end=end)

    def fprint(self, key, value, fmt='{} {}', remove_colors=False, nl=False):
        line = fmt.format(key, value)
        self.printf(line, remove_colors=remove_colors, nl=nl)

    def clearlines(self, num=1):
        for _ in range(num):
            print('\033[1A', end='\x1b[2K')
