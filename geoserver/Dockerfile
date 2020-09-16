FROM alpine as downloader

RUN apk add --no-cache wget
RUN wget -q http://sourceforge.net/projects/geoserver/files/GeoServer/2.11.2/extensions/geoserver-2.11.2-importer-plugin.zip -O /importer-plugin.zip

FROM camptocamp/geoserver:jetty-2.11.2
COPY --from=downloader /importer-plugin.zip /importer-plugin.zip
RUN cd /var/lib/jetty/webapps/geoserver/WEB-INF/lib/ && unzip -o /importer-plugin.zip
