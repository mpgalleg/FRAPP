import subprocess

def make_pdf(frapped_tex_filename,path_to_tex_folder):
    """
    Compiles latex file with bolded letters

    Args: 
        frappified_tex (str): name of frappifed .tex file
        path_to_tex_folder (str): path to folder with all the latex files

    Returns:
        None: will produce a pdf in path_to_tex_folder 
    """
    subprocess.run(["pdflatex", frapped_tex_filename], cwd=path_to_tex_folder)




