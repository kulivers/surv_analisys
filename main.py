import matplotlib.pyplot as plt
import numpy as np
import scipy.stats

from KaplanMeier import GetTimePointsNP2, GetConfidenceIntervals

most_common_diagnosys = ["Острый миелобастный лейкоз", 'B-ОЛЛ', "T-ОЛЛ", "Сверхтяжелая форма аплазии кроветворения",
                         "Нейробластома"]

diagnosis = repr(most_common_diagnosys[0])
[leikos_time_points, leikos_surv_P2, LEIKOS_P] = GetTimePointsNP2(repr(most_common_diagnosys[0]))
# [VOLL_time_points, VOLL_surv_P2, VOLL_P] = GetTimePointsNP2(repr(most_common_diagnosys[1]))
# [TOLL_time_points, TOLL_surv_P2, TOLL_P] = GetTimePointsNP2(repr(most_common_diagnosys[2]))
# [APLASIA_time_points, APLASIA_surv_P2, APLASIA_P] = GetTimePointsNP2(repr(most_common_diagnosys[3]))

lower = []
upper = []
for p in leikos_surv_P2:
    lower.append(p - 0.3)
    upper.append(p + 0.3)

# conf = GetConfidenceIntervals(leikos_surv_P2, )


plt.plot(leikos_time_points, leikos_surv_P2, drawstyle="steps-pre")
plt.fill_between(leikos_time_points, lower, upper, color='b', alpha=.1)
plt.ylabel('Вероятность')
plt.yticks(np.arange(0, 1.501, 0.1))
plt.xlabel('Дни')
plt.title(diagnosis)
plt.show()
