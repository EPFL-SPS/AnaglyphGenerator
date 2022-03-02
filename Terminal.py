import os


def getTerminalSize():
    """
    Get terminal width
    :return: width in chars
    """
    try:
        terminal_size = os.get_terminal_size()[0]
    except OSError:
        terminal_size = 50  # Default value if error
    return terminal_size


def getInput(message, default=None, type='str'):
    """
    Get user input. Allow to specify a default value
    :param message: Message to display
    :param default: Default value
    :return: User input, default value if user hit enter without typing anything
    """
    inp = input("{}{}: ".format(message, " [default='{}']".format(default) if default else ""))

    # If user does not specify a value, use default one
    if inp == '':
        inp = default

    if type == 'int':
        try:
            inp = int(inp)
        except ValueError:
            return None

    return inp


def updateProgressBar(text, current, end):
    """
    Calculate and display progress bar depending on specified progress values
    //!\\ Remove the last line in the console on the first call
    :param text: Progress bar title
    :param current: Current progress value
    :param end: Target value
    """
    progress_percentage = current / end * 100

    header = "{} - {:3.1f}% ".format(text, progress_percentage)

    bar_size = getTerminalSize() - len(header) - 2  # 2 for '[' and ']'

    progress = round(bar_size * progress_percentage / 100)

    print("\033[A                             \033[A")  # Delete last line
    print("{}[{}{}]".format(header, "=" * progress, " " * (bar_size - progress)))

