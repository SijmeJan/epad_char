import numpy as np
import matplotlib.pyplot as plt

class ScatterPlot():
    def __init__(self, fig, ax, x, y, names):
        self.fig = fig
        self.ax = ax

        self.x = x
        self.y = y
        self.names = names

        self.sc = self.ax.scatter(x, y)

        self.annot = self.ax.annotate("", xy=(0,0), xytext=(20,20),
                                      textcoords="offset points",
                                      bbox=dict(boxstyle="round", fc="w"),
                                      arrowprops=dict(arrowstyle="->"))
        self.annot.set_visible(False)

        self.fig.canvas.mpl_connect("motion_notify_event", self.hover)

    def update_annot(self, ind):
        pos = self.sc.get_offsets()[ind["ind"][0]]
        self.annot.xy = pos
        text = "{}, {}".format(" ".join(list(map(str,ind["ind"]))),
                               " ".join([self.names[n] for n in ind["ind"]]))
        self.annot.set_text(text)
        #self.annot.get_bbox_patch().set_facecolor(cmap(norm(c[ind["ind"][0]])))
        self.annot.get_bbox_patch().set_alpha(0.4)

    def hover(self, event):
        vis = self.annot.get_visible()
        if event.inaxes == self.ax:
            cont, ind = self.sc.contains(event)
            if cont:
                self.update_annot(ind)
                self.annot.set_visible(True)
                self.fig.canvas.draw_idle()
            else:
                if vis:
                    self.annot.set_visible(False)
                    self.fig.canvas.draw_idle()

def read_oec(oec, str1, str2):
    x = []
    y = []
    names = []

    for planet in oec.findall(".//planet"):
        if (planet.findtext(str1) is not None and
            planet.findtext(str2) is not None and
            planet.findtext(str1) != '' and
            planet.findtext(str2) != ''):

            x.append(float(planet.findtext(str1)))
            y.append(float(planet.findtext(str2)))
            names.append(planet.findtext("name"))

    return x, y, names
