FROM python:slim-bullseye AS compile-image
ARG APP_INSTALL_FOLDER=/usr/src/app
ENV VENV_PATH=$APP_INSTALL_FOLDER/venv
RUN python -m venv $VENV_PATH
ENV PATH=$VENV_PATH/bin:$PATH \
    CFLAGS=-fcommon
COPY requirements.txt .
ENV VENV_PIP_ALIAS=$VENV_PATH/bin/pip3
RUN $VENV_PIP_ALIAS install --upgrade pip &&\
    $VENV_PIP_ALIAS install -r requirements.txt
COPY lib/. $APP_INSTALL_FOLDER

FROM python:slim-bullseye AS build-image
ARG APP_INSTALL_FOLDER=/usr/src/app
ENV PATH=$APP_INSTALL_FOLDER/venv/bin:$APP_INSTALL_FOLDER/venv/lib/python3.10/site-packages/:$PATH
WORKDIR $APP_INSTALL_FOLDER
COPY --from=compile-image $APP_INSTALL_FOLDER $APP_INSTALL_FOLDER
ENTRYPOINT ["python3", "main.py"]
