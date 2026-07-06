FROM python:3.14
EXPOSE 5000
WORKDIR /py_flask_app
RUN pip install flask
COPY . .
RUN pip install -r requirements.txt
CMD ["flask", "--app", "main", "run", "--host", "0.0.0.0"]


