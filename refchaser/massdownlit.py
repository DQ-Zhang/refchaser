# -*- coding: utf-8 -*-

"""
Downloads full texts of citations from sci-hub.
"""

from scidownl.scihub import SciHub
import os, time, eventlet
import refchaser.bibparser as bibparser


class MassDownLit():
    """
    Class. Downloads full texts of citations from sci-hub, via the python package scidownl.
    You need to enter a path to a bibliographic file of the RIS, .ciw, .nbib or BiBTeX format, and all citations indexed in it will be downloaded to a folder you designate.
    If you have multiple bibliographic files, put them in the same folder and enter path to that folder. All citations in all files will be downloaded to another folder you designate.
        params:
        path -> path to either a directory containing bibliographic files, or to a bibliographic file.
        save_pdf_to -> Path to the folder where full texts shall be saved, must be in the format of r'C:\\User\\full_texts'.
        in_sep_folders -> Valid when path is a to directory. Whether or not to save full texts to seperate folders under the save_pdf_to folder, named after respective txt file that indexes them. True by default.
        reports -> whether or not to generate a download report. True by default.
        timeout -> how many seconds before the script should stop waiting while trying to download an individual pdf. an integer. 300 by default.
    """

    def __init__(self, path: str, save_pdf_to: str, in_sep_folders=True, reports=True, timeout=300):
        self.timeout = timeout
        self._main(path, save_pdf_to, in_sep_folders, reports)

    def info_extract(self, file_path):
        """
        Method. Extracts article information from .ris/.ciw/.nbib/BibTeX bibliographic files.
        params:
            file_path -> path to a bibliographic file of RIS/CIW/NBIB/BibTeX format.
        Returns a list of instances of the citation class.
        """
        self.batch_name = file_path.split('\\')[-1].split('.')[0]
        citation_list = bibparser.BibFile(file_path).parse()
        return citation_list

    def down_pdf(self, citation_list: list, save_pdf_to: str, report=True):
        """
        Method. Takes in a list of instances of the citation class, downloading full texts from Scihub to a folder
        params
            citation_list -> a list of instances of the class citation.
            save_pdf_to -> the path to the directory where downloaded full texts are saved.
        """
        self.Failures = []
        self.num_articles = len(citation_list)
        print('Ready to download %d articles from SciHub' % (self.num_articles))
        counter = 0
        prompt = ''
        start_time = time.time()
        for article in citation_list:
            counter += 1
            try:
                for i in range(0, 3):
                    try:
                        with eventlet.Timeout(self.timeout):
                            SciHub(article.doi, save_pdf_to).download()
                            prompt = "Article number %d downloaded successfully, %d articles remaining" % (
                                counter, self.num_articles - counter)
                            print(prompt)
                            break
                    except eventlet.Timeout:
                        print("Timeout! Retrying download.")
                        if i == 2:
                            raise Exception
                        continue
            except:
                prompt = "Article number %d downloaded unsuccessfully, %d articles remaining " % (
                    counter, self.num_articles - counter)
                self.Failures.append(article)
        end_time = time.time()
        if report == True:
            report_name = r'\%s_report' % (self.batch_name)
            report_path = save_pdf_to + report_name + '.txt'
            report_path = report_path.replace(r'\\', '\\')
            if not os.path.exists(save_pdf_to):
                os.makedirs(save_pdf_to)
            with open(report_path, 'a', encoding='utf-8') as report:
                General_rep = [
                    'Total number of articles identified from bibliographic file: %s\n' % (str(self.num_articles)),
                    'Number of downloads attempted: %s\n' % (str(counter)),
                    'Number of articles successfully retrieved: %d\n' % (int(counter) - len(self.Failures)),
                    'Time taken: %s\n seconds' % (str(end_time - start_time))
                ]
                report.writelines(General_rep)
                report.write('\nA total of %d articles were not downloaded. Please manually retrive them.\n' % (
                    len(self.Failures)))
                Failures_str = []
                for Failed_article in self.Failures:
                    Failed_article = str(Failed_article.title) + ' DOI: ' + str(Failed_article.doi) + '\n'
                    Failures_str.append(Failed_article)
                report.writelines(Failures_str)

    def litdown(self, file_path: str, save_pdf_to: str, in_sep_folders=False, report=True):
        """
        Method. Downloads articles indexed in one blibliographic file to a folder
        param:
            file_path -> Path to the endnote "All Fields" export file, must be in the format of r'C:\\User\\citations.txt'.
            save_pdf_to -> Path to the directory where downloaded full texts shall be saved, must be in the format of r'C:\\User\\full_texts'.
            report -> whether or not to generate a download report. True by default.
        """
        save_to = lambda: save_pdf_to + '\\' + file_path.split('\\')[-1] if in_sep_folders else save_pdf_to
        self.down_pdf(citation_list=self.info_extract(file_path), save_pdf_to=save_to(), report=report)

    def massdown(self, dir_path: str, save_pdf_to: str, in_sep_folders=True, reports=True):
        """
        Method. Downloads articles indexed in all blibliographic files in a folder, to a designated folder or to seperate folders under it
        params:
            dir_path -> Path to the folder endnote "All Fields" export files, must be in the format of r'C:\\User\\citations'.
            save_pdf_to -> Path to the folder where full texts shall be saved, must be in the format of r'C:\\User\\full_texts'.
            in_sep_folders -> whether or not to save full texts to seperate folders under the save_pdf_to folder, named after respective txt file that indexes them. True by default.
            report -> whether or not to generate a download report. True by default.
        """
        for txt in os.listdir(dir_path):
            folder_name = os.path.basename(save_pdf_to + '\\' + txt).rstrip('.txt')
            save_to = lambda: save_pdf_to + '\\' + folder_name if in_sep_folders else save_pdf_to
            self.litdown(file_path=dir_path + '\\' + txt, save_pdf_to=save_to(), report=reports)

    def _main(self, path: str, save_pdf_to: str, in_sep_folders=True, reports=True):
        """
        Main function. Downloads full texts of articles indexed in a citation file, or multiple citation files under the same folder.
        params:
            path -> path to either a directory containing bibliographic files, or to a bibliographic file.
            save_pdf_to -> Path to the folder where full texts shall be saved, must be in the format of r'C:\\User\\full_texts'.
            in_sep_folders -> Valid when path is a to directory. Whether or not to save full texts to seperate folders under the save_pdf_to folder, named after respective txt file that indexes them. True by default.
            reports:whether or not to generate a download report. True by default.
        """
        for i in [path, save_pdf_to]:
            i = os.path.abspath(i).replace("/", "\\")
        if os.path.isdir(path):
            self.massdown(dir_path=path, save_pdf_to=save_pdf_to, in_sep_folders=in_sep_folders, reports=reports)
        elif os.path.isfile(path):
            self.litdown(file_path=path, save_pdf_to=save_pdf_to, report=reports)
        else:
            raise Exception('path %s is incorrect' % (path))
