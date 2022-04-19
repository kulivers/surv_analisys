from datetime import datetime, timedelta

from Repository import Repository


class PatientsHelper:
    curDate = datetime(2021, 5, 31)

    @staticmethod
    def GetLiveDurationsOfDead(patients, daysSinceDiagnosis=12132131):
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
    def GetLiveDurationsOfAlived(patients, daysSinceDiagnosis=12121122, withCensored=False):
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


