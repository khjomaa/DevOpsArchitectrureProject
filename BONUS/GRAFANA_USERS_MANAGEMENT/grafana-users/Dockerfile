FROM python:3.7.4-stretch
RUN groupadd -r app && useradd --no-log-init -r -g app pythonuser
RUN mkdir /app && chown -R pythonuser /app
WORKDIR /app
COPY . /app
RUN pip install --upgrade pip
RUN pip install -r requirements.txt
USER pythonuser
ENTRYPOINT ["python"]
CMD ["run.py"]