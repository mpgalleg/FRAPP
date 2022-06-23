
#import FRAPP.FRAPP 
import re
import os 
from urllib import request
import tarfile
import glob
import sys, getopt
import subprocess

def stage_input_url(arxiv_id):
    reg_pattern = '[0-9]{4}.[0-9]{5}'
    #identify arxiv id
    arx_pat = re.compile(reg_pattern)
    if arx_pat.search(arxiv_id):
        arx_code = arx_pat.search(arxiv_id).group()
    else:
        Exception('Provide a valid arxiv id or url.')
    arx_code = arx_code.rstrip()
    arx_source_url_pre  = 'https://arxiv.org/e-print/'
    arx_source_url = arx_source_url_pre + arx_code
    return arx_source_url, arx_code

def download_arxiv_source(arx_source_url, arx_code):
  arx_tar = arx_code+'.tar.gz' # check if extension is os dependant
  response = request.urlretrieve(arx_source_url, arx_tar)
  
  with tarfile.open(arx_tar) as tar_ref:
    tar_ref.extractall('./'+arx_code)
  
  datadir = './'+arx_code
  os.chdir(datadir)
  print(os.getcwd())
  #identify tex file
  main_tex = ''
  paper_tex_file = glob.glob('*.tex')
  print(paper_tex_file)
  if len(paper_tex_file) ==1:
    main_tex = paper_tex_file[0]
  elif len(paper_tex_file)<1:
    print('No .tex file found')
  else:
    paper_bbl_file = glob.glob('*.bbl')
    if len(paper_bbl_file)<1:
      print('No .tex file found')
    elif  len(paper_bbl_file)>1:
      print('Multiple .bbl files found. Please check the ArXiv Source code')
    else:
      bbl_file = paper_bbl_file[0]
      bbl_pre = bbl_file.split('.bbl')[0]
      main_tex = bbl_pre+'.tex'
  
  #clean up tar file
  subprocess.run(["rm", arx_tar]) # not working

  return main_tex, datadir  


def main():
  input_arx_code = ''
  outputfile = ''

  nargs  = len(sys.argv)
  if nargs<2:
    print('Please provide input')
  input_arx_code = sys.argv[1]
  if nargs > 2:
    for i in range(2, nargs):
      if sys.argv[i] == '-o' and i+1 <nargs:
        outfile = sys.argv[i+1]
  print('ArXiv paper is {0}'.format(input_arx_code))
  print('Output file is {0}'.format(outfile))
  arx_source_url, arx_code = stage_input_url(input_arx_code)
  main_tex, datadir = download_arxiv_source(arx_source_url, arx_code)
  print('main tex file is {0} and the datadir is {1}'.format(main_tex, datadir))
    

if __name__ == "__main__":
  main()




'''
# open .tex file you want to FRAPP
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


def check_word(word):

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
'''