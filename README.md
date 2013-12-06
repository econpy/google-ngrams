# About #
Here you'll find a basic python script to retrieve data behind the trajectories plotted on the [Google Ngram Viewer](http://books.google.com/ngrams).

Just type exactly the same string you would have typed at books.google.com/ngrams, and retrieve the data in csv format. By default, the data is printed on screen and saved to a file in the current directory.

 - You can directly pass queries as arguments to the python script, such as "python getngrams.py awesome".
 - If you pass the '-quit' flag as an argument, the program will run once and quit without asking for more input, such as "python getngrams.py awesome, sauce -quit".
 - Searches are case-sensitive by default, but case-insenitive searches can be performed by adding the `--caseInsensitive=on` argument to your query.
 - Known Caveat: Quotation marks are removed from the input query.

### Basic Examples ###

Here are some basic example uses of `getngrams.py`:

```
python getngrams.py Albert Einstein, Charles Darwin
python getngrams.py aluminum, copper, steel -noprint -quit
python getngrams.py Pearl Harbor, Watergate -corpus=eng_2009 -nosave
python getngrams.py bells and whistles -startYear=1900 -endYear=2001 -smoothing=2
python getngrams.py internet --startYear=1980 --endYear=2000 --corpus=eng_2012 --caseInsensitive=on
```

### Flags ###
  * **corpus** [default: eng_2012] *This will run the query in CORPUS. Possible values are recapitulated below and [here](http://books.google.com/ngrams/info)*
  * **startYear** [default: 1800]
  * **endYear** [default: 2000]
  * **smoothing** [default: 3] *Smoothing parameter (integer). Minimum is 0.*
  * **caseInsensitive** [default: off] *Set to 'on' for case-insensitive queries*
  * **alldata** *Return every column of available data.**
  * **nosave** *Results will not be saved to file*
  * **noprint** *Results will not be printed on screen*
  * **help** *Prints this screen*
  * **quit** *Quits after running query*

\* This can be used with inflection, wildcard, and case-insensitive searches (otherwise it does nothing) where one column is the sum of some of the other columns (labeled with a column name ending in "(All)" or an asterisk for wildcard searches). In the [Google Ngram Viewer](http://books.google.com/ngrams), the columns whose sum makes up these column is viewable by right clicking on the ngram plot. In the `getngrams.py` script, these columns are dropped by default, but you can keep them by adding `-alldata` to your query.

### More Complicated Examples ###

##### Wildcard Searches #####

As in the full [Google Ngram Viewer](http://books.google.com/ngrams), you can also perform wildcard searches using `getngrams.py`.

When doing a wildcard search, use the `?` character instead of the `*` character. Using an asterisk will cause the `getngrams.py` script to fail because your shell will expand the asterisk before Python has a chance to see it.

```
python getngrams.py United ? --startYear=1800 --endYear=2000 -alldata
python getngrams.py University of ? -quit
python getngrams.py University of ?, # State University -alldata -quit
```

##### Modifier Searches #####

Modifier searches let you see how often one more modifies another word. The usual syntax for doing a modifier search is by using the `=>` operator. For example, running the query `dessert=>tasty` would match all instances of when the word *tasty* was used to modify the word *dessert*.

Modifier searches can be done using `getngrams.py`, but you must replace the `=>` operator with the `@` character.

```
python getngrams.py car@fast -startYear=1900 -endYear=2000 -quit
python getngrams.py car@fast -startYear=1900 -endYear=2000 -alldata -quit
python getngrams.py drink@?_NOUN -startYear=1900 -endYear=2000 -alldata -quit
```

For more information on wildcard and modifier searches, take a look at the [About Ngram Viewer](https://books.google.com/ngrams/info) page for more in depth documentation.

##### Other Examples #####

```
python getngrams.py book ? hotel, book_INF a hotel --startYear=1920 --endYear=2000 -alldata -quit
python getngrams.py read ?_DET book
python getngrams.py _DET_ bright_ADJ rainbow
python getngrams.py _START_ President ?_NOUN
python getngrams.py _ROOT_@will
```

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
pylab inline plotting backend (e.g. ipython --pylab inline). Then you can do
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
