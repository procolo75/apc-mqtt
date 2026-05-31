# Changelog

## [1.0.0] — 2026-05-31

### Initial release
- Reads grid voltage, battery charge %, battery voltage, and UPS status directly from APC USB HID device
- Publishes all sensors to MQTT with Home Assistant Auto Discovery
- Configurable MQTT broker, credentials, and polling interval
- Multi-arch support: `amd64`, `aarch64`, `armv7`
- Reports `offline` availability when the UPS is unreachable
