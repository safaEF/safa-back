FROM python:3.10

ENV PYTHONBUFFERED=1

WORKDIR /code

RUN python -m pip install --upgrade pip
RUN pip install pipenv && pipenv install --dev --system --deploy --ignore-pipfile

COPY . .

EXPOSE 8000

CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]