import pandas as pd
from lifelines import KaplanMeierFitter
from lifelines.datasets import load_waltons

from KaplanMeier import GetKaplanPoints
from HsctHelper import HsctHelper
from HsctRepository import HsctRepository

waltons = load_waltons()
kmf = KaplanMeierFitter(label="waltons_data")
kmf.fit(waltons['T'], waltons['E']) #durations, event_observed
a = 21

