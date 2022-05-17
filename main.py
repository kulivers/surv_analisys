from lifelines.statistics import logrank_test
import numpy as np
import pandas as pd
from lifelines import KaplanMeierFitter
from lifelines import CoxPHFitter
from matplotlib import pyplot as plt
from scipy.spatial import KDTree
from webcolors import (
    CSS3_HEX_TO_NAMES,
    hex_to_rgb,
)

from CoxHelper import getTestCoxFit
from HsctHelper import HsctHelper
from HsctRepository import HsctRepository
from KMHelper import plotKaplanValues, plotMultipleKaplanValues
from UmdbHelper import UmdbHelper
from UmdbRepository import UmdbRepository

umdbRepo = UmdbRepository()
umdbHelper = UmdbHelper()
hsctRepo = HsctRepository()
hsctHelper = HsctHelper()


def hex_to_rgb(value):
    value = value.lstrip('#')
    lv = len(value)
    return tuple(int(value[i:i + lv // 3], 16) for i in range(0, lv, lv // 3))


def convert_rgb_to_names(rgb_tuple):
    # a dictionary of all the hex and their respective names in css3
    css3_db = CSS3_HEX_TO_NAMES
    names = []
    rgb_values = []
    for color_hex, color_name in css3_db.items():
        names.append(color_name)
        rgb_values.append(hex_to_rgb(color_hex))

    kdt_db = KDTree(rgb_values)
    distance, index = kdt_db.query(rgb_tuple)
    return f'{names[index]}'


def pltKMDiagnosesByNames(names):
    survs = []
    for idx, d in enumerate(names):
        path = d['_id']
        name = umdbRepo.getDiagnosysName(path)
        [surv, timeline, lower, upper] = umdbHelper.getKaplanValuesByDiagnosysName(name)
        survs.append(umdbHelper.getKaplanValuesByDiagnosysName(name))
        p, = plt.plot(timeline, surv, drawstyle="steps-pre")
        rgb = hex_to_rgb(p.get_color())
        color = convert_rgb_to_names(rgb)
        print(idx, ': ', name, ' - ', color)
    plt.ylabel('Вероятность')
    plt.yticks(np.arange(0, 1.01, 0.1))
    plt.xlabel('Дни')
    plt.title('SURV')
    plt.show()
    return survs


if __name__ == '__main__':
    # getTestCoxFit(toPrint=True)

    common_paths = umdbRepo.getMostCommonDiagnosesPaths(False, 6)
    records = umdbRepo.getPatientsByDiagnosysPath(common_paths[0])
    males = umdbHelper.getPatientsBySex(records, 'm')
    females = umdbHelper.getPatientsBySex(records, 'f')
    noSex = umdbHelper.getPatientsBySex(records, None)
    getTestCoxFit()  # goHERE

    # plotKaplanValues(males, 'males')
    # plotKaplanValues(females, 'females')
    # plotMultipleKaplanValues([males, females], ['males','females'])

    here_stop = 1
    # malesValues = umdbHelper.getKaplanValues(males)
    # femalesValues = umdbHelper.getKaplanValues(females)
    # log = logrank_test(malesValues[0], femalesValues[0], event_observed_A=malesValues[1], event_observed_B=femalesValues[1])
    # # Менее (5% = 0,05) значение P означает, что существует значительная разница между группами, которые мы сравнивали
    #
    # withDiagnosysNSex = umdbHelper.formatDf(records=records, boolFieldNames=['diagnosis', 'patient_sex'],
    #                                         valuesToBeEqual=[['1', '0', '1', '0'], ['m']],
    #                                         fieldsToReturn=['patient_sex', 'diagnosis', 'diagnosis_date'])
    #
    # plt.plot(malesValues[1], malesValues[0], drawstyle="steps-pre", color='b')
    # plt.plot(femalesValues[1], femalesValues[0], drawstyle="steps-pre", color='r')
    # plt.ylabel('Вероятность')
    # plt.yticks(np.arange(0, 1.01, 0.1))
    # plt.xlabel('Дни')
    # plt.title('SURV')
    # plt.show()
