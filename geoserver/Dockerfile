FROM alpine as downloader

RUN apk add --no-cache wget
WORKDIR /plugins
RUN wget -q http://sourceforge.net/projects/geoserver/files/GeoServer/2.17.2/extensions/geoserver-2.17.2-importer-plugin.zip -O importer-plugin.zip && \
    wget -q https://build.geoserver.org/geoserver/master/community-latest/geoserver-2.19-SNAPSHOT-pgraster-plugin.zip -O pgraster-plugin.zip && \
    wget -q http://sourceforge.net/projects/geoserver/files/GeoServer/2.17.2/extensions/geoserver-2.17.2-imagemosaic-jdbc-plugin.zip -O imagemosaic-jdbc-plugin.zip

FROM camptocamp/geoserver:jetty-2.17

COPY --from=downloader /plugins/ /plugins/
RUN cd /var/lib/jetty/webapps/geoserver/WEB-INF/lib/ && find /plugins/ -name '*zip' -print0 -exec unzip -o {} \;
