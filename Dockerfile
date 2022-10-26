FROM python:3.10

ENV PYTHONBUFFERED=1

WORKDIR /code


COPY Pipfile Pipfile.lock ./


RUN python -m pip install --upgrade pip
RUN pip install pipenv && pipenv install --dev --system --deploy --ignore-pipfile
RUN pipenv install django-dotenv

COPY . .


EXPOSE 8000

CMD ["pipenv","run","python","manage.py","runserver","0.0.0.0:8000"]
