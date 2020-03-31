# covid-19-stats

This repo contains data collected from various sources to create a create graphs focused on testing rate.

Knowing the number of tests conducted is essential context for interpreting the absolute number of positive cases typically presented in the media. For example, have China stopped their epidemic, or did they just stop testing?

It's very difficult to get hold of data on the number of tests conducted, and it's very likely that in the vast majority of countries, far more people are infected than the positive cases imply. 

See also [garethjns/social-distancing-sim](https://github.com/garethjns/social-distancing-sim) for a graph-based disease spread model.

# Positivity rate rate: Positive cases vs rate of testing (March 2020)

![positivity rate](https://github.com/garethjns/covid-19-stats/blob/master/images/positivity_plot_2.png) 

I thought this would be a fairly simple plot, but while trying to collect testing data numbers for the UK I've ended up with 4 data points for March, 2 of which are estimates. If anyone has better data, please let me know.

At the time of plotting this, the UK has shown a decline in the number of new cases for the past 3 days. Is this significant? Is it chance? Or has the rate of testing changed?

This plot shows the positivity rate - the number of cases detected per number of tests done. It makes the following data and assumptions, and plots a couple of outcomes based on variation of the estimated number of tests.

Data:
  - https://en.wikipedia.org/wiki/2020_coronavirus_pandemic_in_the_United_Kingdom#Testing_and_surveillance
    - 326 in total had been conducted by tests 3rd Feb
    - 26k tests total by 10th March
    - 30k tests total 12th march
  - https://www.worldometers.info/coronavirus/country/uk/
    - Cases per day (blue line on top panel)

Assuming:
  1) 10 March must be ~2k tests /day to get to 30k by 12
  2) Linear increase in testing rate between 1st Feb -> 1st March
  3) Linear increase from 1st March to 2k on March 12.

Model:
  - Simple piecewise interpolation of known and estimated number of tests per day.

Estimated data points:
  - 0 Tests per day start of Feb - for simplicity, and it's close enough
  - x tests per day as of March 1st (x):
    - Total tests done in Feb (29 days) depend on this point: (x - 0) * 29 / 2
    - Total tests done in March depend on this point: 10 * x + 10 * (2000 - x) / 2
    - We know that by March 10, 26,000 tests have been done in total. So March 1 tests per day is calculated using this value MINUS the tests already done in Feb:  
     Test done between March 1-10 (10 days) = 10 * x + 10 * (2000 - x) / 2 = 26,000 - (x - 0) * 29 / 2  
        10x + 10000 + 5x = 26000 - 14.5x  
        19.5x = 16000  
        x = 820  
  - The number of tests being conducted per day as of March 30. No idea. The government was aiming for 20,000 per day apparently. This final point value is varied in the graph.
  