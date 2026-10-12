import pathlib
import yaml

ROOT = pathlib.Path(__file__).resolve().parents[1]
CFG = yaml.safe_load((ROOT / "addons/zigbee2mqtt/configuration.yaml").read_text())


def test_permit_join_disabled():
    assert CFG["permit_join"] is False


def test_tcp_ember_adapter():
    assert CFG["serial"]["adapter"] == "ember"
    assert CFG["serial"]["port"].startswith("tcp://")


def test_security_defaults():
    assert CFG["advanced"]["network_key"] == "GENERATE"
    assert CFG["advanced"]["pan_id"] == "GENERATE"
    assert CFG["advanced"]["channel"] in (15, 20, 25)


def test_ha_discovery_and_availability():
    assert CFG["homeassistant"]["enabled"] is True
    assert CFG["availability"]["enabled"] is True
