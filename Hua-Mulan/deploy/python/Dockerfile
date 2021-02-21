FROM jupyter/base-notebook:latest

RUN pip install pandas elasticsearch elasticsearch_dsl torch transformers scikit-learn

EXPOSE 8888

CMD ["jupyter", "notebook", "--port=8888", "--allow-root","--no-browser", "--ip=0.0.0.0"]
