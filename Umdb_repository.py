from pymongo import MongoClient
import pymongo


def getPath(nested_dict, value, prepath=()):
    for k, v in nested_dict.items():
        path = prepath + (k,)
        if v == value:  # found value
            return path
        elif hasattr(v, 'items'):  # v is a dict
            p = getPath(v, value, path)  # recursive call
            if p is not None:
                return p


def getDbClient(dbName='umdb'):
    # Provide the mongodb atlas url to connect python to mongodb using pymongo
    CONNECTION_STRING = "mongodb://localhost:27017/?readPreference=primary&appname=MongoDB%20Compass&directConnection=true&ssl=false"

    # Create a connection using MongoClient. You can import MongoClient or use pymongo.MongoClient
    client = MongoClient(CONNECTION_STRING)

    # Create the database for our example (we will use the same database throughout the tutorial
    return client[dbName]


def getCollection(collection_name='records', dbName='umdb'):
    db = getDbClient(dbName)
    return db[collection_name]


def getMostCommonDiagnoses(N=20):
    collection = getCollection('records', 'umdb')
    pipeline = [{"$group": {"_id": '$diagnosis', "count": {"$sum": 1}}}]  # where '_id' is not None
    find = collection.aggregate(pipeline)
    pre = list(find)
    res = []
    for d in pre:
        if d["_id"] is not None:
            res.append(d)
    res = sorted(res, key=lambda d: d['count'], reverse=True)[:N]
    return res


def getDiagnosysName(path):
    res = getCollection('dictionaries').find({"name": "diagnoses"})[0]['dictionary']
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


def getDiagnosysPath(name, withChildren=False, withTitle=False):
    col = getCollection('dictionaries').find({"name": "diagnoses"})[0]['dictionary']
    if withChildren:
        return getPath(col, name)
    else:
        newPath = []
        for node in getPath(col, name):
            if node != 'children':
                newPath.append(node)

        if withTitle == False and newPath[len(newPath) - 1] == 'title':
            return newPath[:-1]
        return newPath


def getPatientsByDiagnosysName(diagnosysName):
    diagnosysPath = getDiagnosysPath(diagnosysName)
    col = getCollection('records', 'umdb')
    return list(col.find({'diagnosis': diagnosysPath}))



def printMostCommonDiagnoses(N=10):
    com = getMostCommonDiagnoses(N)
    for d in com:
        path = d['_id']
        count = d['count']
        try:
            name = getDiagnosysName(path)
            print(path, name, ' - ', count)
        except:
            print('broken path')


if __name__ == "__main__":
    printMostCommonDiagnoses()
    # path = getDiagnosysPath('Нейробластома')
    patients = getPatientsByDiagnosysName('Нейробластома')
    print('done')
