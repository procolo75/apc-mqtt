# APC UPS MQTT — Home Assistant App

Home Assistant app that reads data directly from an APC UPS via USB HID and publishes it to MQTT with Home Assistant Auto Discovery.

No `apcupsd` daemon required — the app talks directly to the HID device.

## Supported Hardware

Tested on **APC Back-UPS ES 650G2** (USB HID). Should work with most APC Back-UPS models that expose HID report IDs `0x0C`, `0x31`, and `0x34`.

## Features

- Reads grid voltage, battery charge %, battery voltage, and UPS status via USB HID
- Publishes sensor data to MQTT at a configurable interval
- Registers all sensors automatically in Home Assistant via MQTT Discovery
- Reports `offline` availability when the UPS cannot be read
- Multi-arch support: `amd64`, `aarch64`, `armv7`

## Sensors Published

| Sensor | Unit | Description |
|--------|------|-------------|
| Grid Voltage | V | AC input voltage (0 when on battery) |
| Battery Charge | % | Current battery charge level |
| Battery Voltage | V | Battery terminal voltage |
| UPS Status | — | `online`, `charging`, or `on_battery` |

## Installation

1. In Home Assistant go to **Settings → Apps → Install App → ⋮ → Repositories**
2. Add this repository URL: `https://github.com/procolo75/apc-mqtt`
3. Find **APC UPS MQTT** in the store and click **Install**
4. Go to the **Configuration** tab and fill in your MQTT settings
5. Click **Start**

## Configuration

```yaml
mqtt_host: core-mosquitto   # MQTT broker hostname
mqtt_port: 1883             # MQTT broker port
mqtt_user: ""               # MQTT username (leave empty if not required)
mqtt_password: ""           # MQTT password (leave empty if not required)
poll_interval: 30           # Polling interval in seconds
```

The app requires `full_access: true` to reach `/dev/hidraw0`.

## Updating

Home Assistant checks for new versions automatically. When a new version is available, an **Update** button appears in the app page. Click it to update — no configuration changes are required between releases unless explicitly noted in the [CHANGELOG](CHANGELOG.md).

## MQTT Topics

| Topic | Content |
|-------|---------|
| `apc_ups/state` | JSON with all sensor values |
| `apc_ups/availability` | `online` / `offline` |
| `homeassistant/sensor/apc_ups/<id>/config` | Discovery payloads (retained) |

## Requirements

- Home Assistant OS or Supervised
- APC UPS connected via USB
- Mosquitto broker (or any MQTT broker accessible from the app)

## License

MIT
