FROM python:3.8
MAINTAINER "Cailyn Seymour, cailyn@uoregon.edu"
COPY . /app
WORKDIR /app
RUN pip install -r requirements.txt
ENTRYPOINT ["python"]
CMD ["flask_brevets.py"]
