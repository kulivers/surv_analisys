from UmdbRepository import UmdbRepository


class UmdbHelper:
    repo = UmdbRepository()

    def GetLiveDurationsOfDead(self, records, daysSinceDiagnosis=12132131):
        durations = []
        for r in records:
            try:
                deathDate = r['death_date']
                diagnosisDate = r['diagnosis_date']
                if deathDate is None or deathDate == '' or diagnosisDate is None or diagnosisDate == '':
                    continue
                difference = deathDate - diagnosisDate
                if difference.days <= daysSinceDiagnosis:
                    durations.append(difference.days)
            except:
                a = 1

        return sorted(durations)
