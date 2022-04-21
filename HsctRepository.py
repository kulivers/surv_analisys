from datetime import datetime

import mysql.connector
from mysql.connector import cursor


class HsctRepository:
    patients = {}

    def RunQuery(self, query):
        cnx = mysql.connector.connect(user='root', password='qwerty',
                                      host='localhost', port='3306',
                                      database='surv_db')
        # "Острый миелобастный лейкоз"
        # 'B-ОЛЛ'
        # "T-ОЛЛ"
        # "Сверхтяжелая форма аплазии кроветворения"
        # "Нейробластома"

        mycursor = cnx.cursor()

        mycursor.execute(query)

        #
        # for idx, name in enumerate(columnNames):
        #     print(idx, name)
        #
        # for x in mycursor:
        #     print(x[5])

        data = []
        columnNames = mycursor.column_names

        for x in mycursor:
            rowObj = {}
            for idx, colName in enumerate(columnNames):
                val = x[idx]
                rowObj[colName] = val
            data.append(rowObj)

        cnx.close()
        return data

    def __init__(self):
        cnx = mysql.connector.connect(user='root', password='qwerty',
                                      host='localhost', port='3306',
                                      database='surv_db')
        # "Острый миелобастный лейкоз"
        # 'B-ОЛЛ'
        # "T-ОЛЛ"
        # "Сверхтяжелая форма аплазии кроветворения"
        # "Нейробластома"

        query = 'Select `Дата диагноза_dt`, `Дата смерти_dt`, isDead, `Вид клеточной терапии`, `Выбыл из очереди`, Пол, `Рецидив основного заболевания` from test where `Диагноз 1` = "Острый миелобастный лейкоз"'

        mycursor = cnx.cursor()

        mycursor.execute(query)

        #
        # for idx, name in enumerate(columnNames):
        #     print(idx, name)
        #
        # for x in mycursor:
        #     print(x[5])

        data = []
        columnNames = mycursor.column_names

        for x in mycursor:
            rowObj = {}
            for idx, colName in enumerate(columnNames):
                val = x[idx]
                rowObj[colName] = val
            data.append(rowObj)

        cnx.close()

    def GetPatientsByDiagnosys(self, diagnosis_name):
        query = "Select `Дата диагноза_dt`, `Дата смерти_dt`, isDead, `Вид клеточной терапии`, `Выбыл из очереди`, `Дата постановки диагноза 1_dt`,  Пол, `Рецидив основного заболевания` from test where `Диагноз 1` = "
        query = query + repr(diagnosis_name)
        records = self.RunQuery(query)
        return records
