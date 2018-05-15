import pandas as pd
import matplotlib.pyplot as plt
import numpy as np


class _pyjoyplotter():

    def __init__(self, data=None, x=None, y=None, hue=None, kind=None,
                       offset=0.75, cmap='Dark2', smooth=1, order=None,
                       bins=None, weights=None, figsize=None):
        ' initialise class, check args'

        assert (kind == 'line') or (kind == 'hist')
        assert type(data) == pd.core.frame.DataFrame
        assert (x in data) and (hue in data), \
                'x and hue must be columns in dataframe'
        if kind == 'line': assert (y in data), \
                'y must be column in dataframe for line plot'

        self.data = data
        self.x = x
        self.y = y
        self.hue = hue
        self.categories = list(set(data[hue])) if order == None else order
        self.n = len(self.categories)
        self.offset = offset
        self.colours = self._get_colours(cmap)
        self.n_c = len(self.colours)
        self.smooth = smooth
        self.kind = kind
        self.bins = bins
        self.weights = weights
        self.figsize = figsize


    def _get_colours(self, cmap):

        if isinstance(cmap, str):
            assert cmap in [
            m for m in plt.cm.datad if not m.endswith("_r")]
            cm = plt.get_cmap(cmap)

            return [cm(i) for i in range(cm.N)]

        if isinstance(cmap, list):
            assert len(cmap) == self.n
            return list(reversed(cmap))

    def _line_plot(self):

        fig = plt.figure(figsize=self.figsize)
        ax = plt.axes(frameon=False)

        self.data = self.data.sort_values(by=self.x)

        for i, c in enumerate(self.categories):

            i = self.n - (i + 1)
            df = self.data[
                self.data[self.hue] == c
                ].rolling(self.smooth).mean()

            x_d = df.loc[df[self.hue] == c, self.x].values
            y_d = df.loc[df[self.hue] == c, self.y].values
            y_d = (y_d - np.nanmin(y_d)
                )/(np.nanmax(y_d) - np.nanmin(y_d))

            y_d += i * self.offset
            y_min = np.tile(np.nanmin(y_d), (len(y_d)))

            col = self.colours[i % self.n_c]

            plt.plot(x_d, y_d,
                    color=col,
                    label=c,
                    alpha=0.8)

            plt.fill_between(x_d, y_d, y_min,
                    alpha=0.6,
                    color=col)

        x_min = self.data[self.x].min()
        x_max = self.data[self.x].max()
        plt.xlim(x_min, x_max)
        plt.xlabel(self.x)
        ax.set_yticks([self.offset*i for i in range(self.n)[::-1]])
        ax.set_yticklabels(self.categories)

        return ax


    def _hist_plot(self):

        fig = plt.figure(figsize=self.figsize)
        ax = plt.axes(frameon=False)

        if not isinstance(self.bins, list):
            self.bins = self.n * [self.bins]
        else:
            self.bins = list(reversed(self.bins))

        if self.weights is None:
            self.weights = self.n * [self.weights]

        for i, c in enumerate(self.categories):

            i = self.n - (i + 1)
            df = self.data[
                self.data[self.hue] == c]

            x_d = df.loc[df[self.hue] == c, self.x].values
            x_d = x_d[~np.isnan(x_d.astype("float"))]

            col = self.colours[i % self.n_c]
            if self.weights[i]:
                hist = np.histogram(x_d, bins=self.bins[i], weights=self.weights[i])
            else:
                hist = np.histogram(x_d, bins=self.bins[i])

            new_hist = (hist[0] / np.nanmax(hist[0]),
                    hist[1])

            width = (new_hist[1] - np.roll(new_hist[1], 1))[1:]
            bot = i * self.offset
            left = new_hist[1][:-1]
            height = new_hist[0]

            plt.bar(left, height, color=col,
                    width=width, bottom=bot, alpha=0.8, align='edge')

        plt.xlabel(self.x)
        ax.set_yticks([self.offset*i for i in range(self.n)[::-1]])
        ax.set_yticklabels(self.categories)

        return ax


    def _plot(self):

        if self.kind == 'line':
            return self._line_plot()

        else:
            return self._hist_plot()


def plot(data=None, x=None, y=None, hue=None, kind='line',
         offset=0.75, cmap='Dark2', smooth=1, order=None,
         bins=10, weights=None, figsize=None):
    '''
    Create 'Joy Plot':
        data (pd.DataFrame): DataFrame holding all data
        x (str)  : DataFrame column to use as x value
        y (str)  : DataFrame column to use as y values
        hue (str): DataFrame column to use to group data
        kind (str): specify plot type; line or hist
        offset (int/float): vertical seperation between plots
        cmap (str/list): name of matplotlib cmap, or list
                         of colors to be used for plots
        smooth (int): smoothing window, if smoothing to be applied
        order (list): order of categories - top to bottom
        bins (int/list): bins if using hist. int for all hists to have same
                         bins else list of bin no. for each hist.
                         If list, entries are specified from top to bottom
        weights (list): weights for (each hue) can be None
                        or a list of weights specified from top to bottom
    '''


    plotter = _pyjoyplotter(data=data, x=x, y=y, hue=hue,
            offset=offset, cmap=cmap, smooth=smooth, kind=kind,
            order=order, bins=bins, weights=weights, figsize=figsize)
    return plotter._plot()

