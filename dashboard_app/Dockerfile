FROM python:3

WORKDIR /app

COPY dashboard_app/requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt

COPY dashboard_app/ ./

EXPOSE 8050

CMD ["python3", "dashboard.py"]

