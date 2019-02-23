FROM python:3.5.1-onbuild


WORKDIR /usr/src/app

# Upgrade pip
RUN pip install --upgrade pip

COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt


COPY . .

CMD python app.py

