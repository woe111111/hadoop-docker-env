FROM woe1997/hbase-base-2.0.6:1.0

ENV PHOENIX_VERSION 5.0.0

ENV PHOENIX_URL http://mirror.bit.edu.cn/apache/phoenix/apache-phoenix-$PHOENIX_VERSION-HBase-2.0/bin/apache-phoenix-$PHOENIX_VERSION-HBase-2.0-bin.tar.gz

RUN set -x \
    && curl -fSL "$PHOENIX_URL" -o /tmp/phoenix.tar.gz \
    && tar -xvf /tmp/phoenix.tar.gz -C /opt/ \
    && rm /tmp/phoenix.tar.gz*

RUN cp -a /opt/apache-phoenix-$PHOENIX_VERSION-HBase-2.0-bin/phoenix-core-$PHOENIX_VERSION-HBase-2.0.jar /opt/apache-phoenix-$PHOENIX_VERSION-HBase-2.0-bin/phoenix-$PHOENIX_VERSION-HBase-2.0-server.jar /opt/hbase-$HBASE_VERSION/lib/

COPY run.sh /run.sh
RUN chmod +x /run.sh

EXPOSE 8765

CMD ["/run.sh"]