import json


def load_json_file(file):
    with open(file, 'r') as f:
        data = json.load(f)
    return data


def sort_title(title, option):
    """Convert [title] to sortable string, or revert sortable [title] to a human-readable string.

    Args:
        title (str): Title to convert
        option (str): Covert/Display

    Options:
        `c`: Convert to sortable title (move article to end of string)
        `d`: Display sortable title (move artice to beginning of string)

    Returns:
        str: Converted title

    Example:
        Input: `sort_title('The Sample Title', c)`
        Output: Sample Title, The

    """

    article = ''
    base_title = ''
    t = ''

    def c(title):
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
        cstr = locals()[option](title)
    except KeyError:
        print('\nOption not recognized. Displaying help dialog...\n\ndef ' +
              sort_title.__name__ + '(title, option)\n\n' + sort_title.__doc__)
        exit()

    return cstr
