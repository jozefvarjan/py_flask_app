FROM python:3.14
EXPOSE 5000
WORKDIR /py_flask_app
COPY requirements.txt .
RUN pip install -r requirements.txt
COPY . .
CMD ["flask", "--app", "main", "run", "--host", "0.0.0.0"]


