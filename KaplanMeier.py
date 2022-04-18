def pure_surv_function(t, live_durations_dead, count_of_alived, N=20):
    # live_durations = count of days, N = how many points, t - time for calculating probability
    # t нужна только чтобы высчитать вероятность P(идет на выходе) выжить в момент t
    # разбили все дни на степы
    maximum_days = max(live_durations_dead)
    step = int(maximum_days / N)
    time_steps = list(range(0, maximum_days + step, step))

    # default values
    ChancesPointsArr = []
    multi = 1
    count_alived_on_start = len(live_durations_dead) + count_of_alived

    for ti in time_steps:
        count_of_dead_at_ti = 0
        for dur in live_durations_dead:
            if dur < ti:
                count_of_dead_at_ti += 1
        # формула выживаемости для каждой точки, на каждую точку считам сколько померло
        chanceInPoint = (count_alived_on_start - count_of_dead_at_ti) / count_alived_on_start

        # я так понимаю ниже для условной вероятности, но почему он зависит от количество точек это не правильно!!
        # multi = multi * chanceInPoint
        # chanceInPoint = multi

        ChancesPointsArr.append(chanceInPoint)

    # now we want to get P of survive at t
    idxOf_t = 0
    # находим нашу точку t на нашем разбиении time_steps

    for idx, ti in enumerate(time_steps):
        if ti >= t:
            idxOf_t = idx
            break

    if t > max(time_steps):
        idxOf_t = len(time_steps)-1

    # находим вероятность на этой точке в массиве result chances
    ChanceOnPoint_t = ChancesPointsArr[idxOf_t]
    return [time_steps, ChancesPointsArr, ChanceOnPoint_t]


def Risks_function(t, delta_t, live_durations_dead, planning_durations_alived, N=20):
    # вероятность того, что смерть произошла в интервале времени [t, t + delta t].
    [_S1, _time_steps, t_P1] = pure_surv_function(t, live_durations_dead, planning_durations_alived, N)
    [_S2, _time_steps2, t_P2] = pure_surv_function(t + delta_t, live_durations_dead, planning_durations_alived, N)
    death_p1 = 1 - t_P1
    death_p2 = 1 - t_P2

    val = (death_p2 - death_p1) * death_p1 / (delta_t)

    return val
