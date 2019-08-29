#!/usr/bin/env /python
# -*- coding:utf-8 -*-
"""
 Created by Dai at 2019-08-29.
"""

#!/usr/bin/env /python
# -*- coding:utf-8 -*-
"""
 Created by Dai at 2019-08-26.
"""

"""
    提供spark on hdfs 对hdfs操作的基本api接口
"""
import subprocess
from pyspark import SparkContext, SparkConf
from pyspark.sql import SparkSession

conf = SparkConf().setMaster("local")
conf.set("hive.metastore.uri", "thrift://172.22.0.5:9083")
sc = SparkContext(conf=conf)
sc.setLogLevel("ERROR")
spark = SparkSession.builder \
    .appName("python spark sql") \
    .enableHiveSupport() \
    .getOrCreate()
# spark.conf.set("spark.executor.memory", "2g")
# spark.conf.set("spark.driver.memory", "2g")
# spark.conf.set("spark.sql.broadcastTimeout", 36000)
spark.conf.set("spark.sql.autoBroadcastJoinThreshold", -1)
spark.conf.set("spark.sql.sources.partitionOverwriteMode", "dynamic")

file_system_cache = dict()

class Infrastructure():

    def __init__(self, spark_id):
        self.spark_id = spark_id
        self.hadoop = sc._jvm.org.apache.hadoop

    def delete_file(self, path):
        path = self.hdfs_path(path)
        self.file_system.delete(path)
        # subprocess.call(["hadoop", "fs", "-rm", "-r", "-f", path])

    def hive_sql(self, sql):
        return spark.sql(sql)

    @property
    def file_system(self):
        if self.spark_id not in file_system_cache:
            fs = self.hadoop.fs.FileSystem
            conf = self.hadoop.conf.Configuration()
            conf.set("fs.defaultFS", f"hdfs://{self.spark_id}")

            file_system = fs.get(conf)

            file_system_cache[self.spark_id] = file_system

        file_system = file_system_cache[self.spark_id]

        return file_system

    def hdfs_path(self, path):
        return self.hadoop.fs.Path(path)

    def read_orc(self, file_path):
        return spark.read.orc(file_path)

    def mkdirs(self, path):
        path = self.hdfs_path(path)
        self.file_system.mkdirs(path)
        # subprocess.call(["hadoop", "fs", "-mkdir", path])

    def set_replication(self, path, replication="2"):
        """
            重新设置副本个数

            检查结果命令 hadoop fs -stat %r /flume/gos/src_player/log_date=2019-06-30/*
        :param path:
        :param log_date:
        :return:
        """
        subprocess.call(["hadoop", "dfs", "-setrep", "-R", replication, path])

    def snapshot_dir(self, file_path, snap_name):
        """
            为单天目录添加快照
        :param log_date:
        :param hdfs_path:
        :return:
        """
        # print(Fs.allowSnapshot.__doc__)
        # 开启
        path = self.hdfs_path(file_path)
        self.file_system.allowSnapshot(path)
        # 创建
        self.file_system.createSnapshot(path, snap_name)

    def snapshot_delete(self, file_path, snap_name):
        path = self.hdfs_path(file_path)

        self.file_system.deleteSnapshot(path, snap_name)

    def exists_file(self, path):
        path = self.hdfs_path(path)
        return self.file_system.exists(path)

    def read_parquet(self, path):
        return spark.read.parquet(path)


if __name__ == '__main__':

    spark_id = "172.20.0.2:9000"
    ins = Infrastructure(spark_id)

    ins.mkdirs("/test2")