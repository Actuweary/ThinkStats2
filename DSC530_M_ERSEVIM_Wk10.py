"""This file contains code for use with "Think Stats",
by Allen B. Downey, available from greenteapress.com

Copyright 2014 Allen B. Downey
License: GNU GPLv3 http://www.gnu.org/licenses/gpl.html
"""

from __future__ import print_function, division

import numpy as np
import statsmodels.formula.api as smf
import thinkplot
import thinkstats2
import regression

def RunQuadraticModel(daily):
    """Runs a linear model of prices versus years.
    daily: DataFrame of daily prices
    returns: model, results
    """
    daily['years2'] = daily.years ** 2
    model = smf.ols('ppg ~ years + years2', data=daily)
    results = model.fit()
    return model, results


def PlotQuadraticModel(daily, name):
    """Plot and save results from Quadratic model.
    """
    model, results = RunQuadraticModel(daily)
    regression.SummarizeResults(results)
    timeseries.PlotFittedValues(model, results, label=name)
    thinkplot.Save(root='timeseries11',
                   title='fitted values',
                   xlabel='years',
                   xlim=[-0.1, 3.8],
                   ylabel='price per gram ($)')

    timeseries.PlotResidualPercentiles(model, results)
    thinkplot.Save(root='timeseries12',
                   title='residuals',
                   xlabel='years',
                   ylabel='price per gram ($)')

    years = np.linspace(0, 5, 101)
    thinkplot.Scatter(daily.years, daily.ppg, alpha=0.1, label=name)
    timeseries.PlotPredictions(daily, years, func=RunQuadraticModel)
    thinkplot.Save(root='timeseries13',
                   title='predictions',
                   xlabel='years',
                   xlim=[years[0] - 0.1, years[-1] + 0.1],
                   ylabel='price per gram ($)')


class SerialCorrelationTest(thinkstats2.HypothesisTest):
    """Tests serial correlations by permutation."""

    def TestStatistic(self, data):
        """Computes the test statistic.
        data: tuple of xs and ys
        """
        series, lag = data
        test_stat = abs(thinkstats2.SerialCorr(series, lag))
        return test_stat

    def RunModel(self):
        """Run the model of the null hypothesis.
        returns: simulated data
        """
        series, lag = self.data
        permutation = series.reindex(np.random.permutation(series.index))
        return permutation, lag


def TestSerialCorr(daily):
    """Tests serial correlations in daily prices and their residuals.
    daily: DataFrame of daily prices
    """
    # test the correlation between consecutive prices
    series = daily.ppg
    test = SerialCorrelationTest((series, 1))
    pvalue = test.PValue()
    print(test.actual, pvalue)

    # test for serial correlation in residuals of the linear model
    _, results = timeseries.RunLinearModel(daily)
    series = results.resid
    test = SerialCorrelationTest((series, 1))
    pvalue = test.PValue()
    print(test.actual, pvalue)

    # test for serial correlation in residuals of the quadratic model
    _, results = RunQuadraticModel(daily)
    series = results.resid
    test = SerialCorrelationTest((series, 1))
    pvalue = test.PValue()
    print(test.actual, pvalue)


def main(name):
    transactions = timeseries.ReadData()

    dailies = timeseries.GroupByQualityAndDay(transactions)
    name = 'high'
    daily = dailies[name]

    PlotQuadraticModel(daily, name)
    TestSerialCorr(daily)
    #PlotEwmaPredictions(daily, name)


if __name__ == '__main__':
    import sys

    main(*sys.argv)