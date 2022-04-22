import numpy as np
import pandas as pd
from lifelines import KaplanMeierFitter
from matplotlib import pyplot as plt
from lifelines.statistics import logrank_test

from HsctHelper import HsctHelper
from HsctRepository import HsctRepository
from UmdbHelper import UmdbHelper
from UmdbRepository import UmdbRepository

umdbRepo = UmdbRepository()
umdbHelper = UmdbHelper()
hsctRepo = HsctRepository()
hsctHelper = HsctHelper()


def getKaplanValuesByDiagnosys(diagnosys):
    records = umdbRepo.getPatientsByDiagnosysName(diagnosys)
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


if __name__ == '__main__':
    path1 = umdbRepo.getMostCommonDiagnosesPaths()[0]['_id']
    name1 = umdbRepo.getDiagnosysName(path1)
    [surv, timeline, lower, upper] = getKaplanValuesByDiagnosys(name1)

    path2 = umdbRepo.getMostCommonDiagnosesPaths()[4]['_id']
    name2 = umdbRepo.getDiagnosysName(path2)
    [surv2, timeline2, lower2, upper2] = getKaplanValuesByDiagnosys(name2)

    results = logrank_test(surv, surv2, event_observed_A=timeline, event_observed_B=timeline2).p_value

    plt.plot(timeline, surv, drawstyle="steps-pre")
    plt.plot(timeline2, surv2, drawstyle="steps-pre")
    plt.fill_between(timeline, lower, upper, color='b', alpha=.1)
    plt.fill_between(timeline2, lower2, upper2, color='b', alpha=.1)
    plt.ylabel('Вероятность')
    plt.yticks(np.arange(0, 1.01, 0.1))
    plt.xlabel('Дни')
    plt.title('SURV')
    plt.show()
