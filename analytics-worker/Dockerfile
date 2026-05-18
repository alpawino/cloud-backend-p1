FROM python:3.9-slim
WORKDIR /app
RUN pip install pandas sqlalchemy pymysql psycopg2-binary boto3 pymongo
COPY ingesta_final.py .
CMD ["python", "ingesta_final.py"]
