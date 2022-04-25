from datetime import datetime

import pandas as pd
from lifelines import KaplanMeierFitter, CoxPHFitter

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

    def getKaplanValuesByDiagnosysName(self, diagnosys_name):
        records = self.getPatientsByDiagnosysName(diagnosys_name)
        live_durations_dead = self.GetLiveDurationsOfDead(records)
        live_durations_censored = self.GetLiveDurationsOfCensored(records)

        mydf = pd.DataFrame()
        mydf['Durs'] = live_durations_dead + live_durations_censored
        mydf['events'] = [1] * len(live_durations_dead) + [0] * len(live_durations_censored)

        kmf = KaplanMeierFitter(label="waltons_data")
        kmf.fit(mydf['Durs'], mydf['events'])
        surv = kmf.survival_function_.values
        timeline = kmf.timeline
        lower = kmf.confidence_interval_['waltons_data_lower_0.95']
        upper = kmf.confidence_interval_['waltons_data_upper_0.95']
        return [surv, timeline, lower, upper]

    def getKaplanValuesByDiagnosysPath(self, path):
        records = self.repo.getPatientsByDiagnosysPath(path)
        live_durations_dead = self.GetLiveDurationsOfDead(records)
        live_durations_censored = self.GetLiveDurationsOfCensored(records)

        mydf = pd.DataFrame()
        mydf['Durs'] = live_durations_dead + live_durations_censored
        mydf['events'] = [1] * len(live_durations_dead) + [0] * len(live_durations_censored)

        kmf = KaplanMeierFitter(label="waltons_data")
        kmf.fit(mydf['Durs'], mydf['events'])
        surv = kmf.survival_function_.values
        timeline = kmf.timeline
        lower = kmf.confidence_interval_['waltons_data_lower_0.95']
        upper = kmf.confidence_interval_['waltons_data_upper_0.95']
        return [surv, timeline, lower, upper]

    def getKaplanValuesByDiagnosys(self, diagnosys):
        records = self.repo.getPatientsByDiagnosysName(diagnosys)
        live_durations_dead = self.GetLiveDurationsOfDead(records)
        live_durations_censored = self.GetLiveDurationsOfCensored(records)

        mydf = pd.DataFrame()
        mydf['Durs'] = live_durations_dead + live_durations_censored
        mydf['events'] = [1] * len(live_durations_dead) + [0] * len(live_durations_censored)

        kmf = KaplanMeierFitter(label="waltons_data")
        kmf.fit(mydf['Durs'], mydf['events'])
        surv = kmf.survival_function_.values
        timeline = kmf.timeline
        lower = kmf.confidence_interval_['waltons_data_lower_0.95']
        upper = kmf.confidence_interval_['waltons_data_upper_0.95']
        return [surv, timeline, lower, upper, kmf.event_table]

    def getPatientsBySex(self, records, sex='m'):
        sex_arr = None
        if sex is not None:
            sex_arr = [sex]

        res = []
        for r in records:
            try:
                if r['patient_sex'] == sex_arr:
                    res.append(r)
            except:
                continue
        return res

    def getKaplanValues(self, records):
        live_durations_dead = self.GetLiveDurationsOfDead(records)
        live_durations_censored = self.GetLiveDurationsOfCensored(records)

        mydf = pd.DataFrame()
        mydf['Durs'] = live_durations_dead + live_durations_censored
        mydf['events'] = [1] * len(live_durations_dead) + [0] * len(live_durations_censored)

        kmf = KaplanMeierFitter(label="waltons_data")
        kmf.fit(mydf['Durs'], mydf['events'])
        surv = kmf.survival_function_.values
        timeline = kmf.timeline
        lower = kmf.confidence_interval_['waltons_data_lower_0.95']
        upper = kmf.confidence_interval_['waltons_data_upper_0.95']
        return [surv, timeline, lower, upper]

    def getCoxValues(self, records):
        live_durations_dead = self.GetLiveDurationsOfDead(records)
        live_durations_censored = self.GetLiveDurationsOfCensored(records)

        mydf = pd.DataFrame()
        mydf['Durs'] = live_durations_dead + live_durations_censored
        mydf['events'] = [1] * len(live_durations_dead) + [0] * len(live_durations_censored)

        cph = CoxPHFitter()
        cph.fit(df=mydf, duration_col='Durs', event_col='events')
        # cph.fit(data, duration_col='time', event_col='status')
        a = 2221
        return cph
        surv = kmf.survival_function_.values
        timeline = kmf.timeline
        lower = kmf.confidence_interval_['waltons_data_lower_0.95']
        upper = kmf.confidence_interval_['waltons_data_upper_0.95']
        return [surv, timeline, lower, upper]
