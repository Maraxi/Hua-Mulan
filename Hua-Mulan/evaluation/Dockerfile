FROM jupyter/base-notebook:python-3.7.6

ENV PYTHONUNBUFFERED 1

USER root

RUN apt-get update && apt-get install -y \
    dpkg-dev \
    gcc \
    git \
    curl \
    gnupg

USER jovyan

RUN conda install panel=0.9.7 bokeh=2.1.1 tornado param colorcet holoviews=1.13.3 hvplot=0.6.0 pandas datashader scikit-learn==0.22.1 scipy==1.4.1
RUN pip install trectools

WORKDIR /home/jovyan/work

CMD ["jupyter", "notebook", "--port=8888","--no-browser", "--NotebookApp.iopub_data_rate_limit=10000000","--ip=0.0.0.0"]
