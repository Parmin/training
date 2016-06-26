FROM python:2.7
RUN easy_install pip
COPY requirements.txt .
COPY search.py .
RUN pip install -r requirements.txt
EXPOSE 8080
CMD [ "python", "search.py" ]
