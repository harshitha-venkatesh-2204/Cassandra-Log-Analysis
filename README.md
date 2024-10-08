# Cassandra-Log-Analysis

## Part 1: Setting Up Cassandra 🚀


1. Installation Steps

   - Install Java 8:

```bash
sudo apt-get update
sudo apt-get install openjdk-8-jdk
java -version
```

  - Install Python 3 (if not already installed):

```bash
sudo apt-get update
sudo apt-get install python3
python3 --version
```

- Add Cassandra Repository:

```bash
echo "deb https://debian.cassandra.apache.org 41x main" | sudo tee -a /etc/apt/sources.list.d/cassandra.sources.list
```

- Add Apache Cassandra Keys:

```bash
curl https://downloads.apache.org/cassandra/KEYS | sudo apt-key add -
```

- Update Package Repository:

```bash
sudo apt-get update
```

- Install Cassandra:

```bash
sudo apt-get install cassandra
```


2.  Configuration

- Edit cassandra.yaml:

```bash
sudo nano /etc/cassandra/cassandra.yaml
```

- Update the following configurations for each node:

```bash
seeds: "10.254.3.108,10.254.1.207,10.254.2.126"
listen_address: <Current_Node_IP>
rpc_address: <Current_Node_IP>
```

3. Starting Cassandra Service
   
  Stop and Start Cassandra Service:

```bash
sudo service cassandra stop
sudo service cassandra start
```

5. Monitoring and Verification

 - Check Cluster Status:

   ```bash
    nodetool status
   ```
   
  - Start CQL Client:

    ```bash
    cqlsh 10.254.3.108
    ```

5. Test the Setup

 - Setting Up Keyspace and Table:

   ```bash
   CREATE KEYSPACE patient WITH replication = {'class': 'SimpleStrategy', 'replication_factor': 1};
   CREATE TABLE patient.exam (patient_id int, id int, date timeuuid, details text, PRIMARY KEY (patient_id, id));
   ```

- Importing Data:

```bash
   INSERT INTO exam (patient_id, id, date, details) VALUES (1, 1, now(), 'first exam patient 1');
   INSERT INTO exam (patient_id, id, date, details) VALUES (1, 2, now(), 'second exam patient 1');
 ```

- Verifying Data:

```bash
SELECT * FROM exam WHERE patient_id=1;
```


## Part 2: Import Data into Cassandra 📥


1. Download Log Data Set


3. Create a Keyspace and Table

```bash
CREATE KEYSPACE log_keyspace WITH replication = {'class': 'SimpleStrategy', 'replication_factor': 1};
CREATE TABLE IF NOT EXISTS log_data_small_log (
    id UUID PRIMARY KEY,
    ip_address TEXT,
    datetime TIMESTAMP,
    method TEXT,
    url TEXT,
    protocol TEXT,
    status_code INT,
    response_size INT,
    user_agent TEXT
);
```

4. Import Data Using DSBulk
   
Ensure the CSV file is placed in an accessible location, then run:

```bash
/home/ubuntu/Log_data/dsbulk-1.11.0/bin/dsbulk load -k log_keyspace -t log_data_small_log -url /home/ubuntu/Log_data/output_log_file_New.csv -header true -f dsbulk.conf -h 10.254.3.108 --port 9042
```

5. Verify Data

```bash
SELECT * FROM log_data_small_log LIMIT 20;
```


Part 3: Operate Data in Cassandra 📊


1. Install DataStax Python Driver

```bash
pip install cassandra-driver
```

2. Python Script to Analyze Access Logs
   
Create a script named python_code_x.py and include the following code snippets.
Example Queries:

Hits to a Specific Item:

```bash
from cassandra.cluster import Cluster

def hits_to_admin():
    cluster = Cluster(['10.254.3.108'])
    session = cluster.connect('log_keyspace')
    query = "SELECT COUNT(*) FROM log_data_small_log WHERE url='/administrator/index.php';"
    result = session.execute(query)
    print(f"Hits to '/administrator/index.php': {result[0].count}")

if __name__ == '__main__':
    hits_to_admin()
```


Hits from a Specific IP:

```bash
def hits_from_ip(ip):
    cluster = Cluster(['10.254.3.108'])
    session = cluster.connect('log_keyspace')
    query = f"SELECT COUNT(*) FROM log_data_small_log WHERE ip_address='{ip}';"
    result = session.execute(query)
    print(f"Hits from {ip}: {result[0].count}")

if __name__ == '__main__':
    hits_from_ip('96.32.128.5')
```

Most Hit Path:

```bash
from collections import Counter

def most_hit_path():
    cluster = Cluster(['10.254.3.108'])
    session = cluster.connect('log_keyspace')
    query = "SELECT url FROM log_data_small_log;"
    rows = session.execute(query)

    url_counts = Counter(row.url for row in rows)
    most_hit = url_counts.most_common(1)
    print(f"Most hit path: {most_hit[0][0]} with {most_hit[0][1]} hits" if most_hit else "No data found.")

if __name__ == '__main__':
    most_hit_path()
```


Most Active IP:

```bash
def most_active_ip():
    cluster = Cluster(['10.254.3.108'])
    session = cluster.connect('log_keyspace')
    query = "SELECT ip_address FROM log_data_small_log;"
    rows = session.execute(query)

    ip_counts = Counter(row.ip_address for row in rows)
    most_active = ip_counts.most_common(1)
    print(f"Most active IP: {most_active[0][0]} with {most_active[0][1]} accesses" if most_active else "No data found.")

if __name__ == '__main__':
    most_active_ip()
```


Count Accesses by Firefox:

```bash
def count_firefox_accesses():
    cluster = Cluster(['10.254.3.108'])
    session = cluster.connect('log_keyspace')
    query = "SELECT COUNT(*) FROM log_data_small_log WHERE user_agent LIKE '%Firefox%';"
    result = session.execute(query)
    print(f"Firefox accesses: {result[0].count}")

if __name__ == '__main__':
    count_firefox_accesses()

```

Conclusion
This documentation serves as a comprehensive guide for setting up a Cassandra cluster, importing log data, and analyzing access logs through various queries. Ensure that your report includes any screenshots and outputs from your commands for verification.
