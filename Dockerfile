FROM python:3-alpine
WORKDIR /usr/src/app
COPY requirements.txt ./
RUN apk update --no-check-certificate && apk add --no-check-certificate python3-dev gcc libc-dev libffi-dev
RUN pip install -r requirements.txt --trusted-host pypi.org --trusted-host files.pythonhosted.org
COPY . .
EXPOSE 80
CMD ["python", "./app.py"]
