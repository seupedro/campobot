FROM python:3

ENV TIMEZONE_SP=America/Sao_Paulo
RUN ln -snf /usr/share/zoneinfo/$TIMEZONE_SP /etc/localtime && echo $TIMEZONE_SP > /etc/timezone

WORKDIR /usr/src/app

COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt

COPY ./* ./

EXPOSE 443
CMD [ "python", "./main.py" ]
