# -*- coding: utf-8 -*-

"""
Reads bibliographical files: RIS, BibTeX, etc.
"""

import re, os

ris_map = {
    "TI": "title",
    "TY": "article_type",
    "PY": "year",
    "AU": "authors",
    "NA": "first_authors",
    "DO": "doi",
    "JF": "journal",
    "AB": "abstract",
    "KW": "keywords",
    "NA1": "databaseID"
}

ciw_map = {
    "TI": "title",
    "NA1": "article_type",
    "PY": "year",
    "AF": "authors",
    "NA": "first_authors",
    "DI": "doi",
    "SO": "journal",
    "AB": "abstract",
    "NA2": "keywords",
    "NA3": "databaseID"
}

nbib_map = {
    "TI": "title",
    "PT": "article_type",
    "DP": "year",
    "FAU": "authors",
    "NA1": "first_authors",
    "ID": "doi",
    "JT": "journal",
    "AB": "abstract",
    "OT": "keywords",
    "PMID": "databaseID"
}

bib_map = {
    "title": "title",
    "type": "article_type",
    "year": "year",
    "author": "authors",
    "NA1": "first_authors",
    "DOI": "doi",
    "journal": "journal",
    "NA2": "abstract",
    "NA3": "keywords",
    "NA4": "databaseID"
}

txt_tab_delim_map = {

}

txt_all_fields_map = {

}


class Citation:
    """
    definition of citation
    """

    def __init__(self, title='', article_type='', year='', authors=[], first_author='', doi='', journal='', abstract='',
                 keywords=[], databaseID='', ref_list=[]):
        self.title = title
        self.article_type = article_type
        self.year = year
        self.authors = authors
        self.first_author = first_author
        self.doi = doi
        self.journal = journal
        self.abstract = abstract
        self.keywords = keywords
        self.databaseID = databaseID
        self.ref_list = ref_list

    def dict_to_citation(self, dict_):
        pass

    def citation_as_dict(self):
        pass

    def write(self, format_: str):
        if format_ in ['ris', '.ris', 'RIS']:
            return self.write_ris()
        if format_ in ['ciw', '.ciw', 'CIW']:
            return self.write_ciw()
        if format_ in ['nbib', '.nbib', 'NBIB']:
            return self.write_nbib()
        if format_ in ['bibtex', 'BibTeX', 'bib', '.bib']:
            return self.write_bib()

    def write_ris(self):
        pass

    def write_ciw(self):
        pass

    def write_nbib(self):
        pass

    def write_bib(self):
        pass


class BibFileReady:
    """
    object must be a bibliography file, already read and seperated into individual citations
    """
    batch_name = ''
    filename_extension = ''
    citation_list = []
    temp_dict = {}

    def __init__(self, indiv_article_info, batch_name, filename_extension):
        self.indiv_article_info = indiv_article_info
        self.filename_extension = filename_extension

    def parse(self):
        if self.filename_extension == '.ris':
            return self.parse_ris()
        elif self.filename_extension == '.ciw':
            return self.parse_ciw()
        elif self.filename_extension == '.nbib':
            return self.parse_nbib()
        elif self.filename_extension == '.bib':
            return self.parse_bib()
        elif self.filename_extension == '.txt':
            try:
                return self.parse_txt_all_fields()
            except:
                return self.parse_txt_tab_delim()

    def _citation_list_append(self, citation_list):
        #print(self.temp_dict, self.filename_extension)
        citation_list = citation_list
        citation_ = Citation(
            self.temp_dict["title"],
            self.temp_dict["article_type"],
            self.temp_dict["year"],
            self.temp_dict["authors"],
            self.temp_dict["first_authors"],
            self.temp_dict["doi"],
            self.temp_dict["journal"],
            self.temp_dict["abstract"],
            self.temp_dict["keywords"]
        )
        citation_list.append(citation_)
        self.temp_dict = {}
        return citation_list

    def parse_ris(self):
        citation_list = []
        for item in self.indiv_article_info:
            for field in ris_map:
                if field not in ['AU']:
                    try:
                        self.temp_dict[ris_map[field]] = re.search(r'\n%s  - (.*)\n[A-Z]{2}  - ' % (field), item).group(
                            1).replace('\n', '')
                    except:
                        self.temp_dict[ris_map[field]] = ''
                else:
                    try:
                        self.temp_dict[ris_map[field]] = re.findall(r'\n%s  - (.*)\n[A-Z]{2}  - ' % (field), item)
                    except:
                        self.temp_dict[ris_map[field]] = ['']

            self.temp_dict['first_authors'] = self.temp_dict['authors'][0]
            try:
                self.temp_dict['keywords'] = self.temp_dict['keywords'].split('\n')
            except:
                self.temp_dict['keywords'] = ['']
            citation_list = self._citation_list_append(citation_list)

        return citation_list

    def parse_ciw(self):
        citation_list = []
        for item in self.indiv_article_info:
            for field in ciw_map:
                if field not in ['AF']:
                    try:
                        self.temp_dict[ciw_map[field]] = re.search(r'\n%s (.*)' % (field), item).group(1).replace('\n',
                                                                                                                  '')
                    except:
                        self.temp_dict[ciw_map[field]] = ''
                elif field in ['AF']:
                    try:
                        self.temp_dict[ciw_map[field]] = re.search(r'\nAF (.*)\n[A-Z]{2}' % (field), item).group(
                            1).split('\n   ')
                    except:
                        self.temp_dict[ciw_map[field]] = ['']

            self.temp_dict['first_authors'] = self.temp_dict['authors'][0]
            citation_list = self._citation_list_append(citation_list)

        return citation_list

    def parse_nbib(self):
        citation_list = []
        for item in self.indiv_article_info:
            for field in nbib_map:
                if field not in ['FAU', 'ID', 'OT']:
                    try:
                        self.temp_dict[nbib_map[field]] = re.search(r'%s {0,2}- (.*?)[A-Z]{2,4}' % (field), item,
                                                                    re.S).group(1).replace('\n', '')
                    except:
                        self.temp_dict[nbib_map[field]] = ''
                elif field not in ['ID']:
                    try:
                        self.temp_dict[nbib_map[field]] = re.findall(r'%s {0,2}- (.*)\n[A-Z]{2,4}' % (field), item)
                    except:
                        self.temp_dict[nbib_map[field]] = ['']

            try:
                self.temp_dict['first_authors'] = self.temp_dict['authors'][0]
            except:
                self.temp_dict['authors'] = ['']
                self.temp_dict['first_authors'] = ''
            try:
                self.temp_dict['year'] = re.search(r'(\d{4})', self.temp_dict['year']).group(1)
            except:
                pass
            try:
                self.temp_dict['doi'] = re.search(r'ID - (.*) \[doi\]', item, re.M).group(1)
            except:
                self.temp_dict['doi'] = ''
            citation_list = self._citation_list_append(citation_list)

        return citation_list

    def parse_bib(self):
        citation_list = []
        for item in self.indiv_article_info:
            # print(item)
            for field in bib_map:
                try:
                    self.temp_dict[bib_map[field]] = re.search(r'%s = \{(.*?)\}' % (field), item).group(1)
                except:
                    self.temp_dict[bib_map[field]] = ''

            self.temp_dict['authors'] = self.temp_dict['authors'].split('and')
            if self.temp_dict['article_type'] == '':
                self.temp_dict['article_type'] = re.search(r'\@(.*?)\{', item).group(1)
            self.temp_dict['first_authors'] = self.temp_dict['authors'][0]
            if self.temp_dict['keywords'] == '':
                self.temp_dict['keywords'] = ['']
            citation_list = self._citation_list_append(citation_list)

        return citation_list

    def parse_txt_tab_delim(self):
        pass

    def parse_txt_all_fields(self):
        pass


class BibFileRead(BibFileReady):
    '''
    definition of bib_file_read
    '''
    batch_name = ''
    filename_extension = ''
    citation_list = []
    temp_dict = {}

    def __init__(self, file_text, batch_name, filename_extension):
        self.file_text = file_text
        self.indiv_article_info = file_text.split('\n\n')
        self.filename_extension = filename_extension


class BibFile(BibFileReady):
    """
    definition of bib_file
    """
    batch_name = ''
    filename_extension = ''
    citation_list = []
    temp_dict = {}

    def __init__(self, file_path):
        self.file_path = os.path.abspath(file_path).replace("/", "\\")
        with open(self.file_path, 'r', encoding='utf-8') as read_str:
            self.filename_extension = os.path.splitext(self.file_path)[1]
            self.file_text = read_str.read()
            self.indiv_article_info = self._seperate_refs(self.file_text, self.filename_extension)

    def _seperate_refs(self, file_text, filename_extension):
        if filename_extension == '.ris':
            return [i for i in re.split('\nER(.*?)\n', file_text) if len(i) > 10]
        elif filename_extension == '.ciw':
            return [i for i in re.split('\nER(.*?)\n', file_text) if len(i) > 10]
        elif filename_extension == '.nbib':
            return [i for i in file_text.split('\n\n') if len(i) > 10]
        elif filename_extension == '.bib':
            return [i for i in file_text.split('\n\n') if len(i) > 10]
        else:
            raise Exception("file type not supported")
