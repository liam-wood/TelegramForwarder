from datetime import datetime


def get_keywords():
    # Returns a list of keywords from text file
    keywords_file = open(r"keywords", "r")
    keywords = keywords_file.readlines()
    keywords_file.close()
    return keywords


def get_commands():
    # Returns a list of commands from text file
    commands_file = open(r"commands", "r")
    cmds: list[str] = commands_file.readlines()
    commands_file.close()
    return cmds


def add_keyword(word):
    # Add keyword to text file
    try:
        keywords_file = open(r"keywords", "a")
        keywords_file.writelines(word.lower() + '\n')
        keywords_file.close()
        log('Keyword ' + word + ' successfully added.')
    except:
        log('Error occurred. Could not add keyword ' + word)


def remove_word(word, new_keywords):
    # Essentially delete everything and write all the keywords to the blank file
    try:
        keywords_file = open(r"keywords", "a")
        keywords_file.truncate(0)
        for x in new_keywords:
            keywords_file.write(x.lower())
            log(f'Word written: ' + x)
        log(f'New keywords written.')
        keywords_file.close()
    except:
        log('Error occurred. Could not remove keyword ' + word)


def log(text):
    # Prints to console as normal but also adds to a text file for logging
    print('(' + datetime.now().strftime("%d/%m/%Y") + ', ' + datetime.now().strftime("%H:%M:%S") + '): ' + text)
    # log_file = open(r"message_log", "a")
    # log_file.writelines(text + '\n')
    # log_file.close()


def get_ids():
    # Gets important info. Need a way of making this secure
    # 0 = API ID
    # 1 = API hash
    # 2 = Chat ID

    id_file = open(r"sensitive", "r")
    ids = id_file.readlines()
    id_file.close()
    return ids


def save_ids(ids):
    # Save new list of IDs to text file. Will need making more secure eventually
    id_file = open(r"sensitive", "a")
    for x in ids:
        id_file.writelines(ids[x])
    log('"IDs" file overwritten. ')
    id_file.close()


def get_counts():
    count_file = open(r"process_count", "r")
    counts = count_file.readlines()
    count_file.close()
    return counts


def save_counts(messages, matches):
    # Essentially delete everything rewrite the count file showing
    # number of messages processed and how many matches have been found
    try:
        count_file = open(r"process_count", "a")
        count_file.truncate(0)
        count_file.writelines(str(messages) + '\n')
        count_file.writelines(str(matches) + '\n')
        log(f'Messages processed: ' + str(messages))
        log(f'Matches processed: ' + str(matches))
        log(f'Count file overwritten.')
        count_file.close()
    except:
        log('Could not save count file')
