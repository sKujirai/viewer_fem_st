FROM python:3.8.3

ARG WORK_DIR="/work"
ARG DATA_DIR="/data"
ARG STREAMLIT_PORT=8501

RUN pip install --upgrade pip

COPY ./requirements.txt .
RUN pip install  -r requirements.txt

RUN mkdir ${DATA_DIR}

WORKDIR ${WORK_DIR}

EXPOSE ${STREAMLIT_PORT}
