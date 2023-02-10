FROM mysql:5.7.40
ENV MYSQL_DATABASE: "faces"
ENV MYSQL_USER: "adm1n"
ENV MYSQL_PASSWORD: "str0ng_P@sswd_0k"
ENV MYSQL_ROOT_PASSWORD: "snorki"
ENV MYSQL_ALLOW_EMPTY_PASSWORD: "yes"
ADD setup.sql /docker-entrypoint-initdb.d/setup.sql