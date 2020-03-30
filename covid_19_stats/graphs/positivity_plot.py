from typing import Union

import matplotlib.pyplot as plt
import seaborn as sns

from covid_19_stats.data.positivity_data import PositivityData


class PositivityPlot:
    data_source: PositivityData = PositivityData

    def __init__(self,
                 data_to_plot: Union[None, PositivityData] = None):
        if data_to_plot is None:
            data_to_plot = [self.data_source(mar_30_estimate=4000), self.data_source(mar_30_estimate=8000),
                            self.data_source(mar_30_estimate=12000)]
        self.data_to_plot = data_to_plot

    def plot(self,
             show: bool = True,
             log: bool = False) -> plt.Figure:

        sns.set('paper')
        sns.set(font_scale=1.5)
        fig, axs = plt.subplots(nrows=2,
                                ncols=1,
                                figsize=(12, 8))

        axs[0].plot(self.data_to_plot[0].df['Date'],
                    self.data_to_plot[0].df['New cases'],
                    label='New cases /day',
                    linewidth=3)
        axs[0].set_title('Estimated positivity rate for COVID-19 in UK',
                         fontweight='bold')
        for di, d in enumerate(self.data_to_plot):

            if di == int(len(self.data_to_plot) / 2):
                # Is median
                axs[0].plot(d.df['Date'],
                            d.df['Tests conducted'],
                            label=f'Est. tests conducted /day ± variation of March 30th est.', color='k',
                            linewidth=3)
                axs[1].plot(d.df['Date'],
                            d.df['Positivity rate'],
                            label='Est. Positivity rate ± Mar 30 error', color='r',
                            linewidth=3)
            else:
                axs[0].plot(d.df['Date'],
                            d.df['Tests conducted'],
                            linestyle='--', color='k')
                axs[1].plot(d.df['Date'],
                            d.df['Positivity rate'],
                            linestyle='--', color='r')

        axs[0].set_ylabel('Count',
                          fontweight='bold')
        axs[0].get_xaxis().set_visible(False)
        axs[0].legend()
        axs[1].set_ylabel('Positive cases per test',
                          fontweight='bold')
        plt.xticks(rotation=45)
        axs[1].legend()

        if log:
            for ax in axs:
                ax.set(yscale="log")

        if show:
            plt.show()

        return fig


if __name__ == "__main__":
    pp = PositivityPlot()
    pp.plot()
