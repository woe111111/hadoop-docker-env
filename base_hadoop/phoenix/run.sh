#!/bin/bash

/opt/hbase-$HBASE_VERSION/bin/start-hbase.sh

opt/apache-phoenix-5.0.0-HBase-2.0-bin/bin/queryserver.py
