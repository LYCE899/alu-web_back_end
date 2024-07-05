#!/usr/bin/env python3
""" log stats """
from pymongo import MongoClient

def main(collection):
    """ log stats """

    num_logs = collection.count_documents({})
    methods = ["GET", "POST", "PUT", "PATCH", "DELETE"]
    results = {method: 0 for method in methods}
    num_status_check = collection.count_documents({"method": "GET", "path": "/status"})
    
    for method in methods:
        num_method = collection.count_documents({"method": method})
        results[method] = num_method
    
    print("{} logs".format(num_logs))
    print("Methods:")
    for method in methods:
        print("\tmethod {}: {}".format(method, results[method]))
    
    print("{} status check".format(num_status_check))

if __name__ == "__main__":
    client = MongoClient()
    db = client.logs
    logs = db.nginx
    main(logs)
