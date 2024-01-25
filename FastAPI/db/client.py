# This file is responsible for managing the connection with Mongo database

from pymongo import MongoClient

# Local database
# db_client = MongoClient().local

# Cloud database
uri = 'mongodb+srv://diegomatias:diego123@cluster0.flzhifa.mongodb.net/?retryWrites=true&w=majority'

db_client = MongoClient(uri).test