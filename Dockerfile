FROM python:3.11

WORKDIR /app/
COPY . /app/
RUN pip3 install --no-cache-dir -U pip && pip3 install --no-cache-dir -U -r requirements.txt

CMD bash start
