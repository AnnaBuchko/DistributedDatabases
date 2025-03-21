import time
import configparser
import logging
from concurrent.futures import ThreadPoolExecutor
from functools import partial

from bson import ObjectId
from pymongo import MongoClient, WriteConcern

# Configure logging to write to a file, appending new logs to it
logging.basicConfig(filename='massive-insert.log', level=logging.INFO, filemode='a',
                    format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger()


# Function to read database configuration
def read_db_config(config_file='database-conf.ini', section='database'):
    config = configparser.ConfigParser()
    config.read(config_file)

    # Check if the section exists in the file
    if section not in config:
        raise Exception(f"Section {section} not found in the {config_file} file")

    # Return the database configuration as a dictionary
    return {
        'uri': config.get(section, 'uri')
    }


def execute_functions_in_threads(func, max_workers=10):
    """
    Executes the same function concurrently in multiple threads.

    Args:
        func (callable): Function to execute.
        max_workers (int): Number of threads to use.
    """
    start_time = time.time()
    with ThreadPoolExecutor(max_workers=max_workers) as executor:
        # Submit the function `max_workers` times to the executor
        futures = [executor.submit(func) for _ in range(max_workers)]

        # Optionally, wait for completion and handle exceptions
        for future in futures:
            try:
                future.result()  # Retrieve the result or re-raise exceptions if any occurred
            except Exception as e:
                logger.error("Error executing function: %s", e)
    end_time = time.time()
    logger.info("Execution Time: %s seconds", '%.6f' % float(end_time - start_time))


# Function to establish a connection
def get_connection():
    db_config = read_db_config()
    try:
        return MongoClient(db_config.get("uri"))  # Ensure your MongoDB is running
    except Exception as e:
        logger.error("Error connecting to MongoDB: %s", e)
        return None


def reinit_table():
    conn_client = get_connection()
    if conn_client is None:
        print("Failed to connect to MongoDB.")
        return
    db = conn_client["homework"]
    collection = db["replicaSetTest"]
    collection.update_one(
        {"_id": ObjectId("67dbef3b79b3ade8cb6b1367")},
        {"$set": {"counter": 0}}
    )


def check_counter():
    conn_client = get_connection()
    db = conn_client["homework"]
    collection = db["replicaSetTest"]
    return collection.find_one({"_id": ObjectId("67dbef3b79b3ade8cb6b1367")})


def increment_counter(wc, wt):
    conn_client = get_connection()
    db = conn_client["homework"]
    collection = db["replicaSetTest"]
    collection = collection.with_options(write_concern=WriteConcern(w=wc,wtimeout=wt))

    for i in range(10000):
        collection.find_one_and_update(
            {"_id": ObjectId("67dbef3b79b3ade8cb6b1367")},
            {"$inc": {"counter": 1}},
            return_document=True
        )


#reinit_table()
#logger.info("Running test with WriteConcern = 1")
#execute_functions_in_threads(partial(increment_counter, 1, None))
#logger.info(check_counter())

reinit_table()
logger.info("Running test with WriteConcern = majority ")
execute_functions_in_threads(partial(increment_counter,"majority", 1000))
logger.info(check_counter())