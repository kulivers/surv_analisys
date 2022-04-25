from datetime import datetime

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

    def GetMaxLastEditDate(self):
        col = self.repo.getCollection()
        queryRes = col.aggregate([{
            "$project": {
                "last_edit_date": {
                    "$dateFromString": {
                        "dateString": '$last_edit_date'
                    }
                }
            }
        }, {"$sort": {"last_edit_date": -1}}])
        result = list(queryRes)
        return result[0]['last_edit_date']

    def GetLiveDurationsOfCensored(self, records):  # diagnosis date - last edit date/max(last edit date)
        durations = []
        maxLastEditDate = self.GetMaxLastEditDate()
        for r in records:
            try:
                diagnosisDate = r['diagnosis_date']
                lastEditDate = r['last_edit_date']
                isDead = r['death'] == ["1"]
                if isDead or diagnosisDate is None or diagnosisDate == '':
                    continue
                if lastEditDate is None or lastEditDate == '':
                    lastEditDate = maxLastEditDate
                lastEditDate = datetime.strptime(lastEditDate, '%d.%m.%Y')

                difference = lastEditDate - diagnosisDate
                if difference.days < 5000:
                    durations.append(difference.days)
            except:
                continue

        return sorted(durations)

