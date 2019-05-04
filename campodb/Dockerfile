FROM mongo:4

ENV TIMEZONE_SP=America/Sao_Paulo
RUN ln -snf /usr/share/zoneinfo/$TIMEZONE_SP /etc/localtime && echo $TIMEZONE_SP > /etc/timezone