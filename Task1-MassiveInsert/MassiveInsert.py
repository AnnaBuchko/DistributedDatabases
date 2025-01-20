import time
import psycopg2
import configparser
import logging
from concurrent.futures import ThreadPoolExecutor


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
        'host': config.get(section, 'host'),
        'port': config.get(section, 'port'),
        'dbname': config.get(section, 'dbname'),
        'user': config.get(section, 'user'),
        'password': config.get(section, 'password'),
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
    return psycopg2.connect(**db_config)


def reinit_table():
    conn = get_connection()
    cursor = conn.cursor()
    try:
        cursor.execute('SELECT counter FROM user_counter WHERE user_id = 1;')
        logger.info("Current counter = %s. Updating to 0...", cursor.fetchone()[0])
        cursor.execute('UPDATE user_counter SET counter = %s WHERE user_id = %s', (0, 1))
        conn.commit()
    finally:
        cursor.close()
        conn.close()


def increment_counter_lost_updates():
    conn = get_connection()
    cursor = conn.cursor()
    try:
        for i in range(10000):
            cursor.execute('SELECT counter FROM user_counter WHERE user_id = 1;')
            result_set = cursor.fetchone()
            counter = result_set[0] + 1
            cursor.execute('UPDATE user_counter SET counter = %s WHERE user_id = %s', (counter, 1))
            conn.commit()
    finally:
        cursor.close()
        conn.close()


def increment_counter_in_place_update():
    conn = get_connection()
    cursor = conn.cursor()
    try:
        for i in range(10000):
            cursor.execute("UPDATE user_counter SET counter = counter + 1 WHERE user_id = 1")
            conn.commit()
    finally:
        cursor.close()
        conn.close()


def increment_counter_row_level_locking():
    conn = get_connection()
    cursor = conn.cursor()
    try:
        for i in range(10000):
            cursor.execute('SELECT counter FROM user_counter WHERE user_id = 1 FOR UPDATE')
            result_set = cursor.fetchone()
            counter = result_set[0] + 1
            cursor.execute('UPDATE user_counter SET counter = %s WHERE user_id = %s', (counter, 1))
            conn.commit()
    finally:
        cursor.close()
        conn.close()


def increment_counter_optimistic_concurrency_control():
    conn = get_connection()
    cursor = conn.cursor()
    try:
        for i in range(10000):
            while True:
                cursor.execute("SELECT counter, version FROM user_counter WHERE user_id = 1")
                (counter, version) = cursor.fetchone()
                counter = counter + 1
                cursor.execute("UPDATE user_counter SET counter = %s, version = %s WHERE user_id = %s AND version = %s",
                               (counter, version + 1, 1, version))
                conn.commit()
                count = cursor.rowcount
                if count > 0:
                    break
    finally:
        cursor.close()
        conn.close()


logger.info("Running scenario with LOST UPDATES")
execute_functions_in_threads(increment_counter_lost_updates)
reinit_table()

logger.info("Running scenario IN PLACE UPDATE")
execute_functions_in_threads(increment_counter_in_place_update)
reinit_table()

logger.info("Running scenario with ROW LEVEL LOCKING")
execute_functions_in_threads(increment_counter_row_level_locking)
reinit_table()

logger.info("Running scenario with OPTIMISTIC CONCURRENCY CONTROL")
execute_functions_in_threads(increment_counter_optimistic_concurrency_control)
reinit_table()
