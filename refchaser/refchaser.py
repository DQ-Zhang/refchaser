# -*- coding: utf-8 -*-

"""
Extract information and reference lists of pdf academic articles with cermine.
"""

import re, os, subprocess
import refchaser.bibparser as bibparser

class RefChaser:
    """
    Class. Parses academic paper PDF files with a third party package CERMINE, extracts reference lists and return a search query of all references by joining titles with OR.
    You need to call methods to produce queries or retrive citations.
    Params:
        pdf_path -> path to the directory containing all PDF files to be extracted. It must not be path to a single pdf file because cermine only accepts a path to a directory as argument.
    Methods:
        back_query -> produces a query by joining all extracted references with Boolean operator OR for searching a database.
        forw_query -> produces a query by joining titles of index articles with Boolean operator OR for searching a database.
        back_WOS/PubMed/GS/EMBASE/Scopus -> retrieves extracted articles as citation files from Web of Science / NCBI PubMed / Google Scholar / EMBASE / Elsevier Scopus.
        forw_WOS/Scopus/GS -> retrieves citing articles as citation files from Web of Science / Scopus / Google Scholar.
    """

    def __init__(self, pdf_path, timeout=300):
        """
        Parses PDFs, extracts information, produces a list of instances of the citation class each containing results of an extracted PDF. Also records failures of extraction.
        """
        self.pdf_path = pdf_path
        self.timeout = timeout
        self.result_list = []
        self.failures = []
        self._main()

    def parse_with_cermine(self, pdf_path):
        """
        Method. Calls local CERMINE .jar file, returns the extraction results in JATS format.
        The CERMINE .jar package is version 1.13 and has "Main-Class: pl.edu.icm.cermine.ContentExtractor" appended to its MANIFEST.MF file.
        params:
            pdf_path: the full path to the directory containing pdf files to be parsed
        """

        subprocess.run("java -jar {}/cermine.jar -path {} -outputs jats -timeout {}".
            format(
            os.path.dirname(os.path.realpath(__file__)),
            pdf_path,
            str(self.timeout)))
        all_files_in_dir = os.listdir(pdf_path)
        result_files = list(filter(lambda item: item.endswith('.cermxml'), all_files_in_dir))
        result_file_names = list((x.split('.')[0] for x in result_files))
        self.failures = list(
            (x for x in all_files_in_dir if x.endswith('.pdf') and x.split('.')[0] not in set(result_file_names)))
        self.JATS_list = []
        for result_file in result_files:
            with open(pdf_path + '/' + result_file, 'r', encoding='latin1') as r:
                self.JATS_list.append(r.read())

    def JATS_extract(self, JATS):
        """
        Method. Further extract relevant information of an article from JATS format result, namely title and doi of index article and its reference list. 
        Each refernce is identified by its title, year of publication, journal and first author.
        Returns an instance of the class citation, including a ref_list attribute, also a list of instances of the class citation.
        params:
            JATS -> path to an XML-like file produced by cermine .jar after it extracts a pdf. Exists only after parse_with_cermine is called.
        """

        article = bibparser.Citation()

        # Extracting information of index articles.

        # extract title
        try:
            article.title = re.search(r'<article-title>(.*?)</article-title>', JATS, re.S).group(1)
        except:
            article.title = ''

        # extract doi
        try:
            article.doi = re.search(r'<article-id.*?>(.*?)</article-id>', JATS).group(1)
        except:
            article.doi = ''

        # identify references
        ref_list = re.findall(r'<ref id="ref\d{1,3}">(.*?)</ref>', JATS, re.S)

        # Extracting information of references
        for ref in ref_list:
            indiv_ref = bibparser.Citation()

            # extract authors
            authors_list = []
            try:
                authors = re.findall(r'<string-name>(.*?)</string-name>', ref, re.S)
                for author in authors:
                    try:
                        given_name = re.search(r'<given-names>(.*?)</given-names>', author).group(1)
                        given_name = given_name.replace(",", "").replace(";", "").replace(" ", "").replace("\n", "")
                        surname = re.search(r'<surname>(.*?)</surname>', author).group(1)
                        surname = surname.replace(",", "").replace(";", "").replace(" ", "").replace("\n", "")
                        author_name = surname + ", " + given_name
                        authors_list.append(author_name)
                    except:
                        pass
            except:
                pass
            if len(authors_list) == 0:
                authors_list = ['']
            indiv_ref.authors = authors_list
            indiv_ref.first_author = authors_list[0]
            #print(indiv_ref.first_author)

            # extract year
            try:
                year = re.search(r'<year>(\d{4})</year>', ref).group(1)
                indiv_ref.year = str(year)
            except:
                indiv_ref.year = ''

            # extract title
            try:
                potential_title = re.search(r'<article-title>(.*?)</article-title>', ref).group(1)
                indiv_ref.title = potential_title.replace('\n', '').replace('?', '').replace('*', '').replace(':',
                                                                                                              '').replace(
                    '>', '').replace('<', '').replace('|', '')
            except:
                indiv_ref.title = ''

            # extract journal
            try:
                indiv_ref.journal = re.search(r'<source>(.*?)</source>', ref, re.S).group(1)
            except:
                indiv_ref.journal = ''

            article.ref_list.append(indiv_ref)

        return article

    def combine_title_list(self, title_list, database, query_type='titles'):
        """
        Methods. Joins titles with the Boolean operator OR to create a search query. It is called in methods back_query and forw_query
        Searching a database of academic papers will return these refernces to be further screened.
        params:
            title_list -> list of titles of extracted articles
            database ->  what database you want to use your query on? must be one of the following: 'WOS','PubMed','EMBASE','GS','Scopus'
            query_type -> must be 'titles','dois' or 'first_author', 'titles' by default
        """
        title_list = list(set(title_list))  # remove duplicates
        final_query = []
        if query_type in ['titles', 'title', 'Title', 'Titles', 'TITLE', 'TITLES']:
            title_list = list(filter(lambda indiv_title: len(str(indiv_title)) > 20, title_list))
            for indiv_t in title_list:
                indiv_t = '"' + indiv_t.replace('\n', '').lstrip('/').rstrip('/').lstrip('\'').rstrip("\'").lstrip(
                    ' ').rstrip(' ') + '"'
                final_query.append(indiv_t)
        elif query_type in ['dois', 'doi', 'DOI', 'DOIS', 'DOIs', 'Dois', 'Doi']:
            title_list = list(filter(lambda indiv_title: re.search(r'10\.\d{4,9}/(\S+\.)?(\S+)', indiv_title) and len(
                indiv_title.split('.')) > 10, title_list))
            for indiv_t in title_list:
                indiv_t = '"' + indiv_t.replace('\n', '').lstrip('/').rstrip('/').lstrip('\\').rstrip('\\').lstrip(
                    ' ').rstrip(' ') + '"'
                final_query.append(indiv_t)
        else:
            for indiv_t in title_list:
                indiv_t = '"' + indiv_t.replace('\n', '').lstrip('/').rstrip('/').lstrip('\\').rstrip('\\').lstrip(
                    ' ').rstrip(' ') + '"'
                final_query.append(indiv_t)

        if database in ['1', 'WOS', 'Web of Science', 'web of science']:
            return 'TI=(' + ' OR '.join(final_query) + ")"  # example TI=("Title One" OR "Title Two" OR "Title Three")
        elif database in ['2', 'PubMed', 'PM', 'pubmed', 'Pubmed']:
            return '(' + '[Title]) OR ('.join(
                final_query) + '[Title])'  # example ("Title One"[Title]) OR ("Title Two"[Title]) OR ("Title Three"[Title])
        elif database in ['3', 'EMBASE', 'em', 'EM']:
            return ':ti OR '.join(final_query) + ':ti'  # example "Title One":ti OR "Title Two":ti OR "Title Three":ti
        elif database in ['4', 'Scopus', 'SCOPUS', 'scopus']:
            return 'TITLE(' + ' OR '.join(
                final_query) + ')'  # example TITLE("Title One" OR "Title Two" OR "Title Three")
        else:
            return ' OR '.join(final_query)  # example "Title One" OR "Title Two" OR "Title Three"

    def back_query(self, database):
        """
        Method. For searching backward. 
        Returns a query to search for the references of index articles as a string.
        You can print the query or save it to a .txt file.
        params:
            database: what database you want to search with your query? must be one of the following: 'WOS','PubMed','EMBASE','Scopus','GS'
        """
        titles_list = []
        for index_article in self.result_list:
            for citation in index_article.ref_list:
                titles_list.append(citation.title)
        return self.combine_title_list(titles_list, database)

    def forw_query(self, database, query_type='titles'):
        """
        Method. For searching backward. 
        Returns a query to search for articles that cite index articles as a string. You can print the query or save it to a .txt file.
        params:
            database: what database you want to use your query at? must be one of the following: 'WOS','PubMed','EMBASE','GS','Scopus'
            query_type -> must be 'titles','dois', 'first_author' or 'authors'. 'titles' by default
        """
        titles_list = []
        dois_list = []
        first_author_list = []
        authors_list = []
        for index_article in self.result_list:
            titles_list.append(index_article.title)
            dois_list.append(index_article.doi)
            first_author_list.append(index_article.first_author)
            authors_list.append(index_article.authors)
        if query_type in ['titles', 'title', 'Title', 'Titles', 'TITLE', 'TITLES']:
            return self.combine_title_list(titles_list, database, 'titles')
        elif query_type in ['dois', 'doi', 'DOI', 'DOIS', 'DOIs', 'Dois', 'Doi']:
            return self.combine_title_list(dois_list, database, 'dois')
        elif query_type in ['first_author', 'firstauthor', 'first author', '1st author', '1st_author', '1stauthor']:
            return self.combine_title_list(first_author_list, database, 'first_author')

    def save_ref_list(self, format_: str, save_to: str, separately: bool):
        if format_ in ['ris', '.ris', 'RIS']:
            format_fixed = 'ris'
        elif format_ in ['ciw', '.ciw', 'CIW']:
            format_fixed = 'ciw'
        elif format_ in ['nbib', '.nbib', 'NBIB']:
            format_fixed = 'nbib'
        elif format_ in ['bibtex', 'BibTeX', 'bib', '.bib']:
            format_fixed = 'bib'
        with open(self.pdf_path + 'index_articles_n={}.{}'.format(len(self.result_list), format_fixed), 'a',
                  encoding='utf-8') as index_articles:
            index_articles.writelines([x.write(format_) for x in self.result_list])
        if separately:
            for article in self.result_list:
                title_fixed = article.title.replace('-', ' ').replace.lstrip('/').rstrip('/').lstrip('\'').rstrip(
                    "\'").lstrip(' ').rstrip(' ').rstrip('.')
                with open(self.pdf_path + '/' + title_fixed + '.' + format_fixed, 'a',
                          encoding='utf-8') as indiv_reflist:
                    indiv_reflist.writelines([x.write(format_) for x in article.ref_list])
        else:
            with open(self.pdf_path + '/pooled_reflist.' + format_fixed, 'a', encoding='utf-8') as pooled_reflist:
                for article in self.result_list:
                    pooled_reflist.writelines([x.write(format_) for x in article.ref_list])

    def crosscheck_extracted_citations(self, citations):
        pass

    def back_WOS(self, saveto):
        pass

    def back_PubMed(self, saveto):
        pass

    def back_GS(self, saveto):
        pass

    def back_EMBASE(self, saveto):
        pass

    def back_Scopus(self, saveto):
        pass

    def forw_WOS(self, saveto):
        pass

    def forw_Scopus(self, saveto):
        pass

    def forw_GS(self, saveto):
        pass

    def _main(self):
        self.parse_with_cermine(self.pdf_path)
        for result in self.JATS_list:
            self.result_list.append(self.JATS_extract(result))
        failures_report = 'failed to parse the following %s items:' % (str(len(self.failures)))
        with open(self.pdf_path + '/report.txt', 'a', encoding='utf-8') as report:
            report.write(failures_report)
            report.writelines(self.failures)
        print(failures_report)
        print(self.failures)
