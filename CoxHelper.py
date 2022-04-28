import datetime

import pandas as pd
# from lifelines import CoxPHFitter
from lifelines.fitters.coxph_fitter import CoxPHFitter

from UmdbHelper import UmdbHelper
from UmdbRepository import UmdbRepository

from lifelines.datasets import load_rossi


def examples():
    rossi = load_rossi()  # TODO test
    # cph.fit(rossi, 'week', 'arrest')

    df2 = pd.DataFrame({  # TODO test
        'T': [5, 3, 9, 8, 7, 4, 4, 3, 2, 5, 6, 7],
        'E': [1, 1, 1, 1, 1, 1, 0, 0, 1, 1, 1, 0],
        'var': [0, 0, 0, 0, 1, 1, 1, 1, 1, 2, 2, 2],
        'weights': [1.1, 0.5, 2.0, 1.6, 1.2, 4.3, 1.4, 4.5, 3.0, 3.2, 0.4, 6.2],
        'month': [10, 3, 9, 8, 7, 4, 4, 3, 2, 5, 6, 7],
        'age': [4, 3, 9, 8, 7, 4, 4, 3, 2, 5, 6, 7],
    })
    # cph.fit(df, duration_col='T', event_col='E', strata=['month', 'age'], robust=True, weights_col='weights')#TODO test

    df3 = pd.DataFrame({  # TODO test
        'T': [5, 3, 9, 8, 7, 4, 4, 3, 2, 5, 6, 7],
        'E': [1, 1, 1, 1, 1, 1, 0, 0, 1, 1, 1, 0],
        'var': [0, 0, 0, 0, 1, 1, 1, 1, 1, 2, 2, 2],
        'age': [4, 3, 9, 8, 7, 4, 4, 3, 2, 5, 6, 7],
    })
    cph.fit(df, 'T', 'E')
    cph.predict_median(df)


helper = UmdbHelper()
repo = UmdbRepository()

common_path = repo.getMostCommonDiagnosesPaths()[7]
records = repo.getPatientsByDiagnosysPath(common_path)

cph = CoxPHFitter()

status_duration_dict = helper.getStatusAndLiveDurationsOfPatients(records)
durations = []
statuses = []
for row in status_duration_dict:
    durations.append(row['duration'])
    statuses.append(row['status'])

# todo fix doesnt work
df, dictionary = helper.formatDf(records, boolFieldNames=['patient_sex', 'death'], simpleFieldsToReturn=['patient_sex', 'death'], removeArrayColumns=True)

df['durs'] = durations
df['status'] = statuses

df.dropna(axis=0, inplace=True)

cph.fit(df=df, duration_col='durs', event_col='status')

cph.print_summary()


