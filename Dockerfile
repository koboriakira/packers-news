FROM python:3.8.5-slim

WORKDIR /work

ADD packers_news /work/packers_news
ADD Pipfile /work/Pipfile
ADD Pipfile.lock /work/Pipfile.lock
RUN pip install --upgrade pip && \
  pip install --no-cache-dir pipenv && \
  pipenv lock -r > requirements.txt && \
  pip install --no-cache-dir -r requirements.txt

CMD ["uvicorn","packers_news.main:app","--host","0.0.0.0","--port","8080"]
