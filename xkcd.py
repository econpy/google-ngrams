import matplotlib.pyplot as plt
import matplotlib.font_manager as fm
from matplotlib import cm
from matplotlib.ticker import FuncFormatter
from matplotlib.backends.backend_agg import FigureCanvasAgg as fc


def addPercentSign(y_tick, pos=0):
    return '%s%%' % y_tick


def plotXKCD(ngramCSVfile):
    fin = open(ngramCSVfile, 'r')
    ngrams = fin.readline().strip().split(',')[1:]
    data_vals = [[] for ngram in ngrams]
    years = []
    for line in fin:
        sp = line.strip().split(',')
        years.append(int(sp[0]))
        for i, s in enumerate(sp[1:]):
            data_vals[i].append(float(s)*100) # Make percentage
    fin.close()

    # Set up a figure
    fig = plt.Figure()
    canvas = fc(fig)
    num_ngrams = len(ngrams)

    # Plot the data
    ax = fig.add_subplot(1, 1, 1)
    if len(data_vals) >= 1:
        for k, data, label in zip(range(num_ngrams), data_vals, ngrams):
            if k == 0:
                ax.plot(years, data, label=label,
                        color=cm.jet(1.*k/num_ngrams), lw=2)
            else:
                ax.plot(years, data, 'white', lw=6)
                ax.plot(years, data, label=label,
                        color=cm.jet(1.*k/num_ngrams), lw=2)

    # Create the Humor-Sans font properties object
    prop = fm.FontProperties(fname='Humor-Sans.ttf')

    # Create the legend
    legend = ax.legend()
    for label in legend.get_texts():
        label.set_fontproperties(prop)

    # Set axis labels and text
    ax.set_xlabel('Time', fontproperties=prop)
    ax.set_ylabel('Percentage of Texts', fontproperties=prop)

    # Setup subtitles
    file_str = ngramCSVfile.split('.')[0]
    file_parts = file_str.split('-')
    bottom_title = '%s - %s | ' % (file_parts[2], file_parts[3])
    if file_str.endswith('on'):
        bottom_title += 'Case Insensitive | '
    else:
        bottom_title += 'Case Sensitive | '
    bottom_title += 'Corpus: %s | ' % file_parts[1]
    bottom_title += 'Smoothing: %s' % file_parts[4]

    ax.set_title(bottom_title, fontproperties=prop,
                 fontdict={'verticalalignment': 'bottom', 'fontsize': 10,
                           'color': '#787878'})

    # Setup title
    if len(ngrams) == 1:
        fig.suptitle(ngrams[0], fontproperties=prop,
                     fontdict={'fontsize': 16, 'weight': 'heavy'})
    elif len(ngrams) == 2:
        title_queries = '%s and %s' % (ngrams[0], ngrams[1])
        fig.suptitle(title_queries, fontproperties=prop,
                     fontdict={'fontsize': 15, 'weight': 'heavy'})
    elif len(ngrams) >= 3:
        title_queries = ', '.join(ngrams[:-1]) + ', and %s' % ngrams[-1]
        fig.suptitle(title_queries, fontproperties=prop,
                     fontdict={'fontsize': 14, 'weight': 'heavy'})
    else:
        fig.suptitle('Google Ngrams', fontproperties=prop,
                     fontdict={'fontsize': 14, 'weight': 'heavy'})

    # Set tick labels text
    for label in ax.get_xticklabels():
        label.set_fontproperties(prop)
    for label in ax.get_yticklabels():
        label.set_fontproperties(prop)

    # Add percentage sign to y-axis ticks
    ax.yaxis.set_major_formatter(FuncFormatter(addPercentSign))

    ax.axison = True

    fig.savefig('%s.png' % file_str, dpi=250)

if __name__ == '__main__':
    import sys
    plotXKCD(sys.argv[1])
