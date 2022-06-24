import FRAPP.FRAPP as frapp
import FRAPP

def test_setup_file():
    """
    Tests basic functionality of ``frapp.setup_file()``
    This function Sets up the new savefile by copying over the Latex packages and settings up to the abstract.
    """
    #how to go about this one. One option is to have a test input and output file. check if they match. 

    input_file1 = FRAPP.DATADIR+'example1/main.tex'
    input_file2 = FRAPP.DATADIR+'example2/aanda-MendezHernandez.tex'

    # The first example1 file works okay as the format conforms with the function
    full_text, newtext, start_ind_file1 = frapp.setup_file(input_file1)
    assert start_ind_file1 == 31
    #The 2nd example is a manuscript from aanda and the abstract structure is different from what we have considered. This should fail. 
    try:
        full_text, newtext, start_ind_file2 = frapp.setup_file(input_file2)
    except UnboundLocalError:
       pass

test_setup_file()