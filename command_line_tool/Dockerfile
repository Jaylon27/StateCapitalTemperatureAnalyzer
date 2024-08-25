FROM python:3.9.19-bullseye

WORKDIR /app

COPY command_line_tool/requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt

COPY command_line_tool/ ./

CMD ["python3", "main.py"]
