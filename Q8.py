from cassandra.cluster import Cluster
from collections import Counter

def list_ips_with_404_requests():
    # Connect to your Cassandra cluster
    cluster = Cluster([''10.254.3.108', '10.254.1.207', '10.254.2.126''])
    session = cluster.connect('log_keyspace')

    # Query to get all 404 requests
    query = "SELECT ip_address FROM log_data_small_log WHERE status_code = 404;"
    rows = session.execute(query)

    # Count the occurrences of each IP address
    ip_counts = Counter(row.ip_address for row in rows)

    # Find IPs with more than ten 404 requests
    ips_with_more_than_ten_404 = [ip for ip, count in ip_counts.items() if count > 10]

    # Print the result
    if ips_with_more_than_ten_404:
        print("IPs with more than ten 404 requests:")
        for ip in ips_with_more_than_ten_404:
            print(f"{ip}: {ip_counts[ip]} requests")
    else:
        most_404_ip = ip_counts.most_common(1)[0]
        print(f"No IP has more than ten 404 requests. The IP with the most 404 requests is {most_404_ip[0]} with {most_404_ip[1]} requests.")

    # Close the connection
    cluster.shutdown()

if __name__ == '__main__':
    list_ips_with_404_requests()
