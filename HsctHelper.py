from datetime import datetime, timedelta

from HsctRepository import HsctRepository


class HsctHelper:
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
    def GetAlivedPatients(patients, daysSinceDiagnosis=12121122, withCensored=True):
        # дата постановки диагноза 1 - Дата ТГСК утверждена

        durations = []
        for p in patients:
            diagnosisDate = p['Дата постановки диагноза 1_dt']
            isDead = p['isDead']
            if diagnosisDate is None:
                continue
            if withCensored:
                if isDead != 1:  # all not dead (+no data)
                    durations.append(p)
            else:
                if isDead == -1:  # only dead
                    durations.append(p)

        return durations


