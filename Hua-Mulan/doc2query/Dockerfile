FROM fastdotai/fastai:latest

RUN apt update 

RUN python3 -m pip install --no-cache-dir --upgrade pip && \
    python3 -m pip install --no-cache-dir \
    transformers 

RUN conda install tensorflow

CMD python doc2query/doc2query.py