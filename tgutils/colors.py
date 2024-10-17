#Source:
# -- https://gist.github.com/rene-d/9e584a7dd2935d0f461904b9f2950007

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
