import file_handler as f


def test_file_writer(new_keyword):
    f.log('TEST: Add new keyword \'' + new_keyword + '\'')
    f.add_keyword(new_keyword)
