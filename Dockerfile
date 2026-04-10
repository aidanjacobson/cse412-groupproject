
# backend stage
FROM python:3.12

WORKDIR /app

COPY . .

RUN pip install -r backend/requirements.txt

EXPOSE 8080

CMD ["python", "backend/main.py"]