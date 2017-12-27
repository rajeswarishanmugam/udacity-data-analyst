# Author: Rajeswari Shanmugam
# Udacity Project for OpenstreetMap Analysis
# Dec 27 2017
from pymongo import MongoClient

db_name = 'udacity'
client = MongoClient('localhost', 27017)
db = client['udacity']
collection = db['output']

print("Fetch one record from Mongodb to test connection and entities")

print(collection.find_one())

print("lenght of users in collection")
print(len(collection.distinct('created.user')))

print ("Number of nodes:",collection.find({'type':'node'}).count())
print ("Number of ways:",collection.find({'type':'way'}).count())


print("Number of unique users")
result = collection.aggregate( [
                                        { "$group" : {"_id" : "$created.user",
                                        "count" : { "$sum" : 1} } },
                                        { "$sort" : {"count" : -1} },
                                        { "$limit" : 50 } ] )

print(list(result))

print("Ameneties in Chennai")
amenity = collection.aggregate([{'$match': {'amenity': {'$exists': 1}}}, \
                                {'$group': {'_id': '$amenity', \
                                            'count': {'$sum': 1}}}, \
                                {'$sort': {'count': -1}}, \
                                {'$limit': 10}])
print(list(amenity))

# Top Cusines
print("Top Cusines in Chennai")
cuisine = collection.aggregate([{"$match":{"amenity":{"$exists":1},
                                 "amenity":"restaurant",}},
                      {"$group":{"_id":{"Food":"$cuisine"},
                                 "count":{"$sum":1}}},
                      {"$project":{"_id":0,
                                  "Food":"$_id.Food",
                                  "Count":"$count"}},
                      {"$sort":{"Count":-1}},
                      {"$limit":6}])
print(list(cuisine))

# Top Buildings
print("Top Buildings in Chennai")
building = collection.aggregate([
       {'$match': {'building': { '$exists': 1}}},
        {'$group': {'_id': '$building',
                    'count': {'$sum': 1}}},
        {'$sort': {'count': -1}},
        {'$limit': 50}])
print(list(building))


# MTS Train stations
print("Train stations in Chennai")
train = collection.aggregate([
       {'$match': {'network': { '$exists': 1}}},
        {'$group': {'_id': '$network',
                    'count': {'$sum': 1}}},
        {'$sort': {'count': -1}},
        {'$limit': 10}])
print(list(train))
