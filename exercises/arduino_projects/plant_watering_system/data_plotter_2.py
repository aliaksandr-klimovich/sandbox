import time
from datetime import timedelta

import plotly.graph_objs as go
import plotly.plotly as ipy
import plotly.offline as py
from data_saver import DB
from logger import get_logger
from plotly.exceptions import PlotlyRequestError

RUN_TYPE = 'CONTINUOUS'  # CONTINUOUS, SINGLE
PLOT_TYPE = 'ONLINE'  # ONLINE, OFFLINE
ROLL_BACK_TIME = timedelta(hours=12)
PLOT_COLOR = 'MONOCHROME'  # MULTICOLOR, MONOCHROME

log = get_logger(__name__)


def main():
    db = DB()
    data = db.get_data(ROLL_BACK_TIME)
    db.disconnect()

    # from datetime import datetime
    # data = [
    #     (datetime.now() + timedelta(seconds=1), 300),
    #     (datetime.now() + timedelta(seconds=2), 500),
    #     (datetime.now() + timedelta(seconds=3), 800),
    #     (datetime.now() + timedelta(seconds=4), 1200),
    #     (datetime.now() + timedelta(seconds=5), 1600),
    # ]

    title = 'CO₂ concentration over time'

    if PLOT_COLOR == 'MULTICOLOR':
        data = [
            filter(lambda i: i[1] < 400, data),
            filter(lambda i: 400 <= i[1] <= 600, data),
            filter(lambda i: 600 <= i[1] <= 1000, data),
            filter(lambda i: 1000 <= i[1] <= 1400, data),
            filter(lambda i: i[1] > 1400, data),
        ]
        color = [
            '#009933',
            '#669900',
            '#cccc00',
            '#ff9900',
            '#cc3300',
        ]
        trace_title = [
            '< 400',
            '400 — 600',
            '600 — 1000',
            '1000 — 1400',
            '> 1400',
        ]

        def make_trace(x, y, color, title):
            return {
                'x': [i.isoformat(timespec='seconds') for i in x],
                'y': y,
                'type': 'scatter',
                'mode': 'markers',
                'marker': {'color': color, 'size': 5},
                'name': title,
                'hoverinfo': 'none',
            }

        traces = []
        for d, c, t in zip(data, color, trace_title):
            d = list(d)
            if d:
                x, y = zip(*d)
            else:
                continue
            traces.append(make_trace(x, y, c, t))

    elif PLOT_COLOR == 'MONOCHROME':
        def make_trace(x, y, color, title):
            return {
                'x': [i.isoformat(timespec='seconds') for i in x],
                'y': y,
                'type': 'scatter',
                'mode': 'markers',
                'marker': {'color': color, 'size': 3},
                'name': title,
            }

        x, y = zip(*data)
        traces = [make_trace(x, y, 'blue', '')]

    else:
        raise ValueError('invalid PLOT_COLOR')

    layout = {
        'title': title,
        'xaxis': {'title': 'time', },
        'yaxis': {'title': 'ppm', },
        'showlegend': True if PLOT_COLOR == 'MULTICOLOR' else False,
        'hovermode': 'closest',
        'annotations': [
            {
                'text': 'The quality of the air in the room*:<br>'
                        ' High — less than 400 ppm<br>'
                        ' Medium — 400-600 ppm<br>'
                        ' Acceptable — 600-1000 ppm<br>'
                        ' Low — more than 1000 ppm<br>'
                        '*GOST 30494-2011',
                'align': 'left',
                'x': 0.02,
                'y': 0.98,
                'showarrow': False,
                'borderpad': 4,
                'borderwidth': 1,
                'bordercolor': 'black',
                'xref': 'paper',
                'yref': 'paper',
                'bgcolor': 'white',
                'font': {'family': 'Courier New, monospace'},
            },
        ]
    }

    fig = go.Figure(data=traces, layout=layout)
    if PLOT_TYPE == 'ONLINE':
        try:
            ipy.plot(fig, filename='CO2_OFFICE__1_DAY', fileopt='overwrite', auto_open=False)
        except PlotlyRequestError:
            pass
    elif PLOT_TYPE == 'OFFLINE':
        py.plot(fig, filename='CO2_OFFICE__1_DAY.html', auto_open=False)
    else:
        raise ValueError('invalid PLOT_TYPE')


if __name__ == '__main__':
    if RUN_TYPE == 'SINGLE':
        main()
    elif RUN_TYPE == 'CONTINUOUS':
        while 1:
            main()
            time.sleep(60 * 15)
    else:
        raise ValueError('invalid RUN_TYPE')
