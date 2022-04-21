import numpy as np
import pandas as pd
from lifelines import KaplanMeierFitter
from matplotlib import pyplot as plt

from HsctHelper import HsctHelper
from HsctRepository import HsctRepository
from UmdbHelper import UmdbHelper
from UmdbRepository import UmdbRepository

umdbRepo = UmdbRepository()
umdbHelper = UmdbHelper()
hsctRepo = HsctRepository()
hsctHelper = HsctHelper()


def GetEvents(durs):
    events = []
    for _ in durs:
        events.append(1)
    return events


if __name__ == '__main__':
    path = umdbRepo.getMostCommonDiagnosesPaths()[0]['_id']
    name = umdbRepo.getDiagnosysName(path)
    name = 'B-ОЛЛ'
    records = umdbRepo.getPatientsByDiagnosysName(name)
    records = hsctRepo.GetPatientsByDiagnosys(name)
    live_durations_dead = umdbHelper.GetLiveDurationsOfDead(records)
    live_durations_dead = hsctHelper.GetLiveDurationsOfDead(records)

    mydf = pd.DataFrame()
    mydf['Durs'] = live_durations_dead
    mydf['events'] = [1] * len(live_durations_dead)
    kmf = KaplanMeierFitter(label="waltons_data")
    kmf.fit(mydf['Durs'], mydf['events'])  # durations, event_observed
    surv = kmf.survival_function_.values
    timeline = kmf.timeline
    lower = kmf.confidence_interval_['waltons_data_lower_0.95']
    upper = kmf.confidence_interval_['waltons_data_upper_0.95']

    plt.plot(timeline, surv, drawstyle="steps-pre")
    plt.fill_between(timeline, lower, upper, color='b', alpha=.1)
    plt.ylabel('Вероятность')
    plt.yticks(np.arange(0, 1.01, 0.1))
    plt.xlabel('Дни')
    plt.title(name + ' - hsct')
    plt.show()
