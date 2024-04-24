FROM python:3.12

WORKDIR /opt/app

ENV PYTHONPATH="${PYTHONPATH}:/opt/app"

COPY requirements.txt requirements.txt
RUN pip install --upgrade pip --no-cache-dir \
    && pip install -r requirements.txt --no-cache-dir

COPY . .

EXPOSE 8000

ENTRYPOINT ["gunicorn", "-w", "4", "-k", "uvicorn.workers.UvicornWorker", "--bind", "0.0.0.0:8000", "src.main:app"]
