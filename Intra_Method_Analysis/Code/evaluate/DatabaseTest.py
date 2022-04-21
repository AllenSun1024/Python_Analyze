import pymongo
from pprint import pprint

client = pymongo.MongoClient()
# db = client['TestSet']  # name of database -> TestSet
# collection = db['APIs']  # name of collection -> APIs
# counter = 0
# for x in collection.find({}, {'_id': 0}):
#     pprint(x)
#     counter += 1
# print(counter)
db = client["PopularProjects"]
collection = db["APIs"]
counter = 0
for x in collection.find({}, {'_id': 0}):
    counter += 1
print(counter)
    # pprint(x)
collection.drop()
