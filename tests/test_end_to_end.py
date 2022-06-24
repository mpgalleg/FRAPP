import FRAPP.FRAPP as frapp
import FRAPP
import subprocess

def test_end_to_end():
    """
    Tests basic functionality of our entire Frapp function.
    """
    #We need some arxiv examples:
    #
    arxiv_id1 = 'arXiv:2206.11631'
    
    arxiv_id2 = 'test0006'

    # Test first example:

    #print(p.communicate())
    #get path to arxiv_directory


    #test second example:  
    try:
         subprocess.run(['python', 'FRAPP.py', arxiv_id2])
    except:
       pass

test_end_to_end()