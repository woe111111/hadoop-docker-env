# hadoop-docker-env
This is a Hadoop eco-family bucket containing the use of hdfs hive hbase phoiex base on https://github.com/big-data-europe/docker-hadoop .  The debugging environment of hbase hive phoenix hdfs can be easily owned by docker



### start up  
```shell
  docker-compose up -d
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


