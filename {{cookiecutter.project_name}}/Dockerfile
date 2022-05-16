FROM python:3.10

ENV WORKDIR_PATH /usr/src/app
ARG USER_CONTAINER
ENV DOCKER 1

RUN mkdir -p $WORKDIR_PATH && chown $USER_CONTAINER:$USER_CONTAINER $WORKDIR_PATH
WORKDIR $WORKDIR_PATH
RUN apt-get update -y && apt-get install vim nano -y && pip install pipenv

COPY --chmod=0444 ./Pipfile* ./
RUN pipenv install --deploy --system --clear

COPY --chmod=0444 . .
RUN find $WORKDIR_PATH -type d -exec chown $USER_CONTAINER:$USER_CONTAINER {} \;
RUN find $WORKDIR_PATH -type d -exec chmod 755 {} \;

USER $USER_CONTAINER
CMD python main.py
