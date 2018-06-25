FROM python:3.6-alpine

RUN mkdir /install
WORKDIR /install

COPY requirements.txt requirements.txt
RUN pip install -r requirements.txt

COPY custom_class .
RUN pip install vsearch-1.0.tar.gz

WORKDIR /install/mysql
RUN python setup.py install

WORKDIR /app

RUN rm -rf /install

EXPOSE 80

# CMD ["sleep", "1000000"]
CMD ["python", "vsearch4web.py"]
# CMD ["python", "quick-session.py"]
# CMD ["python", "simple_webapp.py"]



