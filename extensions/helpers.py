import json
import random
import string


def generate_key(length=64):  # MOVE TO HELPERS
    """Generates random character key.

    Args:
        length (int, optional): No. of characters to generate. Defaults to 64.

    Returns:
        key (str): Generated key.
    """
    key = ''.join(
        random.SystemRandom()
            .choice(string.ascii_letters + string.digits) for _ in range(64))
    return key


def generate_server_name():
    """Generates random IP address and port number as a string.

    Returns:
        server_name (str): Generated IP/port address
    """
    ip_sfx = random.randrange(2, 255)
    port = random.randrange(8100, 8999)
    pfx = '127.0.0.'
    ip_addr = pfx + str(ip_sfx)
    server_name = [ip_addr, port]
    return server_name


def load_json_file(file):
    """Import JSON data object from file.

    Args:
        file (str): Path of JSON file to load

    Returns:
        data (arr): Table of JSON data
    """
    with open(file, 'r') as f:
        data = json.load(f)
    return data


def save_json_file(file, obj, indent=0):
    """Save JSON data object to file.

    Args:
        file (str): File destination
        obj (list, dict): JSON data object
        indent (int): Indentation level
    """

    with open(file, 'w') as f:
        json.dump(obj, f, indent=indent)


def sort_title(title, option):
    """Convert [title] to sortable string, or revert sortable [title] to a human-readable string.

    Args:
        title (str): Title to convert
        option (str): Conversion option [`s` or `d`]

    Options:
        `s`: Convert to sortable title (move article to end of string)  
        `d`: Convert to display title (move artice to beginning of string)

    Returns:
        c_title (str): Converted title string

    Example:
        Input:  
        `sort_title('The Sample Title', c)`

        Output:  
        `Sample Title, The`
    """  # noqa: W291

    article = ''
    base_title = ''
    t = ''

    def s(title):
        if title.startswith('A ') or \
                title.startswith('An ') or \
                title.startswith('The '):
            title_array = title.split(' ')

            article = title_array[0]
            del title_array[0]
            base_title = ' '.join(title_array)
            t = base_title + ', ' + article
        else:
            t = title

        return t

    def d(title):
        if title.endswith(', A') or \
            title.endswith(', An') or \
                title.endswith(', The'):
            base_title, article = title.split(', ')
            t = str(article + ' ' + base_title)
        else:
            t = title

        return t

    try:
        c_title = locals()[option](title)
    except KeyError:
        print('\nOption not recognized. Displaying help dialog...\n\ndef ' +
              sort_title.__name__ + '(title, option)\n\n' + sort_title.__doc__)
        exit()

    return c_title
