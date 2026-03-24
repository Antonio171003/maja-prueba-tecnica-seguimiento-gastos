FROM python:3.10-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

EXPOSE 5000

CMD python -c "from app import create_app; from app.extensions import db; app = create_app(); app.app_context().push(); db.create_all()" && python seed.py && flask --app run run --host=0.0.0.0