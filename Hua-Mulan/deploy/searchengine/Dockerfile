FROM python:3.7

RUN mkdir pred
RUN mkdir start
COPY requirements.txt ./start
COPY ./start_searchengine.sh ./start

RUN pip install --upgrade pip && \
    pip install --no-cache-dir -r /start/requirements.txt

RUN chmod +x /start/start_searchengine.sh

CMD sh ./start/start_searchengine.sh