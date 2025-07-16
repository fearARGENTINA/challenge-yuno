FROM python:3.13
RUN mkdir /api
WORKDIR /api
EXPOSE 8080
COPY requirements.txt .
RUN pip install -r requirements.txt
COPY . .
CMD ["python", "app.py"]