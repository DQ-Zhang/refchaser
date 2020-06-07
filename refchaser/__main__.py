from refchaser import bibparser, bioreader, massdownlit, querydatabase, refchaser
import argparse
from tkinter import filedialog as fd

parser = argparse.ArgumentParser()

mode_choices = ['1', '2', '3', '4', '5', '6', '7', '8', "A", "B", "C", "D", "E", "F", "G", "H", "a", "b", "c", "d", "e",
                "f", "g", "h"]
mode_help = '''
what do you want refchaser to do?
A: download full text articles
B: extract references
'''

parser.add_argument("mode", help=mode_help, choices=mode_choices)
parser.add_argument("-p", "--path", help="path to source files")
parser.add_argument("-t", "--to", help="path to save results to")
parser.add_argument("-x", "--extra", help="additional arguments", nargs="*")
args = parser.parse_args()


def mode_a():
    """
    API.
    Download pdf full texts articles of all citations in all bibliographic files in a directory
    to a designated directory.
    """
    if not args.path:
        pdf_path = fd.askdirectory(title="Please select a folder that contain all the bibliographic files")
        print("You selected:" + pdf_path)
    else:
        pdf_path = args.path
    if not args.to:
        save_pdf_to = fd.askdirectory(title="Please select a folder you want to save full text PDFs to")
        print("You selected:" + save_pdf_to)
    else:
        save_pdf_to = args.to

    massdownlit.MassDownLit(pdf_path, save_pdf_to)


def mode_b():
    """
    API.
    Parse all pdf articles in a directory,
    extract article titles and references,
    create forward and backward search queries for searching databases,
    save queries to a designated folder.
    """
    if not args.path:
        pdf_path = fd.askdirectory(title="Please select a folder that contain all the PDF files")
        print("You selected:" + pdf_path)
    else:
        pdf_path = args.path
    if not args.to:
        save_query_to = fd.askdirectory(title="Please select a folder you want to save query files to")
        print("You selected:" + save_query_to)
    else:
        save_query_to = args.to
    if not args.extra:
        database_prompt = '''
        In which database do you want to use your {} query?
        1 - WOS - Web of Science
        2 - PubMed -PubMed
        3 - EMBASE - EMBASE
        4 - Scopus - Scopus
        5 - GS - Google Scholar
        Please enter a number:
        '''
        forw_database = input(database_prompt.format("forward"))
        back_database = input(database_prompt.format("backward"))
    else:
        forw_database = args.extra[0]
        back_database = args.extra[1]

    cermine_parse = refchaser.RefChaser(pdf_path)
    with open(save_query_to + "/forw_query.txt", "w", encoding="utf-8") as forw:
        forw.write(cermine_parse.forw_query(forw_database))
    with open(save_query_to + "/back_query.txt", "w", encoding="utf-8") as back:
        back.write(cermine_parse.back_query(back_database))


if args.mode in ['1', 'A', 'a']:
    mode_a()

elif args.mode in ['2', 'B', 'b']:
    mode_b()

elif args.mode in ['3', 'C', 'c']:
    pass

elif args.mode in ['4', 'D', 'd']:
    pass

elif args.mode in ['5', 'E', 'e']:
    pass

elif args.mode in ['6', 'F', 'f']:
    pass

elif args.mode in ['7', 'G', 'g']:
    pass

elif args.mode in ['8', 'H', 'h']:
    pass
