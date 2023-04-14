from io import BytesIO
import base64

from GMB.util import DEFAULTS
from GMB.builder import build


def getImageURL(commands):
    try:
        args = DEFAULTS
        args['lines'] = commands
        args['n_models'] = 1
        args['plot_freq'] = -1
        args['losses_freq'] = -1
        args['loss_freq'] = -1
        args['unnamed_objects'] = True

        figs = build(args, show_plot=False, encode_fig=True)
        urls = list()

        for fig in figs:
            img = BytesIO()
            fig.savefig(img, format='png')
            fig.close()
            img.seek(0)
            plot_url = base64.b64encode(img.getvalue()).decode()
            urls.append(f"data:image/png;base64,{plot_url}")

        return urls[0]
    except Exception as e:
        return "http://memegen.link/custom/Can't generate diagram/.jpg?alt=https://i.imgur.com/CsCgN7Ll.png&width=400"
