FROM python:3.10

RUN mkdir /usr/src/app
WORKDIR /usr/src/app

RUN pip install pipenv

COPY Pipfile /usr/src/app/Pipfile
COPY Pipfile.lock /usr/src/app/Pipfile.lock

RUN pipenv install --system --dev

ENTRYPOINT ["bash"]
