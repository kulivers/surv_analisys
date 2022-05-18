import numpy as np
import pandas as pd
from lifelines import CoxPHFitter
from matplotlib import pyplot as plt

from KMHelper import plotKaplanValues, plotMultipleKaplanValues, getKaplanValues
from UmdbDataShaper import UmdbDataShaper
from UmdbRepository import UmdbRepository

umdbRepo = UmdbRepository()
umdbHelper = UmdbDataShaper()


def base_example_cox_fit():
    cph = CoxPHFitter()
    # rossi = load_rossi()
    # cph.fit(df=rossi, duration_col='week', event_col='arrest')
    # cph.print_summary()
    helper = UmdbDataShaper()
    repo = UmdbRepository()

    common_path = repo.getMostCommonDiagnosesPaths()[0]
    records = repo.getPatientsByDiagnosysPath(common_path)

    df, dictionary = helper.formatDf(records, boolFieldNames=['patient_sex', 'hsct_donor_type_common'],
                                     simpleFieldsToReturn=['patient_sex'], removeArrayColumns=True)

    df2 = pd.DataFrame({
        'T': [5, 3, 9, 8, 7, 4, 4, 3, 2, 5, 6, 7],
        'E': [1, 1, 1, 1, 1, 1, 0, 0, 1, 1, 1, 0],
        'var': [0, 0, 0, 0, 1, 1, 1, 1, 1, 2, 2, 2],
        'weights': [1.0, 0.5, 2.0, 1.6, 1.2, 4.3, 1.4, 4.5, 3.0, 3.2, 0.4, 6.2],
        'month': [10, 3, 9, 8, 7, 4, 4, 3, 2, 5, 6, 7],
        'age': [4, 3, 9, 8, 7, 4, 4, 3, 2, 5, 6, 7],
    })
    cph.fit(df2, duration_col='T', event_col='E', strata=['month', 'age'], robust=True, weights_col='weights')
    cph.print_summary()

    df2 = pd.DataFrame({
        'T': [5, 3, 9, 8, 7, 4, 4, 3, 2, 5, 6, 7],
        'E': [1, 1, 1, 1, 1, 1, 0, 0, 1, 1, 1, 0],
        'var': [0, 0, 0, 0, 1, 1, 1, 1, 1, 2, 2, 2],
        'weights': [2.0, 0.5, 2.0, 1.6, 1.2, 4.3, 1.4, 4.5, 3.0, 3.2, 0.4, 6.2],
        'month': [10, 3, 9, 8, 7, 4, 4, 3, 2, 5, 6, 7],
        'age': [4, 3, 9, 8, 7, 4, 4, 3, 2, 5, 6, 7],
    })
    cph.fit(df2, duration_col='T', event_col='E', strata=['month', 'age'], robust=True, weights_col='weights')
    cph.print_summary()

    df3 = pd.DataFrame({
        'T': [5, 3, 9, 8, 7, 4, 4, 3, 2, 5, 6, 7],
        'E': [1, 1, 1, 1, 1, 1, 0, 0, 1, 1, 1, 0],
        'var': [0, 0, 0, 0, 1, 1, 1, 1, 1, 2, 2, 2],
        'age': [4, 3, 9, 8, 7, 4, 4, 3, 2, 5, 6, 7],
    })
    cph.fit(df, duration_col='T', event_col='E')
    cph.print_summary()
    cph.predict_median(df)


def getTestKaplanPlotsNLogRank():
    common_paths = umdbRepo.getMostCommonDiagnosesPaths(False, 6)
    records = umdbRepo.getPatientsByDiagnosysPath(common_paths[4])
    males = umdbHelper.getPatientsBySex(records, 'm')
    females = umdbHelper.getPatientsBySex(records, 'f')

    plotKaplanValues(males, 'males')
    plotKaplanValues(females, 'females')
    plotMultipleKaplanValues([males, females], ['males', 'females'])

    malesValues = getKaplanValues(males)
    femalesValues = getKaplanValues(females)
    # log = logrank_test(malesValues[0], femalesValues[0], event_observed_A=malesValues[1], event_observed_B=femalesValues[1])
    # # Менее (5% = 0,05) значение P означает, что существует значительная разница между группами, которые мы сравнивали
    #
    # withDiagnosysNSex = umdbHelper.formatDf(records=records, boolFieldNames=['diagnosis', 'patient_sex'],
    #                                         valuesToBeEqual=[['1', '0', '1', '0'], ['m']],
    #                                         fieldsToReturn=['patient_sex', 'diagnosis', 'diagnosis_date'])
    #
    plt.plot(malesValues[1], malesValues[0], drawstyle="steps-pre", color='b')
    plt.plot(femalesValues[1], femalesValues[0], drawstyle="steps-pre", color='r')
    plt.ylabel('Вероятность')
    plt.yticks(np.arange(0, 1.01, 0.1))
    plt.xlabel('Дни')
    plt.title('SURV')
    plt.show()


def getTestCoxFit():
    helper = UmdbDataShaper()
    repo = UmdbRepository()

    common_path = repo.getMostCommonDiagnosesPaths()[0]
    records = repo.getPatientsByDiagnosysPath(common_path)
    conditioning_els_df, doses = helper.getConditioningElementsForPatients(records, returnDf=True)
    cph = CoxPHFitter()
    status_duration_dict = helper.getStatusAndLiveDurationsOfPatients(records)
    durations = []
    statuses = []
    for row in status_duration_dict:
        durations.append(row['duration'])
        statuses.append(row['status'])
    df, dictionary = helper.formatDf(records, boolFieldNames=['patient_sex', 'hsct_donor_type_common'],
                                     simpleFieldsToReturn=['patient_sex'], removeArrayColumns=True)
    df['durs'] = durations
    df['status'] = statuses
    for cond_el in list(conditioning_els_df.columns)[0:2]:
        df[cond_el] = conditioning_els_df[cond_el]
    df.dropna(axis=0, inplace=True)
    cph.fit(df=df, duration_col='durs', event_col='status')
    cph.print_summary()
