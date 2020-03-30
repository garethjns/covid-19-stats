from datetime import date

import numpy as np
import pandas as pd

DAYS = 30
DATA = pd.DataFrame({'New cases': [3, 13, 12, 36, 29, 48, 45, 69, 43, 62, 77, 130, 208, 342, 251, 152,
                                        407, 676, 643, 714, 1035, 665, 967, 1427, 1452, 2129, 2885, 2546, 2433, 2619],
                          'Tests conducted': [np.nan for _ in range(DAYS)]},
                         index=[date(2020, 3, d) for d in range(1, DAYS + 1)])


class PositivityData:
    """
    UK testing data

    Sources and guesses:
      - 326 tests 3rd feb, 26k tests total 10th march,  30k tests total 12th march, from:
        https://en.wikipedia.org/wiki/2020_coronavirus_pandemic_in_the_United_Kingdom#Testing_and_surveillance
      - 10 March must be ~2k tests /day to get to 30k by 12
      - Assume for simplicity 0 tests per day 1st feb (was only ~300 3rd Feb, wikipedia again)

    Assuming:
      1) Linear increase in testing rate between 1st feb -> 1st March
      2) Linear increase from 1st March to 2k on March 12.

    What was testing value on March 1st (x)? Known total on 10th (26k) but need to ignore Feb tests from total.

    Total Feb tests depend on March 1st rate due to assumption 1:
    Tests in Feb (29 days) = (x - 0) * 29 / 2

    Therefore, tests between 1st - 10th March (10 days) = 10 * x + 10 * (2000 - x) / 2 = 26,000 - (x - 0) * 29 / 2
    10x + 10000 + 5x = 26000 - 14.5x
    19.5x = 16000
    x = 820

    New daily cases source: https://www.worldometers.info/coronavirus/country/uk/
    """

    days: int = DAYS

    def __init__(self, mar_1_estimate: int = 800,
                 mar_10_estimate: int = 2000,
                 mar_12_estimate: int = 2000,
                 mar_30_estimate: int = 8000) -> None:
        self._data: pd.DataFrame = DATA.copy()

        # Set key estimates
        self.mar_1_estimate = mar_1_estimate
        self.mar_10_estimate = mar_10_estimate
        self.mar_12_estimate = mar_12_estimate
        self.mar_30_estimate = mar_30_estimate

        self.estimate_and_infer_tests_per_day()
        self.calculate_positivity_rate()

    def calculate_positivity_rate(self):
        self._data.loc[:, 'Positivity rate'] = self._data['New cases'] / self._data['Tests conducted']

    def estimate_and_infer_tests_per_day(self) -> None:
        c = 'Tests conducted'
        self._data.loc[:, c] = np.nan
        self._data.loc[self.tests_per_day_estimates.index, c] = self.tests_per_day_estimates[c]
        self._data.loc[:, c] = self._data[c].reset_index(drop=True).interpolate(method='from_derivatives').values

    @property
    def tests_per_day_estimates(self) -> pd.DataFrame:
        return pd.DataFrame({'Tests conducted': [self.mar_1_estimate, self.mar_10_estimate, self.mar_12_estimate,
                                                 self.mar_30_estimate]},
                            index=[date(2020, 3, 1), date(2020, 3, 10), date(2020, 3, 12), date(2020, 3, 30)])

    @property
    def df(self) -> pd.DataFrame:
        return self._data.reset_index(drop=False).rename({'index': 'Date'},
                                                         axis=1)


if __name__ == "__main__":
    d = PositivityData(mar_30_estimate=10000)
