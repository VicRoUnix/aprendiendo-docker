FROM python:3.7-slim
WORKDIR /app
COPY . /app
RUN pip install -r requirements.txt
EXPOSE 80
ENV MY_APP_VERSION="1.0"
CMD ["python", "app.py"]
