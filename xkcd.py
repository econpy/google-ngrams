import matplotlib.pyplot as plt
import matplotlib.font_manager as fm
from matplotlib import cm
from matplotlib.ticker import FuncFormatter
from matplotlib.backends.backend_agg import FigureCanvasAgg


def plotXKCD(ngramCSVfile):
    fin = open(ngramCSVfile, 'r')
    ngrams = fin.readline().strip().split(',')[1:]
    data_vals = [[] for ngram in ngrams]
    years = []
    for line in fin:
        sp = line.strip().split(',')
        years.append(int(sp[0]))
        for i, s in enumerate(sp[1:]):
            data_vals[i].append(float(s)*100)  # Make percentage
    fin.close()

    # Set up a figure
    plt.xkcd(scale=2, randomness=2.75)
    fig = plt.Figure()
    canvas = FigureCanvasAgg(fig)
    num_ngrams = len(ngrams)

    # Plot the data
    ax = fig.add_subplot(1, 1, 1)
    if len(data_vals) >= 1:
        for k, data, label in zip(list(range(num_ngrams)), data_vals, ngrams):
            if label.startswith('_'):  # The legend doesn't like labels that
                label = label[1:]      # start with an underscore.
            if k == 0:
                ax.plot(years, data, label=label,
                        color=cm.jet(1.*k/num_ngrams), lw=2)
            else:
                ax.plot(years, data, 'white', lw=6)
                ax.plot(years, data, label=label,
                        color=cm.jet(1.*k/num_ngrams), lw=2)

    # Create the Humor-Sans font properties object
    prop = fm.FontProperties(fname='Humor-Sans.ttf', size=17)

    # Define axes min/max/center
    xlim, ylim = ax.get_xlim(), ax.get_ylim()
    xmid = (xlim[1] - xlim[0])/2 + xlim[0]

    # Create the legend and change the font
    legend = ax.legend(loc='best', fontsize=9)
    for label in legend.get_texts():
        label.set_fontproperties(prop)

    # Don't show frame around legend
    legend.draw_frame(False)

    # Do not display top and right axes
    ax.spines["right"].set_visible(False)
    ax.spines["top"].set_visible(False)

    # Remove unneeded ticks
    ax.tick_params(axis='both', direction='out')
    ax.get_xaxis().tick_bottom()
    ax.get_yaxis().tick_left()

    # Set tick labels text
    prop.set_size(11)
    for label in ax.get_xticklabels():
        label.set_fontproperties(prop)
    for label in ax.get_yticklabels():
        label.set_fontproperties(prop)

    # Add percentage sign to y-axis ticks
    ax.yaxis.set_major_formatter(FuncFormatter(lambda y, pos=0: '%s%%' % y))

    # Set the ticks on each axes
    ax.set_xticks([xlim[0], xmid, xlim[1]])
    ax.set_yticks([ylim[1]])

    # Change tick thickness
    ax.xaxis.set_tick_params(width=1, length=4)
    ax.yaxis.set_tick_params(width=1, length=4)

    fig.savefig(ngramCSVfile.replace('.csv', '.png'), dpi=190)

if __name__ == '__main__':
    import sys
    plotXKCD(sys.argv[1])
