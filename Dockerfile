# BASE
FROM python:3.9-slim AS base
WORKDIR /app
COPY requirements.txt ./
RUN pip install -r requirements.txt --no-cache-dir

# DEVELOPMENT
FROM base AS development
RUN pip install django-extensions Werkzeug pyOpenSSL
EXPOSE 8000/tcp
ENTRYPOINT ["./manage.py"]
CMD ["runserver_plus", "--key-file", "selftest-key", "--cert-file", "selftest-cert", "0.0.0.0:8000"]

# PRODUCTION
FROM base AS production
COPY . .
CMD ["gunicorn", "--bind", "0.0.0.0:8000", "car_service.wsgi"]
