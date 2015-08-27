FROM java:8-jre
MAINTAINER "Bijia Lan <lbj.world@gmail.com>"

# grab gosu for easy step-down from root
RUN gpg --keyserver ha.pool.sks-keyservers.net --recv-keys B42F6819007F00F88E364FD4036A9C25BF357DD4
RUN arch="$(dpkg --print-architecture)" \
	&& set -x \
	&& curl -o /usr/local/bin/gosu -fSL "https://github.com/tianon/gosu/releases/download/1.3/gosu-$arch" \
	&& curl -o /usr/local/bin/gosu.asc -fSL "https://github.com/tianon/gosu/releases/download/1.3/gosu-$arch.asc" \
	&& gpg --verify /usr/local/bin/gosu.asc \
	&& rm /usr/local/bin/gosu.asc \
	&& chmod +x /usr/local/bin/gosu

RUN apt-key adv --keyserver ha.pool.sks-keyservers.net --recv-keys 46095ACC8548582C1A2699A9D27D666CD88E42B4

ENV ELASTICSEARCH_MAJOR 1.7
ENV ELASTICSEARCH_VERSION 1.7.0

RUN echo "deb http://packages.elasticsearch.org/elasticsearch/$ELASTICSEARCH_MAJOR/debian stable main" > /etc/apt/sources.list.d/elasticsearch.list

RUN set -x \
	&& apt-get update \
        && apt-get install -y redis-server \
	&& apt-get install -y --no-install-recommends elasticsearch=$ELASTICSEARCH_VERSION \
        && apt-get install -y vim \
	&& rm -rf /var/lib/apt/lists/*

# install basic plugins
RUN cd /usr/share/elasticsearch \
    && bin/plugin --install mobz/elasticsearch-head \
    && bin/plugin --install lukas-vlcek/bigdesk

ENV PATH /usr/share/elasticsearch/bin:$PATH
# install other plugins
COPY plugins /usr/share/elasticsearch/plugins

# copy configs
COPY config /usr/share/elasticsearch/config
COPY config/* /etc/elasticsearch/


VOLUME /usr/share/elasticsearch/data

COPY docker-entrypoint.sh /

ENTRYPOINT ["/docker-entrypoint.sh"]

EXPOSE 9200 9300

CMD ["elasticsearch"]
