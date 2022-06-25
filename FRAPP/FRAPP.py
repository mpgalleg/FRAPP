# Code for navigating directories
# import os
# from os import path
# cd = os.chdir
#cd("/drive/Shared with me/")
import numpy as np
import re
import subprocess
import loadarxiv 
import sys
import PDF

# open .tex file you want to FRAPP
# Start with the assumption that the user has all source files saved locally
# Eventually, add functionality of downloading source code from a given link

def FRAPPify(filename="main.tex", savefile=None, compile=True):
  """FRAPPify
  
  The main user function for FRAPPifying an ArXiv paper. This function will save a modified .tex file

    Args: 
      filename (str): The name of the .tex file to be modified.

      savefile (str): The desired name of the modified .tex and .pdf output file. If none is given, the original filename with a _frapp modification will be used.
      
      compile (bool): Sets whether or not to compile the new .tex file into a PDF. 

    Returns:
      None  
  """ 

  ### First, sets up the new save file ###
  fulltext, newtext, abs_ind, frapped_file_name = setup_file(filename, savefile)
  ### CHANGE THE FULL TEXT TO PUT COMMENTS AND CITATIONS ON NEW LINES HERE ###
  #fulltext_new = format_text(fulltext)
  fulltext_new = fulltext.copy()
  
  ### From here on, check if line is text. If it is, start FRAPP procedure
  ### to make it work--editing only first 10 lines

  # Font used in Kindle reading mode: Bookerly, Ember and Ember Bold
  for ii, line in enumerate(fulltext_new[abs_ind+1:]): 

    if ii <10:
      # Skip all lines that begin with known formatting characters
      if line[0] == "\\" or line[0] == "%" or line[0] == "$": # Assume formatting code follows known pattern
        newtext.write(line)
        pass;
      else: # else, this is text!
        words = re.sub(r"([A-Z])", r" \1", line).split() # splits the line into words
        ## 'words' is the line split by spaces and capital letters.
        ## Treating each captial letter as the start of a new word
        ## allows the code to bold acronymns and camel-case words properly.

        for i, word in enumerate(words): # checks each word for compound structure
          word_split = re.split("(/|-)", word)
          ## Each 'word' may be a hyphenated/slash compound word
          ## word_split is a list of these words split by the hyphen/slash

          for j, w in enumerate(word_split): # word split by characters like - or /
            try: 
              if w[0].isalpha(): word_split[j] = modify_word_font(w) # FRAPPifying the word! 
            except: pass; # if word_split is a single word, modify_word_font still works

          ## Recombining all split parts
          words[i] = "".join(word_split) # recombining split word into single word
        newline = " ".join(words) # recombining all reformatted words into new line
      
        ## After line is reformatted into newline, write in text
        newtext.write(newline)
        newtext.write("\n")
      ## Repeat for the rest of the paper
    else:
      newtext.write(line)
  newtext.close()
  return frapped_file_name
### END of FRAPPify ###


def setup_file(filename, savefile=None): 
  """ setup_file
  
  Sets up the new savefile by copying over the Latex packages and settings up to the abstract.
      
    Args: 
      filename (str): 

      savefile (str): 
      
    Returns: 
      fulltext (list): A list containing all lines of the original .tex file.

      newtext (file): An open text file for saving the remaining lines in.

      abs_ind (int): The starting index of the abstract, from which the rest of the paper can be read.
  """

  # If no savefile name given, use filename w/ modification
  name = filename.split(".")[0] # remove filetype from filename
  if not savefile: 
    savefile = name + "_frapp"
  else: savefile = savefile.split(".")[0]

  # Read in file w/ filename
  with open(filename) as text: 
    fulltext = text.readlines() # list of lines from file

  # Opening the new savefile that will be built upon

  frapped_file_name = savefile+".tex"
  newtext = open(frapped_file_name, "w")

  ### FIND THE START OF THE PAPER ###
  ### may want to define this part at def setup_paper()
  ### which returns newtext
  # Searching for key lines in the paper: 
  #         \documentclass, to add \usepackage{setspace} beneath
  #         \begin{abstract} or \abstract to mark the beginning of the text

  for i in range(len(fulltext)):
    if "\documentclass" in fulltext[i]: docclass_ind = i
    elif fulltext[i][0] == "\\" and "abstract" in fulltext[i]:
      abs_ind = i # abstract index
      break;

  # Adding code before abstract + \usepackage{setspace} to the new paper
  for i in fulltext[0:docclass_ind+1]:
    newtext.write(i)
  newtext.write(r"\usepackage{setspace}"+'\n')
  for i in fulltext[docclass_ind+1:abs_ind]: 
    newtext.write(i)
  newtext.write(r"\sffamily")
  newtext.write(r"\setstretch{1.6}"+'\n')
  # Adding the abstract setup code (e.g. \begin{abstract} or \abstract)
  # changing this to abs_ind as this is the line that corresponds to \begin{abstract} command
  newtext.write(fulltext[abs_ind])
  newtext.write(r"\sffamily"+'\n')

  # From here, each line can be read in an FRAPPified accordingly. 
  return fulltext,newtext,abs_ind, frapped_file_name

def open_file(filename):

  # Reads in all lines from text file into a list,
  # with each line as a unique element in the list
  with open(filename) as text: 
    fulltext = text.readlines()

  # Saving the document intializing code (before \begin{abstract})
  # NOTE: Not all formats have \begin{abstract}
  #       Instead may have \abstract followed by paragraphs in {}
  #       Future developments should take this into account.
  # if fulltext[i][0] == "\\" and "abstract" in fulltext[i]:
  for i in range(len(fulltext)): 
    if "\\begin{abstract}" in fulltext[i]: 
      start_ind = i
      break;

  # start_ind = fulltext.index("\\begin{abstract}\n")
  # print(start_ind)
  docinit = fulltext[0:start_ind+1]
  # Add \setspacing and \sffamily somewhere before and within abstract
  abstract = fulltext[start_ind+1]

def bold_letter(word, split_index):
  """  
    Inserts LaTex code for applying bold-face to the appropriate letters. 
    
      Args: 
        word (str):

      Returns:
        new word (str):
   """
  return '\\textbf{'+ word[0:split_index] + '}' + word[split_index:]


def modify_word_font(word):
  """  

  This takes in one word from latex file, checks word length, and bolds appropriate letters. 
  
    Args:
      word (str): Word to be modified

    Returns:
      new_word (str): latex compatible modified word 

    Example:
      'espresso' -> '\\textbf{espr}esso' 
  """

  length = len(word) 
  if '$' in word or  '\\' in word or '{' in word or '}' in word:
    new_word = word

  else:
    if length <= 3:
      #only bold the first letter
      new_word = bold_letter(word, split_index=1) 

    elif length == 4:
      #only bold the first letter
      new_word = bold_letter(word, split_index=2) 
    
    else:
      #figure out a portion of word to bold
      #Our idea - capture first 2 vowels and then find next consonent
      
      split_index = int(np.ceil(length/2))

      # things to do:
      # 1. strip special characters
      # 2. 
      new_word = bold_letter(word, split_index)

  return new_word 

def test(a):
  abstract_word_list = abstract.split()
  for i, word in enumerate(abstract_word_list):
    abstract_word_list[i] = check_word(word)

  new_abstract = ' '.join(abstract_word_list)
  # consider using ' \ ' instead to space out the words more

  newtext = "".join(docinit) + new_abstract + "".join(fulltext[start_ind+2:])

  with open("testing.tex", "w") as f: 
    for i in docinit: 
      print(i)
      f.write(i)
    f.write(new_abstract)
    for i in fulltext[start_ind+2:]: 
      f.write(i)

  f.close()


def main():
  global main_tex, datadir
  input_arx_code = ''
  outputfile = None

  #processing user input
  nargs  = len(sys.argv)
  if nargs<2:
    print('Please provide input')
  input_arx_code = sys.argv[1]
  if nargs > 2:
    for i in range(2, nargs):
      if sys.argv[i] == '-o' and i+1 <nargs:
        outfile = sys.argv[i+1]
  print('ArXiv paper is {0}'.format(input_arx_code))
  print('Output file is {0}'.format(outputfile))

  # download ArXiv Source code and find the .tex file
  arx_source_url, arx_code = loadarxiv.stage_input_url(input_arx_code)
  main_tex, datadir = loadarxiv.download_arxiv_source(arx_source_url, arx_code)
  print('main tex file is {0} and the datadir is {1}'.format(main_tex, datadir))
  
  #Run FRAPPify
  frapped_file_name = FRAPPify(main_tex, savefile=outputfile)  
  
  # Run PDF:
  #print(frapped_file_name, datadir)
  PDF.make_pdf(frapped_file_name,path_to_tex_folder=datadir)


if __name__ == "__main__":
  main()

