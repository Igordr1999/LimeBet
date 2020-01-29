FROM python:3.7

ENV PYTHONUNBUFFERED 1
RUN mkdir -p /opt/services/djangoapp/src

COPY Pipfile Pipfile.lock /opt/services/djangoapp/src/
WORKDIR /opt/services/djangoapp/src
RUN pip install pipenv && pipenv install --system

COPY . /opt/services/djangoapp/src
RUN cd limebet && python manage.py collectstatic --no-input

EXPOSE 80
CMD ["gunicorn", "-c", "config/gunicorn/conf.py", "--bind", ":80", "--chdir", "limebet", "limebet.wsgi:application"]
