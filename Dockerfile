FROM python:latest
LABEL Maintainer="cyclothymia@github"
ADD requirements.txt /
RUN pip install -r requirements.txt
ADD main.py /
CMD [ "python", "./main.py" ]