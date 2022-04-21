import numpy as np
import pandas as pd
from lifelines import KaplanMeierFitter
from lifelines.datasets import load_waltons
from matplotlib import pyplot as plt
from HsctHelper import HsctHelper
from HsctRepository import HsctRepository


def GetEvents(durs):
    events = []
    for _ in durs:
        events.append(1)
    return events


hsct_repo = HsctRepository()
most_common_diagnosys = ["Острый миелобастный лейкоз", 'B-ОЛЛ', "T-ОЛЛ", "Сверхтяжелая форма аплазии кроветворения",
                         "Нейробластома"]


def GetFitByDiagnosys(diagnosis_p):
    diagnosis = repr(diagnosis_p)
    records = hsct_repo.GetPatientsByDiagnosys(diagnosis)
    live_durations_dead = HsctHelper.GetLiveDurationsOfDead(records)
    mydf = pd.DataFrame()
    mydf['Durs'] = live_durations_dead
    mydf['events'] = GetEvents(live_durations_dead)
    kmf = KaplanMeierFitter(label="waltons_data")
    kmf.fit(mydf['Durs'], mydf['events'])  # durations, event_observed
    surv = kmf.survival_function_.values
    timeline = kmf.timeline
    lower = kmf.confidence_interval_['waltons_data_lower_0.95']
    upper = kmf.confidence_interval_['waltons_data_upper_0.95']
    return [surv, timeline, lower, upper]


[surv, timeline, lower, upper] = GetFitByDiagnosys(most_common_diagnosys[0])
plt.plot(timeline, surv, drawstyle="steps-pre")
plt.fill_between(timeline, lower, upper, color='b', alpha=.1)


[surv, timeline, lower, upper] = GetFitByDiagnosys(most_common_diagnosys[1])
plt.plot(timeline, surv, drawstyle="steps-pre")
plt.fill_between(timeline, lower, upper, color='b', alpha=.1)


plt.ylabel('Вероятность')
plt.yticks(np.arange(0, 1.01, 0.1))
plt.xlabel('Дни')
plt.title('2) TESTING last')
plt.show()
