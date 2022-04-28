import pandas as pd
from lifelines import KaplanMeierFitter

from UmdbHelper import UmdbHelper
from UmdbRepository import UmdbRepository

umdbHelper = UmdbHelper()


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
