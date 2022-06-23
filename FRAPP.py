# Code for navigating directories
# import os
# from os import path
# cd = os.chdir
#cd("/drive/Shared with me/")
import numpy as np

# open .tex file you want to FRAPP
def open_file(a):
  with open("main.tex") as text: 
    fulltext = text.readlines()

  # Saving the document intializing code (before \begin{abstract})
  for i in range(len(fulltext)): 
    if "\\begin{abstract}" in fulltext[i]: 
      start_ind = i
      break;

  # start_ind = fulltext.index("\\begin{abstract}\n")
  # print(start_ind)
  docinit = fulltext[0:start_ind+1]
  abstract = fulltext[start_ind+1]

def bold_letter(word, split_index):
  return '\\textbf{'+ word[0:split_index] + '}' + word[split_index:]


def modify_word_font(word):
  """ Modify word font 

  This takes in one word from latex file, checks word length, and bolds appropriate letters. 
  
  Args:
    word (str): Word to be modified

  Returns:
    str: latex compatible modified word 

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

  newtext = "".join(docinit) + new_abstract + "".join(fulltext[start_ind+2:])

  with open("testing.tex", "w") as f: 
    for i in docinit: 
      print(i)
      f.write(i)
    f.write(new_abstract)
    for i in fulltext[start_ind+2:]: 
      f.write(i)

  f.close()