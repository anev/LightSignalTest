FROM python:2.7

WORKDIR /app
ADD . /app

RUN pip install -r requirements.txt
EXPOSE 5000 

# Environment Variables
#ENV NAME World

CMD ["python", "Light.py"]
