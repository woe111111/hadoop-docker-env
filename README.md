# hadoop-docker-env
This is a Hadoop eco-family bucket containing the use of hdfs hive hbase phoiex base on https://github.com/big-data-europe/docker-hadoop .  The debugging environment of hbase hive phoenix hdfs can be easily owned by docker


### Operating system support
#### Ubuntu
```shell
  docker-compose up -d
```

#### mac
Because the container is not built directly on the host
So it should base on openvpn to proxy 。
Thank for https://github.com/wojas/docker-mac-network
you can set /help/run.sh and run the docker-compose in the project
```shell
#!/bin/sh

dest=${dest:-docker.ovpn}

if [ ! -f "/local/$dest" ]; then
    echo "*** REGENERATING ALL CONFIGS ***"
    set -ex
    #rm -rf /etc/openvpn/*
    ovpn_genconfig -u tcp://localhost
    sed -i 's|^push|#push|' /etc/openvpn/openvpn.conf
    echo localhost | ovpn_initpki nopass
    easyrsa build-client-full host nopass
    ovpn_getclient host | sed '
    	s|localhost 1194|localhost 13194|;
	s|redirect-gateway.*|route 172.30.0.0 255.255.0.0|;
    ' > "/local/$dest"
fi

# Workaround for https://github.com/wojas/docker-mac-network/issues/6
/sbin/iptables -I FORWARD 1 -i tun+ -j ACCEPT

exec ovpn_run
```

if you install success you can ping the ip inside in container 
then
```sql
docker-compose up -d 
```

#### change conf
```conf
vim docer-for-mac.ovpn

comp-lzo yes   # add

```
```conf
vim ／config／openvpn.conf

comp-lzo yes  # change
```

### ENV
```
HADOOP 2.7.7
HIVE 2.3.6 
POSTGRES 9.4 AS METASTORE
HBASE 2.0.6
PHOENIX 5.0.0
```

### 添加地址解析
```
vim /etc/hosts

172.30.0.2 namenode
172.30.0.3 datenode
172.30.0.4 hive-server
172.30.0.5 hive-metastore
172.30.0.6 hive-metastore-postgresql
172.30.0.7 hbase
172.30.0.8 hue
```

### use
```.env
web_hdfs http://namenode:50070
default_fs hdfs://namenode:9000
hive_metastore_uris http://hive-metastore:9083
hive_server_jdb http://hive-server:10000
hbase_regionserver_info http://hbase:1603065
phoenix_query_server http://hbase:8765
```

### Pyspark Demo
```python

from __future__ import print_function

from pyspark import SparkContext, SparkConf
from pyspark.sql import SparkSession
from pyspark.sql import Row
conf = SparkConf().setMaster("local[4]")


## 配置hive 的 matestore地址 让spark.sql可以访问到测试集群的hive
conf.set("hive.metastore.uris", "thrift://hive-metastore:9083")
sc = SparkContext(conf=conf)
sc.setLogLevel("error")
spark = SparkSession.builder.appName("python spark examp").enableHiveSupport().getOrCreate()


def create():
    df = spark.sql("""SHOW TABLES""")
    df.show()
    spark.sql("""CREATE TABLE IF NOT EXISTS helloword (name STRING, age INT)""")

def insert():
    df = sc.parallelize([Row(name="h", age=20)]).toDF()
    df.printSchema()
    df.show()
    df.registerTempTable("temp")
    spark.sql("INSERT INTO TABLE helloword SELECT name,age FROM temp")
    spark.catalog.dropTempView("temp")


def get():
    df = spark.sql("select * from helloword")
    # print("num of recoder is %s" % df.count())
    df.show()


if __name__ == "__main__":

    df = spark.sql("SHOW DATABASES")

    create()
    insert()
    get()
    df.write.mode("overwrite").orc("hdfs://namenode:9000/test")

    spark.stop()

```

