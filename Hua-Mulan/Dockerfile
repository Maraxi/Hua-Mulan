FROM python:3.7

RUN mkdir pred
COPY requirements.txt ./pred

RUN pip install --upgrade pip && \
    pip install --no-cache-dir -r /pred/requirements.txt
RUN echo ls
CMD python pred/index.py