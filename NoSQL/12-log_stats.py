#!/usr/bin/env python3
""" log stats """
from pymongo import MongoClient

def main(collection):
    """ log stats"""

    num_logs = collection.count_documents({})
    methods = ["GET", "POST", "PUT", "PATCH", "DELETE"]
    results = {method: collection.count_documents({"method": method}) for method in methods}
    num_status_check = collection.count_documents({"method": "GET", "path": "/status"})

    print(f"{num_logs} logs")
    print("Methods:")
    for method in methods:
        print(f"\tmethod {method}: {results[method]}")
    print(f"{num_status_check} status check")

if __name__ == "__main__":
    client = MongoClient('mongodb://localhost:27017/')
    db = client.logs
    logs = db.nginx
    main(logs)
