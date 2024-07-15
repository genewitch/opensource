import pymongo
import sys
import time
#import cProfile
#import pstats
#from pstats import SortKey


def insert_lines_to_mongodb(file_path, mongo_uri, db_name, collection_name):
    # Connect to MongoDB with specified maxPoolSize
    client = pymongo.MongoClient(mongo_uri, maxPoolSize=16, minPoolSize=5)
    db = client[db_name]
    collection = db[collection_name]

    # Batch size for insertion
    BATCH_SIZE = 225000
    batch = []
    # Variables for timing inserts
    start_time = time.time()  # Start time for measuring elapsed time
    totbatch = 0

    # Read the file and prepare documents
    with open(file_path, 'r') as file:
        for line in file:
            batch.append({"line": line.strip()})
            if len(batch) >= BATCH_SIZE:
                collection.insert_many(batch)
                batch = []
                totbatch += 1
                elapsed_time_us = (time.time() - start_time) * 1_000_000 #microseconds lol
                inserts_per_second = BATCH_SIZE / (time.time() - start_time)
                print(f"Elapsed time: {elapsed_time_us:.2f} microseconds")
                print(f"Rate of insert: {inserts_per_second:.2f} inserts per second")
                start_time = time.time()  # Reset start time for next batch
                print(f"total processed: {totbatch * BATCH_SIZE}")

        # Insert any remaining documents in the last batch
        if batch:
            collection.insert_many(batch)
            print(f"Inserted {len(batch)} lines into the collection '{collection_name}'")

    # Close the MongoDB connection
    client.close()

if __name__ == "__main__":
    if len(sys.argv) != 5:
        print("Usage: python insert_lines.py <file_path> <mongo_uri> <db_name> <collection_name>")
        sys.exit(1)

    file_path = sys.argv[1]
    mongo_uri = sys.argv[2]
    db_name = sys.argv[3]
    collection_name = sys.argv[4]

#cProfile.run('insert_lines_to_mongodb(file_path, mongo_uri, db_name, collection_name)', 'insertprofile')
insert_lines_to_mongodb(file_path, mongo_uri, db_name, collection_name)
#p = pstats.Stats('insertprofile')
#p.strip_dirs().sort_stats(SortKey.CUMULATIVE).print_stats()


