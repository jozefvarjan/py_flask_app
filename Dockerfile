FROM python:3.14
EXPOSE 5001
WORKDIR /py_flask_app
RUN pip install flask
COPY . .
CMD ["flask", "--app", "main", "run", "--host", "0.0.0.0"]


