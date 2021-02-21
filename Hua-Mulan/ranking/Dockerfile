FROM fastdotai/fastai:latest

RUN apt update

RUN python3 -m pip install --no-cache-dir --upgrade pip && \
    python3 -m pip install --no-cache-dir \
    transformers
RUN python3 -m pip install flask

RUN python3 -m pip install SentencePiece

RUN conda install tensorflow

CMD python ranking.py