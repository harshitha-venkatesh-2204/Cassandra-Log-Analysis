from cassandra.cluster import Cluster
from collections import Counter

def find_most_active_ip():
    # Connect to the Cassandra cluster
    cluster = Cluster(['10.254.3.108', '10.254.1.207', '10.254.2.126'])
    session = cluster.connect('log_keyspace')

    # Query to get all IP addresses
    query = "SELECT ip_address FROM log_data_small_log;"
    rows = session.execute(query)

    # Count the occurrences of each IP address
    ip_counts = Counter(row.ip_address for row in rows)

    # Find the IP address with the most accesses
    if ip_counts:
        most_active_ip, access_count = ip_counts.most_common(1)[0]
        print(f"Most active IP: {most_active_ip} with {access_count} accesses")
    else:
        print("No data found.")

    # Close the connection
    cluster.shutdown()

if __name__ == '__main__':
    find_most_active_ip()

