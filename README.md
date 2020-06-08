Refchaser Provisional User Guide
=================================
This package is developed as a toolbox for conducting literature reviews and systematic reviews. It allows downloading full text articles in batches. It can parse the reference lists of pdf articles for searching reference list.  

The latest version is 0.0.3  

Currently, it only support Windows systems.  

Although the use of python packages usually requires some programming knowledge, refchaser provides quick APIs to be called in commandline, which even lay people can use.  

Acknowledgement to developers of [CERMINE](https://github.com/CeON/CERMINE.git)

***
***What do I need to install before using refchaser?***  
You need to install the following programming languages.  

[python 3](https://www.python.org/downloads/)

[Java](https://www.java.com/en/download/windows-64bit.jsp)

[R](https://www.r-project.org/)

Although this is a python module, it works by calling third-party applications written in the other two languages.
Make sure to add the executables of these languages to [PATH environment variable](https://en.wikipedia.org/wiki/PATH_(variable))
***
***How to install refchaser?***  

After you have installed python 3, open cmd.exe.    

Run command:  


    pip install refchaser
***
***How to get help?***  

Open cmd.exe  

Run command:  


    python -m refchaser -h
***
***How to batch-download articles?***  

Open cmd.exe  

Run command:  


    python -m refchaser A -p C://directory/containing/bibliographical/files/ -t C://directory/where/you/want/fulltexts/saved/

The `-p` parameter should contain nothing else than bibiographic files of citations you want to download.
The `-t` is a folder where you want to save all the downloaded PDF articles.  

Alternatively, you can just run this command:  


    python -m refchaser A

And a graphic user interface will guide you through.
***
***How to parse reference lists of pdf articles and generate queries?***  

Open cmd.exe  

Run command:  


    python -m refchaser B -p C://directory/containing/pdf/files/ -t C://directory/where/you/want/queries/saved -x WOS PubMed

The database names pass to the `-x` can be numbers

    python -m refchaser B -p C://directory/containing/pdf/files/ -t C://directory/where/you/want/queries/saved -x 1 2

The mapping relationships are as follows:

    1 - WOS - Web of Science
    2 - PubMed -PubMed
    3 - EMBASE - EMBASE
    4 - Scopus - Scopus
    5 - GS - Google Scholar

The `-p` parameter should contain nothing else than PDF files you want parsed.  
The `-t` is a folder where you want to save forward search queries (consisting of titles of parsed articles) and backward search queries (consisting of titles of references) in .txt format.  
The `-x` parameter is the databases you want to search with the forward and backward query, respectively. The package can create queries according to search rules of different databases.  

Alternatively, you can just run this command:

    python -m refchaser B

And a graphic user interface will guide you through.
