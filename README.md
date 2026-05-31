# APC UPS MQTT — Home Assistant Add-on

Home Assistant add-on that reads data directly from an APC UPS via USB HID and publishes it to MQTT with Home Assistant Auto Discovery.

No `apcupsd` daemon required — the add-on talks directly to the HID device.

## Supported Hardware

Tested on **APC Back-UPS ES 650G2** (USB HID). Should work with most APC Back-UPS models that expose HID report IDs `0x0C`, `0x31`, and `0x34`.

## Features

- Reads grid voltage, battery charge %, battery voltage, and UPS status via USB HID
- Publishes sensor data to MQTT at a configurable interval
- Registers all sensors automatically in Home Assistant via MQTT Discovery
- Reports `offline` availability when the UPS cannot be read

## Sensors Published

| Sensor | Unit | Description |
|--------|------|-------------|
| Grid Voltage | V | AC input voltage (0 when on battery) |
| Battery Charge | % | Current battery charge level |
| Battery Voltage | V | Battery terminal voltage |
| UPS Status | — | `online`, `charging`, or `on_battery` |

## Installation

1. In Home Assistant, go to **Settings → Add-ons → Add-on Store**
2. Click the three-dot menu → **Repositories**
3. Add this repository URL
4. Find **APC UPS MQTT** and click **Install**

## Configuration

```yaml
mqtt_host: core-mosquitto   # MQTT broker hostname
mqtt_port: 1883             # MQTT broker port
mqtt_user: ""               # MQTT username (leave empty if not required)
mqtt_password: ""           # MQTT password (leave empty if not required)
poll_interval: 30           # Polling interval in seconds
```

The add-on requires `full_access: true` to reach `/dev/hidraw0`.

## MQTT Topics

| Topic | Content |
|-------|---------|
| `apc_ups/state` | JSON with all sensor values |
| `apc_ups/availability` | `online` / `offline` |
| `homeassistant/sensor/apc_ups/<id>/config` | Discovery payloads (retained) |

## Requirements

- Home Assistant OS or Supervised
- APC UPS connected via USB
- Mosquitto broker (or any MQTT broker accessible from the add-on)

## License

MIT
