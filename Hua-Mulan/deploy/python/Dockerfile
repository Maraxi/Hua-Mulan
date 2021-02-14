FROM jupyter/base-notebook:latest

RUN pip install pandas elasticsearch elasticsearch_dsl

EXPOSE 8888

CMD ["jupyter", "notebook", "--port=8888", "--allow-root","--no-browser", "--ip=0.0.0.0"]

