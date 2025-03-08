import time
import warnings
import configparser
import logging
from concurrent.futures import ThreadPoolExecutor
from typing import LiteralString

from neo4j import GraphDatabase, PreviewWarning

# Configure logging to write to a file, appending new logs to it
logging.basicConfig(filename='massive-insert.log', level=logging.INFO, filemode='a',
                    format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger()
warnings.filterwarnings("ignore", category=PreviewWarning)

# Function to read database configuration
def read_db_config(config_file='database-conf.ini', section='database'):
    config = configparser.ConfigParser()
    config.read(config_file)

    # Check if the section exists in the file
    if section not in config:
        raise Exception(f"Section {section} not found in the {config_file} file")

    # Return the database configuration as a dictionary
    return {
        'uri': config.get(section, 'uri'),
        'user': config.get(section, 'user'),
        'password': config.get(section, 'password')
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


db_conf = read_db_config()


def get_driver():
    return GraphDatabase.driver(db_conf.get('uri'), auth=(db_conf.get('user'), db_conf.get('password')))


def reinit_value():
    query: LiteralString = """
    MATCH (n:Item) WHERE n.id = 4
    SET n.no_like = 0
    """
    with get_driver() as driver:
        driver.session().run(query)
    driver.close()


def update_node_run(tx):
    query: LiteralString = """
    MATCH (n:Item) WHERE n.id = 4
    SET n.no_like = n.no_like + 1
    """
    result = tx.run(query)
    return result.consume()


def update_node_property():
    driver = get_driver()
    for i in range(10000):
        with driver.session(database='neo4j') as session:
            session.execute_write(update_node_run)
            session.close()
    driver.close()


reinit_value()
logger.info("Running update")
execute_functions_in_threads(update_node_property)
# update_node_property()