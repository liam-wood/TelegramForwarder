import file_handler as f
import re

cmds = f.get_commands()


def find_word_in_string(w):
    # Checks if string contains keywords. FUNCTION FORMAT > find_word_in_string(keyword)(textToCheck)
    # Dunno how tf it works I just copied and pasted off StackOverflow
    return re.compile(r'\b({0})\b'.format(w), flags=re.IGNORECASE).search


def check_for_keywords(text, keywords):
    #   This function searches for specific keywords within the message

    matched = []            # list of keywords that match to supplied text
    matching = False        # false by default, changes to true if 1 or more matches

    f.log(f'Checking for keywords...')
    for x in keywords:
        x = x.removesuffix('\n')
        if find_word_in_string(x)(text):
            matched.append(x)
            matching = True

    if not matching:
        f.log('No keywords matched.')
        return False
    else:
        f.log('Keywords matched: ')
        for x in matched:
            f.log(x.removesuffix('\n'))

    return True


def check_cmd(text):
    # Checks if the input starts with a command phrase
    f.log(f'Checking for commands...')
    is_command = False
    for x in cmds:
        if text.startswith(x.removesuffix('\n')):
            f.log('This is a command: ' + x)
            is_command = True
    if not is_command:
        f.log(f'This isn\'t a command.')
    return is_command


def process_command(text, keywords):
    f.log('TEXT: ' + text)

    # ADD KEYWORD
    if text.startswith('/add '):
        new_keyword = text[5:]
        f.log('Command: add new keyword ' + new_keyword)
        for x in keywords:
            if find_word_in_string(new_keyword)(x):
                return 'This is already in the list of keywords.'
        f.add_keyword(new_keyword)
        keywords.append(new_keyword + '\n')
        return 'Added new keyword: ' + new_keyword

    # REMOVE KEYWORD
    elif text.startswith('/remove '):
        remove_word = text[8:]
        word_length = len(remove_word)
        # Check if keyword is in current list
        word_exists = False
        for x in keywords:
            if find_word_in_string(remove_word)(x):
                word_exists = True
        if word_exists:
            f.log(f'Word length: ' + remove_word + ' = ' + str(word_length))
            f.log('Command: remove keyword: ' + remove_word)
            for x in keywords:
                f.log(f'Word length = ' + x[0:word_length] + ' | remove_word = ' + remove_word)
                if x[0:word_length] == remove_word:
                    f.log(f'Word length matches keyword length')
                    keywords.remove(x)
            f.remove_word(remove_word, keywords)
            return 'Keyword removed: ' + remove_word
        else:
            return 'Keyword ' + remove_word + ' is not in the current list.'

    # PRINT LIST OF KEYWORDS
    elif text == '/keywords':
        f.log('Command: show keywords')
        message = 'List of keywords:\n'
        for x in keywords:
            message += x
        return message
    else:
        return 'Could not process command.'
