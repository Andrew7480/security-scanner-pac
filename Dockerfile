FROM python:3.10

WORKDIR /app

COPY . .

RUN pip install flask

CMD ["python", "scanner/scanner.py", "./test_project"]
