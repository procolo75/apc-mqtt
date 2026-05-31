#!/usr/bin/env python3
import array
import fcntl
import json
import os
import time
import logging
import paho.mqtt.client as mqtt

logging.basicConfig(level=logging.WARNING, format='%(asctime)s [%(levelname)s] %(message)s')
log = logging.getLogger(__name__)

HIDRAW_PATH   = '/dev/hidraw0'
MQTT_HOST     = os.environ.get("MQTT_HOST", "core-mosquitto")
MQTT_PORT     = int(os.environ.get("MQTT_PORT", 1883))
MQTT_USER     = os.environ.get("MQTT_USER", "")
MQTT_PASSWORD = os.environ.get("MQTT_PASSWORD", "")
POLL_INTERVAL = int(os.environ.get("POLL_INTERVAL", 30))

DEVICE_ID     = "apc_ups"
BASE_TOPIC    = "apc_ups"
DISCOVERY_PFX = "homeassistant"

SENSORS = [
    {"id": "input_voltage",   "name": "Grid Voltage",    "unit": "V",   "device_class": "voltage", "icon": "mdi:transmission-tower"},
    {"id": "battery_charge",  "name": "Battery Charge",  "unit": "%",   "device_class": "battery", "icon": "mdi:battery"},
    {"id": "battery_voltage", "name": "Battery Voltage", "unit": "V",   "device_class": "voltage", "icon": "mdi:flash"},
    {"id": "status",          "name": "UPS Status",      "unit": None,  "device_class": None,      "icon": "mdi:power"},
]

# HIDIOCGFEATURE(n) = (3<<30) | (n<<16) | (ord('H')<<8) | 7
def _get_feature(fd, report_id, size=8):
    buf = array.array('B', [report_id] + [0] * (size - 1))
    fcntl.ioctl(fd, (3 << 30) | (size << 16) | (0x48 << 8) | 7, buf, True)
    return list(buf)


def read_ups_data():
    try:
        fd = os.open(HIDRAW_PATH, os.O_RDWR | os.O_NONBLOCK)
        try:
            r31 = _get_feature(fd, 0x31)  # grid voltage (Volts LE16, 0 when on battery)
            r0c = _get_feature(fd, 0x0C)  # battery charge % (r[1], 0-100)
            r34 = _get_feature(fd, 0x34)  # battery voltage (r[1]/10, range 11.5-14.1V)
        finally:
            os.close(fd)
    except PermissionError:
        log.error(f"Permission denied on {HIDRAW_PATH}")
        return {}
    except FileNotFoundError:
        log.error(f"Device {HIDRAW_PATH} not found")
        return {}
    except Exception as e:
        log.error(f"UPS read error: {e}")
        return {}

    input_v  = (r31[2] << 8) | r31[1]
    batt_pct = r0c[1]
    batt_v   = round(r34[1] / 10.0, 1)

    if input_v > 50:
        status = "charging" if batt_pct < 100 else "online"
    else:
        status = "on_battery"

    return {
        "input_voltage":   input_v,
        "battery_charge":  batt_pct,
        "battery_voltage": batt_v,
        "status":          status,
    }


def publish_discovery(client, sensor):
    topic = f"{DISCOVERY_PFX}/sensor/{DEVICE_ID}/{sensor['id']}/config"
    payload = {
        "name": sensor["name"],
        "unique_id": f"{DEVICE_ID}_{sensor['id']}",
        "state_topic": f"{BASE_TOPIC}/state",
        "value_template": f"{{{{ value_json.{sensor['id']} }}}}",
        "availability_topic": f"{BASE_TOPIC}/availability",
        "icon": sensor["icon"],
        "device": {
            "identifiers": [DEVICE_ID],
            "name": "APC Back-UPS",
            "model": "Back-UPS ES 650G2",
            "manufacturer": "APC",
        },
    }
    if sensor["unit"]:
        payload["unit_of_measurement"] = sensor["unit"]
    if sensor["device_class"]:
        payload["device_class"] = sensor["device_class"]
    client.publish(topic, json.dumps(payload), retain=True)


def main():
    client = mqtt.Client(client_id=DEVICE_ID)
    if MQTT_USER:
        client.username_pw_set(MQTT_USER, MQTT_PASSWORD)
    client.will_set(f"{BASE_TOPIC}/availability", "offline", retain=True)

    def on_connect(c, userdata, flags, rc):
        if rc == 0:
            c.publish(f"{BASE_TOPIC}/availability", "online", retain=True)
            for sensor in SENSORS:
                publish_discovery(c, sensor)
        else:
            log.error(f"MQTT connection failed, code: {rc}")

    client.on_connect = on_connect

    while True:
        try:
            client.connect(MQTT_HOST, MQTT_PORT, keepalive=60)
            client.loop_start()
            break
        except Exception as e:
            log.error(f"MQTT unreachable: {e}. Retrying in 10s...")
            time.sleep(10)

    while True:
        try:
            data = read_ups_data()
            if data:
                client.publish(f"{BASE_TOPIC}/state", json.dumps(data), retain=True)
            else:
                client.publish(f"{BASE_TOPIC}/availability", "offline", retain=True)
        except Exception as e:
            log.error(f"Loop error: {e}")
        time.sleep(POLL_INTERVAL)


if __name__ == "__main__":
    main()
