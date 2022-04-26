from datetime import datetime

import pandas as pd
from lifelines import KaplanMeierFitter, CoxPHFitter
from past.types import basestring

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

    def GetLiveDurationsOfPatient(self, patient_record):
        maxLastEditDate = self.GetMaxLastEditDate()
        try:
            diagnosisDate = patient_record['diagnosis_date']
            lastEditDate = patient_record['last_edit_date']
            isDead = patient_record['death'] == ["1"]
            if isDead or diagnosisDate is None or diagnosisDate == '':
                return None
            if lastEditDate is None or lastEditDate == '':
                lastEditDate = maxLastEditDate
            lastEditDate = datetime.strptime(lastEditDate, '%d.%m.%Y')

            difference = lastEditDate - diagnosisDate
            if difference.days < 5000:
                return difference.days
        except:
            return None

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

    def isPatientMale(self, patient_record):
        try:
            if patient_record['patient_sex'] == ['m']:
                return 1
            return 0
        except:
            return None

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

    def formatDf(self, records, boolFieldNames, valuesToBeEqual, fieldsToReturn, fixBoolFields=False):
        """
        :type fixBoolFields: bool
        :type fieldsToReturn: list
        :type boolFieldNames: list
        :type valuesToBeEqual: list
        :type records: list
        """
        if len(boolFieldNames) != len(valuesToBeEqual):
            raise ValueError('lengths are not the same')

        fixedBoolFields = []
        for f in boolFieldNames:
            if not isinstance(f, str):
                raise ValueError('val in boolFieldNames is not string')
            fixedBoolFields.append(str(f) + '_bit')
        if fixBoolFields:
            boolFieldNames = fixedBoolFields

        df = pd.DataFrame(columns=fieldsToReturn + boolFieldNames)

        for i, r in enumerate(records):
            row = []
            for f in fieldsToReturn:
                try:
                    row.append(r[f])
                except:
                    row.append(False)
            for idx, f in enumerate(boolFieldNames):
                try:
                    if r[f] == valuesToBeEqual[idx]:
                        row.append(True)
                    else:
                        row.append(False)
                except:
                    row.append(False)
            df.loc[i] = row

        return df
