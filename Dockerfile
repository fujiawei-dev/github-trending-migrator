# docker build -t github-trending-api .
# docker run -p 12351:12351 github-trending-api:latest

FROM python

LABEL maintainer="Rustle Karl <rustlekarl@gmail.com>"

WORKDIR /github-trending-api

COPY ./requirements.txt .

RUN pip install --no-cache-dir -r requirements.txt

COPY ./github_trending_migrator ./app

CMD uvicorn app.main:app --host 0.0.0.0 --port=${PORT:-12351}
