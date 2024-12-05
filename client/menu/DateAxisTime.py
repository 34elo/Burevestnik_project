from datetime import datetime
import pyqtgraph as pg


class DateAxisItem(pg.AxisItem):
    def tickStrings(self, values, scale, spacing):
        return [datetime.fromtimestamp(value).strftime('%Y-%m-%d') for value in values]
