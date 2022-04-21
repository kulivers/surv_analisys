import math
from cmath import sqrt

from HsctPatientsHelper import HsctPatientsHelper
from HsctRepository import HsctRepository


def GetConfidenceIntervals(kaplanMeierPoints, alivedCount, deadPoints):
    if len(deadPoints) != len(kaplanMeierPoints):
        raise ValueError('alivedPoints, deadPoints should have same length')
    sumAtT = 0
    confIntervals = []
    for idx, deadAtT in enumerate(deadPoints):
        alivedAtT = alivedCount - deadAtT
        sumAtT += deadAtT / (alivedAtT * (alivedCount - deadAtT))
        result = sqrt(sumAtT) * kaplanMeierPoints[idx]
        confIntervals.append(result)
    return confIntervals


def pure_surv_function2(t, live_durations_dead, count_of_alived, N=None):
    # live_durations = count of days, N = how many points, t - time for calculating probability
    # t нужна только чтобы высчитать вероятность P(идет на выходе) выжить в момент t
    # разбили все дни на степы

    if N is None:
        N = len(live_durations_dead)

    maximum_days = max(live_durations_dead)
    step = int(maximum_days / N)
    time_steps = list(range(0, maximum_days + step, step))

    if N is None:
        time_steps = sorted(live_durations_dead)

    ChancesPointsArr = []
    multi = 1
    count_alived_on_start = len(live_durations_dead) + count_of_alived

    for ti in time_steps:
        count_of_dead_at_ti = 0
        for dur in live_durations_dead:
            if dur < ti:
                count_of_dead_at_ti += 1
        chanceInPoint = (count_alived_on_start - count_of_dead_at_ti) / count_alived_on_start
        ChancesPointsArr.append(chanceInPoint)

    # now we want to get P of survive at t
    idxOf_t = 0
    # находим нашу точку t на нашем разбиении time_steps

    for idx, ti in enumerate(time_steps):
        if ti >= t:
            idxOf_t = idx
            break

    if t > max(time_steps):
        idxOf_t = len(time_steps) - 1

    # находим вероятность на этой точке в массиве result chances
    ChanceOnPoint_t = ChancesPointsArr[idxOf_t]
    return [time_steps, ChancesPointsArr, ChanceOnPoint_t]


def GetKaplanPoints(diagnosis_name):
    repo = HsctRepository()
    records = repo.GetPatientsByDiagnosys(diagnosis_name)
    live_durations_dead = HsctPatientsHelper.GetLiveDurationsOfDead(records)
    alivedCens = HsctPatientsHelper.GetAlivedPatients(records, withCensored=True)
    alivedNotCens = HsctPatientsHelper.GetAlivedPatients(records, withCensored=False)

    return pure_surv_function(max(live_durations_dead) + 1, live_durations_dead, len(alivedNotCens))


def pure_surv_function(t, live_durations_dead, count_of_alived_without_cens):
    time_steps = sorted(live_durations_dead)

    chances_points_arr = []
    confidence_intervals = []
    multi = 1
    count_alived_on_start_without_cens = len(live_durations_dead) + count_of_alived_without_cens
    confidence_intervals_sum = 0
    for ti in time_steps:
        count_of_dead_at_ti = 0
        for dur in live_durations_dead:
            if dur < ti:
                count_of_dead_at_ti += 1
        count_of_dead_at_ti = 1
        count_alived_at_ti = count_alived_on_start_without_cens - count_of_dead_at_ti
        chanceInPoint = ((count_alived_at_ti - count_of_dead_at_ti) / count_alived_at_ti) * multi
        multi = chanceInPoint
        chances_points_arr.append(chanceInPoint)

        confidence_intervals_sum += count_of_dead_at_ti / (count_alived_at_ti * (count_alived_at_ti - count_of_dead_at_ti))
        confidence_interval_at_ti = chanceInPoint * math.sqrt(confidence_intervals_sum)
        confidence_intervals.append(confidence_interval_at_ti)

    idxOf_t = 0

    for idx, ti in enumerate(time_steps):
        if ti >= t:
            idxOf_t = idx
            break

    if t > max(time_steps):
        idxOf_t = len(time_steps) - 1

    # находим вероятность на этой точке в массиве result chances
    ChanceOnPoint_t = chances_points_arr[idxOf_t]
    return [time_steps, chances_points_arr, ChanceOnPoint_t, confidence_intervals]
