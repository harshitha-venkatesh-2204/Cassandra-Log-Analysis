
from cassandra.cluster import Cluster
from collections import Counter

def find_most_hit_path():
    # Connect to the Cassandra cluster
    cluster = Cluster(['10.254.3.108', '10.254.1.207', '10.254.2.126'])
    session = cluster.connect('log_keyspace')

    # Query to get all URLs
    query = "SELECT url FROM log_data_small_log;"
    rows = session.execute(query)

    # Count the occurrences of each URL
    url_counts = Counter(row.url for row in rows)

    # Find the most hit URL
    if url_counts:
        most_hit_url, hit_count = url_counts.most_common(1)[0]
        print(f"Most hit path: {most_hit_url} with {hit_count} hits")
    else:
        print("No data found.")

    # Close the connection
    cluster.shutdown()

if __name__ == '__main__':
    find_most_hit_path()

