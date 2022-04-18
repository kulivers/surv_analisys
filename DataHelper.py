from datetime import datetime, timedelta

from Repository import Repository


class DataHelper:
    curDate = datetime(2021, 5, 31)

    @staticmethod
    def GetLiveDurationsOfDead(patients, daysSinceDiagnosis):
        durations = []
        for p in patients:
            deathDate = p['Дата смерти_dt']
            diagnosisDate = p['Дата постановки диагноза 1_dt']
            if deathDate is None or diagnosisDate is None:
                continue
            daysToDeath = deathDate - diagnosisDate
            if daysToDeath.days <= daysSinceDiagnosis:
                durations.append(daysToDeath.days)
        return durations

    @staticmethod
    def GetLiveDurationsOfAlived(patients, daysSinceDiagnosis, withCensored=False):
        # дата постановки диагноза 1 - Дата ТГСК утверждена

        durations = []
        for p in patients:
            diagnosisDate = p['Дата постановки диагноза 1_dt']
            # tgskDate = p['Дата ТГСК утверждена_dt']
            isDead = p['isDead']
            if diagnosisDate is None:
                continue
            if withCensored:
                if isDead != 1:  # all not dead (+no data)
                    days = diagnosisDate + timedelta(days=daysSinceDiagnosis)  # здесь дата минус
                    durations.append(days.days)
            else:
                if isDead == -1:  # only dead
                    days = diagnosisDate + timedelta(days=daysSinceDiagnosis)  # здесь дата минус дни. не хорошо
                    durations.append(days.days)

        return durations


def pure_surv_function(t, live_durations_dead, planning_durations_alived, N=20):
    a = 1
# live_durations = count of days, N = how many points, t - time for calculating probability
# t нужна только чтобы высчитать вероятность P(идет на выходе) выжить в момент t
# разбили все дни на степы
