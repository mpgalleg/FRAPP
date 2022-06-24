import FRAPP.FRAPP as frapp


def test_modify_word_font():
    """
    Tests basic functionality of ``frapp.modify_word()``
    This function takes in one word at a time from latex file, check for  a length and bold the appropriate portion
    
    """
    #unit testing options
    # empty string, string with $, \, or {} sign
    # String with numbers

    test_string_long = 'California'
    new_string_long = frapp.modify_word_font(test_string_long)

    test_string_short = 'CA'
    new_string_short = frapp.modify_word_font(test_string_short)


    test_empty  = ''
    new_string_empty = frapp.modify_word_font(test_empty)

    test_chars  = '\\test'
    new_string_chars = frapp.modify_word_font(test_chars)

    test_chars_2  = '\\test$$'
    new_string_chars_2 = frapp.modify_word_font(test_chars_2)

    test_chars_3  = 'numbers-123'
    new_string_chars_3 = frapp.modify_word_font(test_chars_3)

    assert new_string_long == '\\textbf{Calif}ornia'
    assert new_string_short == '\\textbf{C}A'
    assert new_string_chars == test_chars
    assert new_string_chars_2 == test_chars_2
    assert new_string_chars_3 == '\\textbf{number}s-123'
    
test_modify_word_font()