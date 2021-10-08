import matplotlib as mpl
import matplotlib.pyplot as plt
from phys import *
pgf_with_latex = {                      # setup matplotlib to use latex for output
    "pgf.texsystem": "pdflatex",        # change this if using xetex or lautex
    "text.usetex": True,                # use LaTeX to write all text
    "font.family": "sans-serif",        # default fig size of 0.9 textwidth
    "pgf.preamble": "\n".join([         # plots will use this preamble
        r"\usepackage[utf8]{inputenc}",
        r"\usepackage[T1]{fontenc}",
        r"\usepackage[detect-all,locale=DE]{siunitx}", # Unity package (ax titles)
        r"\usepackage{physics}"         # Physics package we know and love
        ])
    }
mpl.use("pgf")
mpl.rcParams.update(pgf_with_latex)
title_font = {"fontname": "monospace", "fontsize": 16}
ax_font = {"fontsize": 12}


def linear(x, a, b):
    return a * x + b
linear = np.vectorize(linear)


class Lin_errgraph(plt.Axes):
    """
    Class to automatically create a graph where a linear
    regression has been made, with errorbar, with the error on the
    parameter of the regression.

    This class inherits from Axes, from pyplot, matplotlib
    """
    def __init__(self, x, y, dx, dy, label_fit = None,
        pt_fit = 100, *args, **kwargs):

        fig, ax = plt.subplots()
        super(Lin_errgraph, self).__init__(fig, [1, 1, 2, 6])
        self.x = x
        self.y = y
        self.dx = dx
        self.dy = dy
        ax.errorbar(x, y, dx, dy, *args, **kwargs)
        param = [1, 0]
        popt, pcov = op.curve_fit(linear, x, y, param, dy)
        self.a = popt[0]
        self.err = np.sqrt(np.diag(pcov))
        x = np.linspace(np.min(x), np.max(x), 100)
        y = linear(x, *popt)
        kwargs.pop("label")
        kwargs.pop("fmt")
        ax.plot(x, y, label=label_fit, *args, **kwargs)
        self.fig = fig
        self.ax = ax


class Excel_import_var():
    """
    From an excel file, load all columns as numpy table and variables.

    You can access the numpy tables from the class' attribute of the name
    of the first row of each column inside your excel file.
    """
    def __init__(self, file):
        self.file = file
        data = pd.read_excel(file)
        names = data.columns
        for var in names:
            string = "self." + var + f"=data['{var}'].dropna().to_numpy()"
            exec(string)

        
