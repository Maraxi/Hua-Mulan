FROM python:3.7

RUN mkdir pred
COPY requirements.txt ./pred
COPY start_searchengine.sh ./pred

RUN pip install --upgrade pip && \
    pip install --no-cache-dir -r /pred/requirements.txt

RUN chmod +x /pred/start_searchengine.sh


CMD sh ./pred/start_searchengine.sh