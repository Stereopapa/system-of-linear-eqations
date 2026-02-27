from pathlib import Path

import matplotlib.pyplot as plt
from typing import Dict, List, Tuple
from matplotlib.figure import Figure
from matplotlib.axes import Axes
import numpy as np
from matplotlib.pyplot import title
from packaging import markers


class ExperimentVisualizer:
    save: bool
    show: bool
    output_dir: Path
    _fig: Figure
    _ax: Axes
    _axs: np.ndarray
    image_encoding: str
    _markers = ['o', 's', '^', 'D', 'v', 'x']

    def __init__(self, save: bool = False, show: bool = True, outdir: Path = Path("docs/charts"),
                 image_encoding: str = ".png"):
        self.save = save
        self.show = show
        self.output_dir = outdir
        self.image_encoding = image_encoding
        plt.style.use('ggplot')

    def plot_methods_comparison(self, experiments: Dict[str, Tuple[List[float], List[float]]],
            title: str = "None", x_label: str = "None", y_label: str = "None",
            filename: str = None, x_log: bool = False, y_log: bool = True):
        """
        experiments: Dict, key is the method name,
        and value is Tuple: (list_x, listy_y)
        """
        if not filename:
            filename = title.replace(" ", "_").lower() if title else "plot"

        self._fig, self._ax = plt.subplots(layout="constrained", figsize=(10, 6))


        for i, (label, data) in enumerate(experiments.items()):
            x_vals, y_vals = data
            label_name = label[0].upper() + label[1:]
            current_marker = self._markers[i%len(self._markers)]
            self._ax.plot(
                x_vals, y_vals, label=label_name, linewidth=2,
                marker=current_marker, markersize=6, markevery=1
            )

        if x_log:
            self._ax.set_xscale('log')
            x_label += " (log scale)"
        if y_log:
            self._ax.set_yscale('log')
            y_label += " (log scale)"

        self._ax.set_title(title, fontsize=14)
        self._ax.set_xlabel(x_label, fontsize=12)
        self._ax.set_ylabel(y_label, fontsize=12)
        self._ax.grid(True, which="both", ls="-", alpha=0.5)
        self._ax.legend()

        self._save_show_close_chart(filename)

    def _save_show_close_chart(self, filename: str):
        if self._fig is None:
            raise ValueError("No plot to be saved or showed, run any plot functions first")
        if self.save:
            self.output_dir.mkdir(parents=True, exist_ok=True)
            self._fig.savefig(self.output_dir / (filename + self.image_encoding))
        if self.show:
            plt.show()
        plt.close(self._fig)
        self._fig = None

