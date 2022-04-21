import numpy as np
import pandas as pd
from lifelines import KaplanMeierFitter
from lifelines.datasets import load_waltons
from matplotlib import pyplot as plt
from PatientsHelper import PatientsHelper
from Hsct_repository import Hsct_repository


def GetEvents(durs):
    events = []
    for _ in durs:
        events.append(1)
    return events


hsct_repo = Hsct_repository()
most_common_diagnosys = ["Острый миелобастный лейкоз", 'B-ОЛЛ', "T-ОЛЛ", "Сверхтяжелая форма аплазии кроветворения",
                         "Нейробластома"]

diagnosis = repr(most_common_diagnosys[0])
records = hsct_repo.GetPatientsByDiagnosys(diagnosis)
live_durations_dead = PatientsHelper.GetLiveDurationsOfDead(records)
alivedCens = PatientsHelper.GetAlivedPatients(records, withCensored=True)
alivedNotCens = PatientsHelper.GetAlivedPatients(records, withCensored=False)
mydf = pd.DataFrame()
mydf['Durs'] = live_durations_dead
mydf['events'] = GetEvents(live_durations_dead)

waltons = load_waltons()
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
plt.title('2) TESTING last')
plt.show()
