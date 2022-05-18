from pymongo import MongoClient


class UmdbRepository:
    def getPath(self, nested_dict, value, prepath=()):
        for k, v in nested_dict.items():
            path = prepath + (k,)
            if v == value:  # found value
                return path
            elif hasattr(v, 'items'):  # v is a dict
                p = self.getPath(v, value, path)  # recursive call
                if p is not None:
                    return p

    def getDbClient(self, dbName='umdb'):
        # Provide the mongodb atlas url to connect python to mongodb using pymongo
        CONNECTION_STRING = "mongodb://localhost:27017/?readPreference=primary&appname=MongoDB%20Compass&directConnection=true&ssl=false"

        # Create a connection using MongoClient. You can import MongoClient or use pymongo.MongoClient
        client = MongoClient(CONNECTION_STRING)

        # Create the database for our example (we will use the same database throughout the tutorial
        return client[dbName]

    def getCollection(self, collection_name='records', dbName='umdb'):
        db = self.getDbClient(dbName)
        return db[collection_name]

    def getMostCommonDiagnosesPaths(self, withCounts=False, N=20):  # there is broken paths if big value
        # like ['1', '3', '6', 'Десмопластическая медуллобластома']

        collection = self.getCollection('records', 'umdb')
        pipeline = [{"$group": {"_id": '$diagnosis', "count": {"$sum": 1}}}]  # where '_id' is not None
        find = collection.aggregate(pipeline)
        pre = list(find)
        res = []
        for d in pre:
            if d["_id"] is not None:
                res.append(d)
        res = sorted(res, key=lambda d: d['count'], reverse=True)[:N]
        if withCounts:
            return res
        return list(map(lambda x: x['_id'], res))

    def getDiagnosysName(self, path):
        res = self.getCollection('dictionaries').find({"name": "diagnoses"})[0]['dictionary']
        for idx, key in enumerate(path):
            if idx > len(path) - 1:
                break
            dictKeys = res.keys()
            if key in dictKeys:
                res = res[key]
            else:
                res = res['children'][key]
        if type(res) is dict:
            return res['title']
        return res

    def getDiagnosysPath(self, name, withChildren=False, withTitle=False):
        col = self.getCollection('dictionaries').find({"name": "diagnoses"})[0]['dictionary']
        if withChildren:
            return self.getPath(col, name)
        else:
            newPath = []
            for node in self.getPath(col, name):
                if node != 'children':
                    newPath.append(node)

            if withTitle == False and newPath[len(newPath) - 1] == 'title':
                return newPath[:-1]
            return newPath

    def getPatientsByDiagnosysName(self, diagnosysName):
        diagnosysPath = self.getDiagnosysPath(diagnosysName)
        col = self.getCollection('records', 'umdb')
        return list(col.find({'diagnosis': diagnosysPath}))

    def getPatientsByDiagnosysPath(self, path):
        """

        :rtype: list
        """
        col = self.getCollection('records', 'umdb')
        return list(col.find({'diagnosis': path}))

    def getAllPatients(self):
        """

        :rtype: list
        """
        col = self.getCollection('records', 'umdb')
        return list(col.find())

    def getMaxLastEditDate(self):
        collection = self.getCollection('records', 'umdb')
        queryRes = collection.aggregate([{
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



