import pandas as pd
from lifelines import KaplanMeierFitter
from lifelines.datasets import load_waltons

from KaplanMeier import GetKaplanPoints
from PatientsHelper import PatientsHelper
from Hsct_repository import Hsct_repository

waltons = load_waltons()
kmf = KaplanMeierFitter(label="waltons_data")
kmf.fit(waltons['T'], waltons['E']) #durations, event_observed
a = 21

