import sys
import subprocess

# ----------------------------------------------------------------------- UTILS
class TGUtils:
    def __init__(self):
        self.app_title = 'SET APPTITLE HERE'
        self.app_slogan = 'SET SLOGAN HERE'
    
    # -------------------------------------------------------- APP HEADER
    def app_header(self, colors=True, clear_screen=False, nl=True):
        if clear_screen:
            subprocess.call('clear')

        title = f"%y{self.app_title}%R - %g{self.app_slogan}%R"
        self.printf(title, colors=colors, nl=nl)

    # ---------------------------------------------------------- MESSAGES
    def message(self, string, arrow='>', colors=True, nl=False):
        message = f"%g{arrow}%R {string}"
        self.printf(message, colors=colors, nl=nl)
    
    def warning(self, string, arrow='>', colors=True, nl=False):
        message = f"%y{arrow}%R {string}"
        self.printf(message, colors=colors, nl=nl)
    
    def error(self, string, arrow='!!', colors=True, nl=False, exit_app=False):
        message = f"%r{arrow}%R {string}"
        if exit_app:
            message += ', exiting...'
        self.printf(message, colors=colors, nl=nl)
        if exit_app:
            sys.exit()

    # --------------------------------------------------------------- CLI
    def printf(self, string, colors=True, nl=False):
        end = '\n\n' if nl else '\n'
        colored = self.colorize(string) 
        if not colors:
            colored = self.colorize(string, remove_colors=True)
        print(colored, end=end)
    
    def fprint(self, key, value, fmt='{} {}', colors=True, nl=False):
        formatted = fmt.format(key, value)
        self.printf(formatted, colors=colors, nl=nl)

    # ----------------------------------------------------------- HELPERS
    def colorize(self, string, remove_colors=False):
        for color in Colors.colors:
            repl = '' if remove_colors else color[1]
            string = string.replace(color[0], repl)
        return string
    
    def clearlines(self, num=1):
        for _ in range(num):
            print('\033[1A', end='\x1b[2K')
    
    def human_readable(self, size_in_bytes=0):
        units = ['B', 'KiB', 'MiB', 'GiB', 'TiB']
        size = float(size_in_bytes)
        for unit in units:
            if size < 1024:
                return f"{size:.2f} {unit}"
            size /= 1024

# ---------------------------------------------------------------------- COLORS
class Colors:
    reset     = "\033[0m"
    black     = "\033[0;30m"
    red       = "\033[0;31m"
    green     = "\033[0;32m"
    yellow    = "\033[0;33m"
    blue      = "\033[0;34m"
    purple    = "\033[0;35m"
    cyan      = "\033[0;36m"
    white     = "\033[0;37m"
    gray      = "\033[1;30m"
    italic    = "\033[0;3m"
    bold      = "\033[0;1m"
    faint     = "\033[2m"
    underline = "\033[4m"
    crossed   = "\033[9m"

    colors = [
            ('%R', reset),
            ('%B', bold),
            ('%F', faint),
            ('%U', underline),
            ('%C', crossed),
            ('%r', red),
            ('%g', green),
            ('%y', yellow),
            ('%p', purple),
            ('%b', blue),
            ('%c', cyan),
            ('%w', white),
            ('%i', italic)
    ]
