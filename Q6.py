from cassandra.cluster import Cluster

# Connect to the Cassandra cluster
cluster = Cluster(['10.254.3.108', '10.254.1.207', '10.254.2.126'])
session = cluster.connect('log_keyspace')

# Query to get the total number of requests on April 2, 2022
total_requests_query = "SELECT COUNT(*) AS total_requests FROM log_data_small_log WHERE datetime >= '2022-04-02' AND datetime < '2022-04-03'"

# Query to get the number of GET requests on April 2, 2022
get_requests_query = "SELECT COUNT(*) AS get_requests FROM log_data_small_log WHERE datetime >= '2022-04-02' AND datetime < '2022-04-03' AND method = 'GET'"

# Execute the queries
total_requests_result = session.execute(total_requests_query).one()
get_requests_result = session.execute(get_requests_query).one()

# Calculate the ratio of GET requests to total requests
total_requests = total_requests_result['total_requests']
get_requests = get_requests_result['get_requests']
ratio = get_requests / total_requests if total_requests != 0 else 0.0

# Print the ratio
print(f"Ratio of GET requests to total requests on 2022-04-02: {ratio}")

# Close the session and cluster
session.shutdown()
cluster.shutdown()
