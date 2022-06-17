# -*- coding: utf-8 -*-
"""Tests the VAR model."""
__author__ = ["thayeylolu", "AurumnPegasus"]
import numpy as np
import pandas as pd
from numpy.testing import assert_allclose
from statsmodels.tsa.api import VECM as _VECM

from sktime.forecasting.base import ForecastingHorizon
from sktime.forecasting.model_selection import temporal_train_test_split

#
from sktime.forecasting.vecm import VECM

index = pd.date_range(start="2005", end="2006-12", freq="M")
df = pd.DataFrame(
    np.random.randint(0, 100, size=(23, 2)),
    columns=list("AB"),
    index=pd.PeriodIndex(index),
)


def test_VAR_against_statsmodels():
    """Compares Sktime's and Statsmodel's VECM."""
    train, test = temporal_train_test_split(df)
    sktime_model = VECM()
    fh = ForecastingHorizon([1, 3, 4, 5, 7, 9])
    sktime_model.fit(train, fh=fh)
    y_pred = sktime_model.predict(fh=fh)

    stats = _VECM(train)
    stats_fit = stats.fit()
    fh_int = fh.to_relative(train.index[-1])
    # lagged = stats_fit.k_ar
    y_pred_stats = stats_fit.predict(steps=fh_int[-1])
    new_arr = []
    for i in fh_int:
        new_arr.append(y_pred_stats[i - 1])
    assert_allclose(y_pred, new_arr)
