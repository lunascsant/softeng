FROM python:3.11-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir --trusted-host files.pythonhosted.org --trusted-host pypi.org --trusted-host pypi.python.org -r requirements.txt
COPY . .

ENV FLASK_APP=main.py
ENV FLASK_ENV=production
ENV MONGO_URI=mongodb://mongodb:27017/moradiapp

EXPOSE 5000

CMD ["gunicorn", "--bind", "0.0.0.0:5000", "main:app"]