FROM python:3.7.5-alpine3.10
RUN adduser -D pythonuser && mkdir /app && chown -R pythonuser /app
COPY requirements.txt /app
COPY words_counter.py /app
WORKDIR /app
RUN pip install --upgrade pip
RUN pip install -r requirements.txt
USER pythonuser
CMD ["python", "/app/words_counter.py"]