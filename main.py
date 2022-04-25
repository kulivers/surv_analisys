from lifelines.statistics import logrank_test
import numpy as np
import pandas as pd
from lifelines import KaplanMeierFitter
from matplotlib import pyplot as plt
from scipy.spatial import KDTree
from webcolors import (
    CSS3_HEX_TO_NAMES,
    hex_to_rgb,
)

from HsctHelper import HsctHelper
from HsctRepository import HsctRepository
from UmdbHelper import UmdbHelper
from UmdbRepository import UmdbRepository

umdbRepo = UmdbRepository()
umdbHelper = UmdbHelper()
hsctRepo = HsctRepository()
hsctHelper = HsctHelper()


def getKaplanValuesByDiagnosysName(diagnosys_name):
    records = umdbRepo.getPatientsByDiagnosysName(diagnosys_name)
    live_durations_dead = umdbHelper.GetLiveDurationsOfDead(records)
    live_durations_censored = umdbHelper.GetLiveDurationsOfCensored(records)

    mydf = pd.DataFrame()
    mydf['Durs'] = live_durations_dead + live_durations_censored
    mydf['events'] = [1] * len(live_durations_dead) + [0] * len(live_durations_censored)

    kmf = KaplanMeierFitter(label="waltons_data")
    kmf.fit(mydf['Durs'], mydf['events'])
    surv = kmf.survival_function_.values
    timeline = kmf.timeline
    lower = kmf.confidence_interval_['waltons_data_lower_0.95']
    upper = kmf.confidence_interval_['waltons_data_upper_0.95']
    return [surv, timeline, lower, upper]


def getKaplanValuesByDiagnosysPath(path):
    records = umdbRepo.getPatientsByDiagnosysPath(path)
    live_durations_dead = umdbHelper.GetLiveDurationsOfDead(records)
    live_durations_censored = umdbHelper.GetLiveDurationsOfCensored(records)

    mydf = pd.DataFrame()
    mydf['Durs'] = live_durations_dead + live_durations_censored
    mydf['events'] = [1] * len(live_durations_dead) + [0] * len(live_durations_censored)

    kmf = KaplanMeierFitter(label="waltons_data")
    kmf.fit(mydf['Durs'], mydf['events'])
    surv = kmf.survival_function_.values
    timeline = kmf.timeline
    lower = kmf.confidence_interval_['waltons_data_lower_0.95']
    upper = kmf.confidence_interval_['waltons_data_upper_0.95']
    return [surv, timeline, lower, upper]


def getKaplanValues(records):
    live_durations_dead = umdbHelper.GetLiveDurationsOfDead(records)
    live_durations_censored = umdbHelper.GetLiveDurationsOfCensored(records)

    mydf = pd.DataFrame()
    mydf['Durs'] = live_durations_dead + live_durations_censored
    mydf['events'] = [1] * len(live_durations_dead) + [0] * len(live_durations_censored)

    kmf = KaplanMeierFitter(label="waltons_data")
    kmf.fit(mydf['Durs'], mydf['events'])
    surv = kmf.survival_function_.values
    timeline = kmf.timeline
    lower = kmf.confidence_interval_['waltons_data_lower_0.95']
    upper = kmf.confidence_interval_['waltons_data_upper_0.95']
    return [surv, timeline, lower, upper]


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


def pltDiagnosesByNames(names):
    survs = []
    for idx, d in enumerate(names):
        path = d['_id']
        name = umdbRepo.getDiagnosysName(path)
        [surv, timeline, lower, upper] = getKaplanValuesByDiagnosysName(name)
        survs.append(getKaplanValuesByDiagnosysName(name))
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



def getPatientsBySex(records, sex='m'):
    sex_arr = None
    if sex is not None:
        sex_arr = [sex]

    res = []
    for r in records:
        try:
            if r['patient_sex'] == sex_arr:
                res.append(r)
        except:
            continue
    return res


if __name__ == '__main__':
    common_paths = umdbRepo.getMostCommonDiagnosesPaths(False, 6)
    records = umdbRepo.getPatientsByDiagnosysPath(common_paths[0])
    males = getPatientsBySex(records, 'm')
    females = getPatientsBySex(records, 'f')
    noSex = getPatientsBySex(records, None)

    malesValues = getKaplanValues(males)
    femalesValues = getKaplanValues(females)
    # 0-surv, 1-timelines
    a=1
    plt.plot(malesValues[1], malesValues[0], drawstyle="steps-pre", color='b')
    plt.plot(femalesValues[1], femalesValues[0], drawstyle="steps-pre", color='r')
    log = logrank_test(malesValues[0], femalesValues[0])

    # p = plt.plot(timeline, surv, drawstyle="steps-pre")
    plt.ylabel('Вероятность')
    plt.yticks(np.arange(0, 1.01, 0.1))
    plt.xlabel('Дни')
    plt.title('SURV')
    plt.show()
