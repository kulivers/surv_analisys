# import matplotlib.pyplot as plt
# import numpy as np
#
# from KaplanMeier import GetKaplanPoints
# from HsctHelper import HsctHelper
# from HsctRepository import HsctRepository
#
# repo = HsctRepository()
# most_common_diagnosys = ["Острый миелобастный лейкоз", 'B-ОЛЛ', "T-ОЛЛ", "Сверхтяжелая форма аплазии кроветворения",
#                          "Нейробластома"]
#
# diagnosis = repr(most_common_diagnosys[0])
# [leikos_time_points, leikos_surv_P2, LEIKOS_P, confidence_intervals] = GetKaplanPoints(diagnosis)
#
# live_durations_dead = HsctHelper.GetLiveDurationsOfDead(repo.GetPatientsByDiagnosys(diagnosis))
# aliveCount = len(repo.GetPatientsByDiagnosys(diagnosis))
#
# lower = []
# upper = []
# for idx, p in enumerate(leikos_surv_P2):
#     ci = confidence_intervals[idx]
#     lower.append(p - ci*0.05)
#     upper.append(p + ci*0.05)
#
#
# plt.plot(leikos_time_points, leikos_surv_P2, drawstyle="steps-pre")
# plt.fill_between(leikos_time_points, lower, upper, color='b', alpha=.1)
# plt.ylabel('Вероятность')
# plt.yticks(np.arange(0, 1.01, 0.1))
# plt.xlabel('Дни')
# plt.title(diagnosis)
# plt.show()
