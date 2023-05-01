FROM python:alpine3.16
COPY ./requirements.txt /app/requirements.txt
RUN python -m pip install -r /app/requirements.txt
COPY . /app
RUN rm -rf /app/.env
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]





