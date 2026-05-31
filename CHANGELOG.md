# Changelog

## [1.1.1] — 2026-05-31

### Fixed
- Added explicit `devices: [/dev/hidraw0]` in `config.yaml` to ensure the HA
  Supervisor grants cgroup access to the HID device. `full_access: true` alone
  is not sufficient for hidraw devices on some HA OS versions.

## [1.1.0] — 2026-05-31

### Changed
- Each sensor now publishes its value to an individual retained topic
  (`homeassistant/sensor/apc_ups_{id}/state`) instead of a single JSON blob.
  Compatible with `mqtt_statestream`, `mqtt_discoverystream_alt`, and any
  subscriber that uses the standard `{prefix}/{domain}/{entity_id}/state` pattern.
- Discovery config no longer uses `value_template` since each state topic
  carries a single scalar value.
- Availability topic moved to `homeassistant/sensor/apc_ups/availability`.

## [1.0.0] — 2026-05-31

### Initial release
- Reads grid voltage, battery charge %, battery voltage, and UPS status directly from APC USB HID device
- Publishes all sensors to MQTT with Home Assistant Auto Discovery
- Configurable MQTT broker, credentials, and polling interval
- Multi-arch support: `amd64`, `aarch64`, `armv7`
- Reports `offline` availability when the UPS is unreachable
