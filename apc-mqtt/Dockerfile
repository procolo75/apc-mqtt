ARG BUILD_FROM
FROM $BUILD_FROM

WORKDIR /app

COPY requirements.txt .
RUN pip3 install --no-cache-dir --break-system-packages -r requirements.txt

COPY apc_mqtt.py .
COPY run.sh .
RUN chmod +x run.sh

CMD ["/app/run.sh"]
