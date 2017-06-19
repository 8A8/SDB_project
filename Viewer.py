# -*- coding: utf8 -*-
from matplotlib import pyplot as plt
import shapely
from shapely.geometry.polygon import Polygon
from descartes import PolygonPatch


from matplotlib.widgets import Button, CheckButtons



# get monitor size.
from win32api import GetSystemMetrics

class Viewer:

    def __init__(self, types, SIZE=None):
        _dpi = 100
        if SIZE is None:
            w = (GetSystemMetrics(0) - 200) / _dpi
            h = (GetSystemMetrics(1) - 200) / _dpi
            SIZE = (w, h)
        self.fig = plt.figure(1, figsize=SIZE, dpi=_dpi)
        self.ax = self.fig.add_subplot(111)
        self.ax.set_facecolor((0.815, 0.925, 0.9, 1))

        self.patches = []
        self.cid = self.fig.canvas.mpl_connect('button_press_event', self.highlight_area)
        self.coords = []

        # geom object save
        self.object = {}
        self.color = {}
        for t in types:
            self.object[t] = []

        #self.object['type'] = []
        #self.object['draw'] = []
        #self.object['index'] =[]

        self.all_points = {}
        self.points = []
        self.lines = []
        self.polygons = []
        self.point_index = 0
        self.line_index = 0
        self.polygon_index = 0

        # temp
        self.scatters = {}
        self.point_list = []
        # temp too
        self.polygon_list = []
        self.line_list = []

        self.ax.set_title('toronto')

        # view range
        xrange = [-79.7034, -79.8187]
        yrange = [43.5635, 43.6200]
        self.ax.set_xlim(*xrange)
        self.ax.set_ylim(*yrange)
        self.ax.set_aspect(1)

        # button
        self.flag = 0
        axnext = plt.axes([0.81, 0.05, 0.1, 0.075])
        self.bnext = Button(axnext, 'highlight area')
        self.bnext.on_clicked(self.flag_setting)
        self.highlifgted = None
        #self.bprev = Button(axprev, 'Previous')
        #self.bprev.on_clicked(self.flag_setting)

        # check buttons
        axchk = plt.axes([0.7, 0.05, 0.1, 0.275])

        # ladel's list, active's list is all
        self.labels = types
        self.act = [0 for x in types]
        self.check = CheckButtons(axchk, labels=self.labels, actives=self.act)
        self.check.on_clicked(self.get_active)

    def insert_object(self, table_name, objects, _color):

        self.all_points[table_name] = []

        for o in objects:
            object = o['object']
            zorder = o['zorder']
            o['table'] = table_name
            o['color'] = _color

            self.object[table_name].append(o)
            self.color[table_name] = _color
            if isinstance(object, shapely.geometry.point.Point):
                self.points.append(o)
                self.all_points[table_name].append([object.x, object.y])
                o['index'] = len(self.all_points[table_name]) - 1
            elif isinstance(object, shapely.geometry.linestring.LineString):
                self.lines.append(o)
                # line plot
                x, y = object.xy
                self.ax.plot(x, y, color=_color, linewidth=1, solid_capstyle='round', zorder=-1 * zorder, gid=self.line_index)
                o['index'] = self.line_index
                self.line_index += 1
            elif isinstance(object, shapely.geometry.polygon.Polygon):
                self.polygons.append(o)
                poly_patch = PolygonPatch(object)
                poly_patch.set_fc(_color)
                poly_patch.set_zorder(zorder)  # * zorder[i])
                poly_patch.set_picker(self.polygon_index)
                self.ax.add_patch(poly_patch)
                o['index'] = self.polygon_index
                self.polygon_index += 1


        # point draw
        if len(self.all_points[table_name]) != 0:
            self.scatters[table_name] = self.ax.scatter(*zip(*self.all_points[table_name]),
                                            color=[_color] * len(self.all_points[table_name]),
                                            s=[5] * len(self.all_points[table_name]), picker=True, marker="*")

    def plot_object(self, objects, _color):
        """

        :param table_name:
        :param objects: shapely.geometry type instance and z order dict list objects[i]['object'], object[i]['zorder']
        :param _color: color = (R, G, B, A) dict
        :return:
        """

        for o in objects:
            object = o['object']
            zorder = o['zorder']
            idx =  o['index']
            table_name = o['table']
            o['color'] = _color
            if isinstance(object, shapely.geometry.point.Point):
                self.scatters[table_name]._facecolors[idx, :] = _color
                self.scatters[table_name]._edgecolors[idx, :] = _color

            elif isinstance(object, shapely.geometry.linestring.LineString):
                list = self.ax.get_lines()
                p = list[idx]
                self.lines.append(o)
                p.set_color(_color)


            elif isinstance(object, shapely.geometry.polygon.Polygon):
                list = self.ax.patches
                p = list[idx]
                p.set_fc(_color)

    def get_active(self, event):
        # self.object[event]가 선택된것
        idx = self.labels.index(event)
        if self.act[idx]:
            self.plot_object(self.object[event], (self.color[event]))
            self.act[idx] = 0
        else:
            self.plot_object(self.object[event], (1, 1, 0, 1))
            self.act[idx] = 1

        '''
        if event == self.labels[0]:
            if self.act[0]:
                for i, p in enumerate(self.point_list):
                    self.scatters._facecolors[i, :] = (0.99, 0.89, 0.925, 0.5)
                    self.scatters._edgecolors[i, :] = (0.99, 0.89, 0.925, 0.5)
                    self.act[0] = 0
            else:
                for i, p in enumerate(self.point_list):
                    self.scatters._facecolors[i, :] = (1, 1, 0, 1)
                    self.scatters._edgecolors[i, :] = (1, 1, 0, 1)
                    self.act[0] = 1
        elif event == self.labels[1]:
            if self.act[1]:
                for l in self.ax.get_lines():
                    l.set_color('GRAY')
                self.act[1] = 0
            else:
                for l in self.ax.get_lines():
                    l.set_color((0.968, 0.8627, 0.435, 1))
                self.act[1] = 1

        elif event == self.labels[2]:
            if self.act[2]:
                for p in self.ax.patches:
                    p.set_fc((0.84, 0.917, 0.97, 0.5))
                self.act[2] = 0
            else:
                for p in self.ax.patches:
                    p.set_fc((0.968, 0.8627, 0.435, 1))
                self.act[2] = 1
        print event
        '''

        self.fig.canvas.draw()

    def flag_setting(self, event):
        if self.highlifgted is not None:
            self.highlifgted.remove()
            for p in self.points:
                self.scatters[p['table']]._facecolors[p['index'], :] = p['color']
                self.scatters[p['table']]._edgecolors[p['index'], :] = p['color']
                self.act[0] = 0
            for l in self.ax.get_lines():
                idx = l.get_gid()
                if idx is None:
                    break;
                color = self.lines[idx]['color']
                l.set_color(color)

            for p in self.ax.patches:
                idx = p.get_picker()
                if idx is None:
                    break;
                color = self.polygons[idx]['color']
                p.set_fc(color)
        self.flag = 1

    def highlight_area(self, event):
        coords = self.coords
        if self.flag == 1:
            ix, iy = event.xdata, event.ydata
            # print 'x = %f, y = %f' % (ix, iy)
            coords.append((ix, iy))

        if len(coords) == 2 and self.flag == 1:
            rec = []
            x1, y1 = coords[0]
            x2, y2 = coords[1]
            rec.append(coords[0])
            rec.append((x1,y2))
            rec.append(coords[1])
            rec.append((x2, y1))

            self.flag = 0
            #plt.scatter(*zip(*coords), color=(17 / 255, 120 / 255, 100 / 255, 1), s=0.5)
            ring_patch = PolygonPatch(Polygon(rec))
            r = Polygon(rec)

            # if point
            for p in self.points:
                if r.contains(p['object']):
                    self.scatters[p['table']]._facecolors[p['index'], :] = (1, 1, 0, 1)
                    self.scatters[p['table']]._edgecolors[p['index'], :] = (1, 1, 0, 1)

            # if polygon
            for p in self.ax.patches:
                idx = p.get_picker()
                if idx is None:
                    break;
                if r.contains(self.polygons[idx]['object']):
                    p.set_fc((0.968, 0.8627, 0.435, 1))
                    #p.set_fc((0.424, 0.204, 0.514, 0.5))


            # if line
            for l in self.ax.get_lines():
                idx = l.get_gid()
                if idx is None:
                    break;
                line = self.lines[idx]['object']
                if r.contains(line):
                    l.set_color((0.968, 0.8627, 0.435, 1))

            ring_patch.set_fc((0.84, 0.917, 0.97, 0.5))
            ring_patch.set_zorder(99)
            self.highlifgted = ring_patch
            self.ax.add_patch(ring_patch)
            for p in coords:
                x, y = p[0], p[1]
                self.ax.plot(x, y, color='GRAY', linewidth=1, solid_capstyle='round')

            self.coords = []
            self.fig.canvas.draw()
            # fig.canvas.mpl_disconnect(cid)

        return coords

    def run(self):
        plt.show()

