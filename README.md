# About #
Here you'll find a basic python script to retrieve data behind the trajectories plotted on the [Google Books Ngram Viewer](http://books.google.com/ngrams).

Just type exactly the same string you would have typed at books.google.com/ngrams, and retrieve the data in csv format. By default, the data is printed on screen and saved to a file in the current directory.

 1. You can directly pass queries as arguments to the python script, such as "python getngrams.py awesome".
 2. If you pass the '-quit' flag as an argument, the program will run once and quit without asking for more input, such as "python getngrams.py awesome, sauce -quit".     
 3. Known caveat: quotation marks are removed from the input query. 

### Example Usage ###

```
python getngrams.py Albert Einstein, Charles Darwin
python getngrams.py internet --startYear=1980 --endYear=2000 --corpus=eng_2012 --caseInsensitive=on
python getngrams.py Pearl Harbor, Watergate -corpus=eng_2009 -nosave 
python getngrams.py bells and whistles -startYear=1900 -endYear=2001 -smoothing=2
python getngrams.py aluminum, copper, steel -noprint -quit
```

### Flags ###
  * **corpus** [default: eng_2012] *This will run the query in CORPUS. Possible values are recapitulated below and [here](http://books.google.com/ngrams/info)*
  * **startYear** [default: 1800]
  * **endYear** [default: 2000]
  * **smoothing** [default: 3] *Smoothing parameter (integer). Minimum is 0.*
  * **caseInsensitive** [default: off] *Set to 'on' for case-insensitive queries*
  * **nosave** *Results will not be saved to file*
  * **noprint** *Results will not be printed on screen*
  * **help** *Prints this screen*
  * **quit** *Quits after running query*

### Possible Corpora ###

```
eng_2012, eng_2009, eng_us_2012, eng_us_2009, eng_gb_2012, eng_gb_2009,
chi_sim_2012, chi_sim_2009, fre_2012, fre_2009, ger_2012, ger_2009,
spa_2012, spa_2009, rus_2012, rus_2009, heb_2012, heb_2009, ita_2012,
eng_fiction_2012, eng_fiction_2009, eng_1m_2009
```

### Plotting ###
One way to plot data from a csv file created from the getngrams.py script is
to read the csv file into a pandas DataFrame object and call the .plot()
option on it.

For example, open an IPython terminal in the directory with a csv file with a
pylab inline plotting backend (e.g. ipython --pylab=inline). Then you can do
something like the following:

```python
import pandas
df = pandas.read_csv('aluminum_copper_steel_zinc-eng_2012-1800-2000-3.csv', index_col=0, parse_dates=True)
df.plot()
```

which will produce an image like this:
![](https://s3.amazonaws.com/ngramplots/ngrams.png)

### License ###
None, feel free to distribute and modify.

However, PLEASE do respect the terms of service of the Google Books Ngram Viewer while using this code. This code is meant to help viewers retrieve data behind a few queries, not bang at Google's servers with thousands of queries. The complete dataset can be freely downloaded [here](http://storage.googleapis.com/books/ngrams/books/datasetsv2.html). This code is not a Google product and is not endorsed by Google in any way. 

With this in mind... happy plotting!
