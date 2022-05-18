import numpy as np
import pandas as pd
from lifelines import KaplanMeierFitter
from matplotlib import pyplot as plt
from scipy.spatial import KDTree
from webcolors import (
    CSS3_HEX_TO_NAMES,
)

from UmdbDataShaper import UmdbDataShaper
from UmdbRepository import UmdbRepository

umdbHelper = UmdbDataShaper()


def plotKaplanValues(records, label):
    live_durations_dead = umdbHelper.getLiveDurationsOfDead(records)
    live_durations_censored = umdbHelper.getLiveDurationsOfCensored(records)
    mydf = pd.DataFrame()
    mydf['Durs'] = live_durations_dead + live_durations_censored
    mydf['events'] = [1] * len(live_durations_dead) + [0] * len(live_durations_censored)

    kmf = KaplanMeierFitter(label=label)
    kmf.fit(mydf['Durs'], mydf['events'])
    kmf.plot()
    plt.show()


def plotMultipleKaplanValues(arr_of_records, labels=[]):
    for idx, records in enumerate(arr_of_records):
        live_durations_dead = umdbHelper.getLiveDurationsOfDead(records)
        live_durations_censored = umdbHelper.getLiveDurationsOfCensored(records)
        mydf = pd.DataFrame()
        mydf['Durs'] = live_durations_dead + live_durations_censored
        mydf['events'] = [1] * len(live_durations_dead) + [0] * len(live_durations_censored)
        label = 'gragh' + str(idx + 1)
        if len(labels) != 0:
            try:
                label = labels[idx]
            except:
                a = 1
        kmf = KaplanMeierFitter(label=label)
        kmf.fit(mydf['Durs'], mydf['events'])
        kmf.plot()
    plt.show()


def getKaplanValues(records):
    live_durations_dead = umdbHelper.getLiveDurationsOfDead(records)
    live_durations_censored = umdbHelper.getLiveDurationsOfCensored(records)
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


def getKaplanValuesByDiagnosysName(diagnosys_name):  # todo move it
    records = umdbHelper.repo.getPatientsByDiagnosysName(diagnosys_name)
    return getKaplanValues(records)


def getKaplanValuesByDiagnosysPath(path):  # todo move it
    records = umdbHelper.repo.getPatientsByDiagnosysPath(path)
    live_durations_dead = umdbHelper.getLiveDurationsOfDead(records)
    live_durations_censored = umdbHelper.getLiveDurationsOfCensored(records)

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


def getKaplanValuesByDiagnosys(diagnosys):  # todo move it
    records = umdbHelper.repo.getPatientsByDiagnosysName(diagnosys)
    live_durations_dead = umdbHelper.getLiveDurationsOfDead(records)
    live_durations_censored = umdbHelper.getLiveDurationsOfCensored(records)

    mydf = pd.DataFrame()
    mydf['Durs'] = live_durations_dead + live_durations_censored
    mydf['events'] = [1] * len(live_durations_dead) + [0] * len(live_durations_censored)

    kmf = KaplanMeierFitter(label="waltons_data")
    kmf.fit(mydf['Durs'], mydf['events'])
    surv = kmf.survival_function_.values
    timeline = kmf.timeline
    lower = kmf.confidence_interval_['waltons_data_lower_0.95']
    upper = kmf.confidence_interval_['waltons_data_upper_0.95']
    return [surv, timeline, lower, upper, kmf.event_table]


def pltKMDiagnosesByNames(names):
    survs = []
    umdbRepo = UmdbRepository()
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
