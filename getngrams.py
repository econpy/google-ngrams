#!/usr/bin/env python
# -*- coding: utf-8 -*
from ast import literal_eval
from pandas import DataFrame  # http://github.com/pydata/pandas
import re
import requests               # http://github.com/kennethreitz/requests
import subprocess
import sys

corpora = dict(eng_us_2012=17, eng_us_2009=5, eng_gb_2012=18, eng_gb_2009=6,
               chi_sim_2012=23, chi_sim_2009=11, eng_2012=15, eng_2009=0,
               eng_fiction_2012=16, eng_fiction_2009=4, eng_1m_2009=1,
               fre_2012=19, fre_2009=7, ger_2012=20, ger_2009=8, heb_2012=24,
               heb_2009=9, spa_2012=21, spa_2009=10, rus_2012=25, rus_2009=12,
               ita_2012=22)


def getNgrams(query, corpus, startYear, endYear, smoothing, caseInsensitive):
    params = dict(content=query, year_start=startYear, year_end=endYear,
                  corpus=corpora[corpus], smoothing=smoothing,
                  case_insensitive=caseInsensitive)
    if params['case_insensitive'] is False:
        params.pop('case_insensitive')
    if '?' in params['content']:
        params['content'] = params['content'].replace('?', '*')
    if '@' in params['content']:
        params['content'] = params['content'].replace('@', '=>')
    req = requests.get('http://books.google.com/ngrams/graph', params=params)
    res = re.findall('var data = (.*?);\\n', req.text)
    if res:
        data = {qry['ngram']: qry['timeseries']
                for qry in literal_eval(res[0])}
        df = DataFrame(data)
        df.insert(0, 'year', list(range(startYear, endYear + 1)))
    else:
        df = DataFrame()
    return req.url, params['content'], df


def runQuery(argumentString):
    arguments = argumentString.split()
    query = ' '.join([arg for arg in arguments if not arg.startswith('-')])
    if '?' in query:
        query = query.replace('?', '*')
    if '@' in query:
        query = query.replace('@', '=>')
    params = [arg for arg in arguments if arg.startswith('-')]
    corpus, startYear, endYear, smoothing = 'eng_2012', 1800, 2000, 3
    printHelp, caseInsensitive, allData = False, False, False
    toSave, toPrint, toPlot = True, True, False

    # parsing the query parameters
    for param in params:
        if '-nosave' in param:
            toSave = False
        elif '-noprint' in param:
            toPrint = False
        elif '-plot' in param:
            toPlot = True
        elif '-corpus' in param:
            corpus = param.split('=')[1].strip()
        elif '-startYear' in param:
            startYear = int(param.split('=')[1])
        elif '-endYear' in param:
            endYear = int(param.split('=')[1])
        elif '-smoothing' in param:
            smoothing = int(param.split('=')[1])
        elif '-caseInsensitive' in param:
            caseInsensitive = True
        elif '-alldata' in param:
            allData = True
        elif '-help' in param:
            printHelp = True
        else:
            print(('Did not recognize the following argument: %s' % param))
    if printHelp:
        print('See README file.')
    else:
        if '*' in query and caseInsensitive is True:
            caseInsensitive = False
            notifyUser = True
            warningMessage = "*NOTE: Wildcard and case-insensitive " + \
                             "searches can't be combined, so the " + \
                             "case-insensitive option was ignored."
        elif '_INF' in query and caseInsensitive is True:
            caseInsensitive = False
            notifyUser = True
            warningMessage = "*NOTE: Inflected form and case-insensitive " + \
                             "searches can't be combined, so the " + \
                             "case-insensitive option was ignored."
        else:
            notifyUser = False
        url, urlquery, df = getNgrams(query, corpus, startYear, endYear,
                                      smoothing, caseInsensitive)
        if not allData:
            if caseInsensitive is True:
                for col in df.columns:
                    if col.count('(All)') == 1:
                        df[col.replace(' (All)', '')] = df.pop(col)
                    elif col.count(':chi_') == 1 or corpus.startswith('chi_'):
                        pass
                    elif col.count(':ger_') == 1 or corpus.startswith('ger_'):
                        pass
                    elif col.count(':heb_') == 1 or corpus.startswith('heb_'):
                        pass
                    elif col.count('(All)') == 0 and col != 'year':
                        if col not in urlquery.split(','):
                            df.pop(col)
            if '_INF' in query:
                for col in df.columns:
                    if '_INF' in col:
                        df.pop(col)
            if '*' in query:
                for col in df.columns:
                    if '*' in col:
                        df.pop(col)
        if toPrint:
            print((','.join(df.columns.tolist())))
            for row in df.iterrows():
                try:
                    print(('%d,' % int(row[1].values[0]) +
                           ','.join(['%.12f' % s for s in row[1].values[1:]])))
                except:
                    print((','.join([str(s) for s in row[1].values])))
        queries = ''.join(urlquery.replace(',', '_').split())
        if '*' in queries:
            queries = queries.replace('*', 'WILDCARD')
        if caseInsensitive is True:
            word_case = 'caseInsensitive'
        else:
            word_case = 'caseSensitive'
        filename = '%s-%s-%d-%d-%d-%s.csv' % (queries, corpus, startYear,
                                              endYear, smoothing, word_case)
        if toSave:
            for col in df.columns:
                if '&gt;' in col:
                    df[col.replace('&gt;', '>')] = df.pop(col)
            df.to_csv(filename, index=False)
            print(('Data saved to %s' % filename))
        if toPlot:
            try:
                subprocess.call(['python', 'xkcd.py', filename])
            except:
                if not toSave:
                    print(('Currently, if you want to create a plot you ' +
                           'must also save the data. Rerun your query, ' +
                           'removing the -nosave option.'))
                else:
                    print(('Plotting Failed: %s' % filename))
        if notifyUser:
            print(warningMessage)

if __name__ == '__main__':
    argumentString = ' '.join(sys.argv[1:])
    if argumentString == '':
        argumentString = eval(input('Enter query (or -help):'))
    else:
        try:
            runQuery(argumentString)
        except:
            print('An error occurred.')
