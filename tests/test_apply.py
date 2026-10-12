import pathlib
import subprocess

ROOT = pathlib.Path(__file__).resolve().parents[1]
APPLY = ROOT / "scripts/apply.sh"


def run(cfg):
    return subprocess.run(["sh", str(APPLY)], env={"HA_CONFIG": str(cfg), "PATH": "/usr/bin:/bin"},
                          capture_output=True, text=True)


def test_copies_config_and_z2m_on_fresh_box(tmp_path):
    r = run(tmp_path)
    assert r.returncode == 0, r.stderr
    assert (tmp_path / "configuration.yaml").read_text() == (ROOT / "config/configuration.yaml").read_text()
    assert (tmp_path / "packages/notifications.yaml").exists()
    assert (tmp_path / "dashboards/security.yaml").exists()
    assert (tmp_path / "automations.yaml").exists()
    assert "GENERATE" in (tmp_path / "zigbee2mqtt/configuration.yaml").read_text()


def test_never_overwrites_initialised_z2m(tmp_path):
    run(tmp_path)
    z = tmp_path / "zigbee2mqtt/configuration.yaml"
    z.write_text("network_key: [1, 2, 3]\n")
    r = run(tmp_path)
    assert r.returncode == 0, r.stderr
    assert z.read_text() == "network_key: [1, 2, 3]\n"
    assert "not touching" in r.stdout


def test_preserves_existing_ui_automations(tmp_path):
    (tmp_path / "automations.yaml").write_text("- id: keep\n")
    run(tmp_path)
    assert (tmp_path / "automations.yaml").read_text() == "- id: keep\n"


def test_never_copies_secrets_example_as_secrets(tmp_path):
    run(tmp_path)
    assert not (tmp_path / "secrets.yaml").exists()
