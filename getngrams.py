#!/usr/bin/env python
import ast
import pandas    # http://github.com/pydata/pandas
import re
import requests  # http://github.com/kennethreitz/requests
import sys

corpora = dict(eng_us_2012=17, eng_us_2009=5, eng_gb_2012=18, eng_gb_2009=6, 
               chi_sim_2012=23, chi_sim_2009=11,eng_2012=15, eng_2009=0,
               eng_fiction_2012=16, eng_fiction_2009=4, eng_1m_2009=1,
               fre_2012=19, fre_2009=7, ger_2012=20, ger_2009=8, heb_2012=24,
               heb_2009=9, spa_2012=21, spa_2009=10, rus_2012=25, rus_2009=12,
               ita_2012=22)


def getNgrams(query, corpus, startYear, endYear, smoothing):
    params = dict(content=query, year_start=startYear, year_end=endYear,
                  corpus=corpora[corpus], smoothing=smoothing)
    req = requests.get('http://books.google.com/ngrams/graph', params=params)
    response = req.content
    res = re.findall('data.addRows(.*?);', response.replace('\n',''))
    data = ast.literal_eval(res[0])
    return req.url, params['content'], data


def saveData(fname, query, data, url):
    df = pandas.DataFrame(data)
    df.columns = ['year'] + [q.strip() for q in query.split(',')]
    df.to_csv(fname, index=False, sep='\t')


def runQuery(argumentString):
    arguments = argumentString.split()
    query = ' '.join([arg for arg in arguments if not arg.startswith('-')])
    params = [arg for arg in arguments if arg.startswith('-')]
    corpus, startYear, endYear, smoothing = 'eng_2012', 1800, 2000, 3
    printHelp, toSave, toPrint = False, True, True
    
    # parsing the query parameters
    for param in params:
        if '-nosave' in param:
            toSave = False
        elif '-noprint' in param:
            toPrint = False
        elif '-corpus' in param:
            corpus = param.split('=')[1].strip()
        elif '-startYear' in param:
            startYear = int(param.split('=')[1])
        elif '-endYear' in param:
            endYear = int(param.split('=')[1])
        elif '-smoothing' in param:
            smoothing = int(param.split('=')[1])    
        elif '-help' in param:
            printHelp = True
        elif '-quit' in param:
            pass
        else:
            print 'Did not recognize the following argument:', param
    if printHelp:
        print 'See README file.'
    else:
        url, urlquery, data = getNgrams(query, corpus, startYear, endYear, smoothing)
        if toPrint:
            print url
            for d in data:
                try:
                    print '%d,'%int(d[0])+','.join([str(s) for s in d[1:]])
                except:
                    print ','.join([str(s) for s in d])
        if toSave:
            queries = ''.join(urlquery.replace(',', '_').split())
            filename = '%s-%s-%d-%d-%d.tsv' % (queries, corpus, startYear, endYear, smoothing)
            saveData(filename, urlquery, data, url)
            print 'Data saved to %s' % filename

if __name__ == '__main__':
    argumentString = ' '.join(sys.argv[1:])
    if '-quit' in argumentString.split():
        runQuery(argumentString)    
    if argumentString == '':
        argumentString = raw_input('Please enter an ngram query (or -help, or -quit):')
    while '-quit' not in argumentString.split():
        try:
            runQuery(argumentString)
        except:
            print 'An error occurred.'
        argumentString = raw_input('Please enter an ngram query (or -help, or -quit):')
