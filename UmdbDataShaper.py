from datetime import datetime
import pandas as pd
from UmdbRepository import UmdbRepository


class UmdbDataShaper:
    repo = UmdbRepository()

    def getLiveDurationsOfDead(self, records, daysSinceDiagnosis=12132131):
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

    def getPatientStatus(self, record, withMinusOneIfCensored=False):
        try:
            if record['death'] is None:
                if withMinusOneIfCensored:
                    return -1
                return 0
            if record['death'] == ["0"]:
                return 0
            return 1
        except:
            if withMinusOneIfCensored:
                return -1
            return 0

    def getStatusAndLiveDurationsOfPatients(self, records):
        res = []
        for r in records:
            res.append(self.getLiveDurationOfPatient(r))
        return res

    def getLiveDurationOfPatient(self, record):
        status = self.getPatientStatus(record)
        repo = UmdbRepository()
        maxLastEditDate = repo.getMaxLastEditDate()

        if status == 1:
            try:
                deathDate = record['death_date']
                diagnosisDate = record['diagnosis_date']
                if deathDate is None or deathDate == '' or diagnosisDate is None or diagnosisDate == '':
                    raise ValueError
                difference = deathDate - diagnosisDate
                duration = difference.days
                return {"status": status, "duration": duration}
            except:
                return {"status": status, "duration": None}

        if status == -1 or status == 0:
            try:
                diagnosisDate = record['diagnosis_date']
                lastEditDate = record['last_edit_date']
                if diagnosisDate is None or diagnosisDate == '':
                    raise ValueError
                if lastEditDate is None or lastEditDate == '':
                    lastEditDate = datetime.strptime(maxLastEditDate, '%d.%m.%Y')
                if type(lastEditDate) is str:
                    lastEditDate = datetime.strptime(lastEditDate, '%d.%m.%Y')

                duration = (lastEditDate - diagnosisDate).days
                if duration > 5000:
                    raise ValueError

                return {"status": status, "duration": duration}
            except:
                return {"status": status, "duration": None}

    def getLiveDurationsOfCensored(self, records):  # diagnosis date - last edit date/max(last edit date)
        durations = []
        repo = UmdbRepository()
        maxLastEditDate = repo.getMaxLastEditDate()
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

    def renameDublucateColumns(self, df):
        cols = list(df.columns)
        newlist = []
        for i, v in enumerate(cols):
            totalcount = cols.count(v)
            count = cols[:i].count(v)
            newlist.append(v + str(count + 1) if totalcount > 1 else v)
        df.columns = newlist
        return df

    # df = df.drop(columns=df.columns[0])

    def removeArrayColumns(self, df):
        def delete_multiple_element(list_object, indices):
            indices = sorted(indices, reverse=True)
            for idx in indices:
                if idx < len(list_object):
                    list_object.pop(idx)

        init_columns = list(df.columns)
        columns = list(df.columns)
        if len(columns) != len(set(columns)):
            df = self.renameDublucateColumns(df)
            columns = list(df.columns)
        # get columns with arrays data, save their indexes

        to_delete_cols_idxs = []
        for idx, col in enumerate(columns):
            if any(isinstance(x, list) for x in list(df[col])):
                to_delete_cols_idxs.append(idx)

        # for drop them all
        to_delete_names = list(map(lambda x: df.columns[x], to_delete_cols_idxs))
        df = df.drop(columns=to_delete_names)

        # rename columns back
        delete_multiple_element(init_columns, to_delete_cols_idxs)
        df.columns = init_columns
        return df

    def formatDf(self, records, boolFieldNames=[], simpleFieldsToReturn=[], withNones=True, removeArrayColumns=False):
        """
        :type removeArrayColumns: bool
        :type fixBoolFields: bool
        :type fieldsToReturn: list
        :type boolFieldNames: list
        :type valuesToBeEqual: list
        :type records: list
        """

        df = pd.DataFrame(columns=simpleFieldsToReturn + boolFieldNames)

        saved_values = dict()  # dict({"fieldName": ['savedVal1', 'savedVal2']})  # return: idx: val

        for i, r in enumerate(records):
            row = []
            for f in simpleFieldsToReturn:  # add to row simpleFieldsToReturn values
                try:
                    row.append(r[f])
                except:
                    row.append(0)
            for idx, f in enumerate(boolFieldNames):  # add to row boolFieldNames values
                try:
                    if f not in saved_values.keys():
                        saved_values[f] = []
                    if r[f] not in saved_values[f]:
                        saved_values[f].append(r[f])
                    if r[f] in saved_values[f]:
                        ii = saved_values[f].index(r[f])
                        row.append(ii)
                except:
                    row.append(None)
            df.loc[i] = row

        if removeArrayColumns:
            df = self.removeArrayColumns(df)

        if not withNones:
            df.dropna(axis=0, inplace=True)

        return df, saved_values

    def getConditioningElements(self, record):
        elements_object = dict()
        try:
            elements_object = record['conditioning_elements']
        except:
            return [], dict()
        active_elements = []
        doses = dict()
        keys = list(elements_object.keys())
        for key in keys:
            if key == '_id':
                continue
            try:
                if elements_object[key]['is_active']:
                    active_elements.append(key)
            except:
                continue
            try:
                if elements_object[key]['is_active']:
                    dose = elements_object[key]['dose']
                    doses[key] = dose
            except:
                continue

        return active_elements, doses

    def formConditioningElementsDataFrame(self, conditioning_elements):
        listOfAllElements = []
        for sublist in conditioning_elements:
            for element in sublist:
                if element not in listOfAllElements:
                    listOfAllElements.append(element)
        df = pd.DataFrame(columns=listOfAllElements)
        for idx, sublist in enumerate(conditioning_elements):
            columnNames = list(df.columns)
            row = []
            # take every name in columnName, if name in sublist row append 1 else 0
            for name in columnNames:
                if name in sublist:
                    row.append(1)
                else:
                    row.append(0)
            df.loc[idx] = row
        return df

    def getConditioningElementsForPatients(self, records, returnDf=True):
        """
        :rtype: list
        """
        active_elements = []
        for record in records:
            elementsForRecord = self.getConditioningElements(record)
            active_elements.append(elementsForRecord)

        conditioning_els = list(map(lambda x: x[0], active_elements))
        conditioning_els_doses = list(map(lambda x: x[1], active_elements))

        if returnDf:
            return self.formConditioningElementsDataFrame(conditioning_els), conditioning_els_doses

        return conditioning_els, conditioning_els_doses
