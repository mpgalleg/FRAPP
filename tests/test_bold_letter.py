import FRAPP.FRAPP as frapp

def test_bold_letter():
    """
    Tests basic functionality of ``frapp.bold_letter()``
    """
    test_string_long = 'California'
    new_string_long = frapp.bold_letter(test_string_long,3)

    test_string_short = 'CA'
    new_string_short = frapp.bold_letter(test_string_short,1)

    assert new_string_long == '\\textbf{Cal}ifornia'
    assert new_string_short == '\\textbf{C}A'

test_bold_letter()