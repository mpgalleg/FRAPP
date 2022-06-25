# FRAPP
Font-Facilitated Reading for Arxiv PDF Publications



### How to install:

    git clone https://github.com/mpgalleg/FRAPP.git

### Example Usage:

To FRAPPify any ArXiv paper

    cd FRAPP
    python FRAPP/FRAPP.py arXiv:2206.11701

or 

    python FRAPP/FRAPP.py arXiv:2206.11701 -o myFrappifiedFile

Note: Currently only AAS Journal formats are accepted. Accepted inputs can be any string/url that includes the ArXiv identifier numeric id. 

### Requirements:

    numpy
    subprocess
    pdflatex
Any LaTEX compiler, e.g., for Mac, you can use MacTEX

[![codeastro](https://img.shields.io/badge/Made%20at-Code/Astro-blueviolet.svg)](https://semaphorep.github.io/codeastro/)



