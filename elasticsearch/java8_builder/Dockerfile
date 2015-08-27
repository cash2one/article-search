FROM ubuntu:14.04
MAINTAINER "Bijia Lan <lbj.world@gmail.com>"

COPY sources.list /etc/apt/
RUN apt-get update \
	&& apt-get -y install vim wget \
	&& rm -rf /var/lib/apt/lists/*

# install JDK
ENV JAVA_JDK_VERSION 8u60
ENV JAVA_JDK_FILE jdk-$JAVA_JDK_VERSION-linux-x64.tar.gz
RUN mkdir -p /opt/jvm && cd /opt/jvm \
        && wget --no-check-certificate --no-cookies --header "Cookie: oraclelicense=accept-securebackup-cookie" http://download.oracle.com/otn-pub/java/jdk/$JAVA_JDK_VERSION-b27/$JAVA_JDK_FILE \
        && tar zxf $JAVA_JDK_FILE \
        && rm $JAVA_JDK_FILE \
        && mv `ls | grep jdk` /usr/lib/jvm
ENV JAVA_HOME /usr/lib/jvm

# install MAVEN
ENV MAVEN_VERSION 3.0.5
ENV MAVEN_FILE apache-maven-$MAVEN_VERSION-bin.tar.gz
RUN cd /opt \
        && wget http://mirrors.hust.edu.cn/apache/maven/maven-3/$MAVEN_VERSION/binaries/$MAVEN_FILE \
        && tar zxf $MAVEN_FILE \
        && rm $MAVEN_FILE \
        && mv /opt/apache-maven-$MAVEN_VERSION /opt/maven
ENV MAVEN_HOME /opt/maven
        
# setup envs
ENV JRE_HOME $JAVA_HOME/jre
ENV CLASSPATH $JRE_HOME/lib:$CLASSPATH
ENV PATH $JAVA_HOME/bin:$JRE_HOME/bin:$MAVEN_HOME/bin:$PATH

WORKDIR /tmp/build

VOLUME /tmp/build

CMD ["/bin/bash"]
