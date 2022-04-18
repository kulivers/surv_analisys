import matplotlib.pyplot as plt
import numpy as np
from KaplanMeier import pure_surv_function
from DataHelper import DataHelper
from Repository import Repository

most_common_diagnosys = ["Острый миелобастный лейкоз", 'B-ОЛЛ', "T-ОЛЛ", "Сверхтяжелая форма аплазии кроветворения",
                         "Нейробластома"]
diagnosis = repr(most_common_diagnosys[1])

repo = Repository()
query = "Select `Дата диагноза_dt`, `Дата смерти_dt`, isDead, `Вид клеточной терапии`, `Выбыл из очереди`, `Дата постановки диагноза 1_dt`,  Пол, `Рецидив основного заболевания` from test where `Диагноз 1` = "
query = query + diagnosis
records = repo.RunQuery(query)

live_durations_dead = DataHelper.GetLiveDurationsOfDead(patients=records, daysSinceDiagnosis=12132131)

[time_points, surv_P2, P] = pure_surv_function(4100, live_durations_dead, len(records),
                                               len(live_durations_dead))

plt.plot(time_points, surv_P2, drawstyle="steps-pre")  # steps-pre is important for correct gragh
plt.ylabel('Вероятность')
plt.yticks(np.arange(0, 1.01, 0.1))
plt.xlabel('Дни')
plt.title(diagnosis)
plt.show()
print('P = ', P)

# # Planning_times_func
# [ counts, times ] = Planning_times_func(all_patients, max(live_durations_dead))
# plt.plot(times, counts)  # steps-pre is important for correct gragh
# plt.ylabel('counts')
# plt.xlabel('times')
# plt.title('planning times')
# plt.show()
#
