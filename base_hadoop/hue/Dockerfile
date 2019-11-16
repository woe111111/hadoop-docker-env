FROM gethue/hue


COPY hue.ini /usr/share/hue/desktop/conf/hue.ini

COPY docker-entrypoint.sh /
RUN chmod +x /docker-entrypoint.sh
ENTRYPOINT ["/docker-entrypoint.sh"]

CMD ["./startup.sh", "-n"]
