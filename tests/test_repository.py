from repository import monitoring_repository as repo


def test_save_and_get_latest(monkeypatch, tmp_path):
    monkeypatch.setattr(repo, "_LOCAL_FILE", tmp_path / "history.json")
    monkeypatch.setattr(repo, "_USE_UPSTASH", False)

    results = [
        {"name": "Health", "url": "http://x/health", "status": "ONLINE",
         "status_code": 200, "latency_ms": 10, "error": None, "anomaly_detected": False},
        {"name": "Error", "url": "http://x/error", "status": "ERROR",
         "status_code": 500, "latency_ms": 5, "error": None, "anomaly_detected": False},
    ]

    entry = repo.save_cycle(results)

    assert repo.get_latest() == entry
    assert len(repo.get_history(limit=10)) == 1
    alerts = repo.get_alerts(limit=10)
    assert len(alerts) == 1
    assert alerts[0]["api"] == "Error"


def test_history_respects_limit(monkeypatch, tmp_path):
    monkeypatch.setattr(repo, "_LOCAL_FILE", tmp_path / "history.json")
    monkeypatch.setattr(repo, "_USE_UPSTASH", False)

    for _ in range(3):
        repo.save_cycle([{"name": "A", "url": "http://x", "status": "ONLINE",
                           "status_code": 200, "latency_ms": 1, "error": None,
                           "anomaly_detected": False}])

    assert len(repo.get_history(limit=2)) == 2


def test_throttle_and_incident_recovery(monkeypatch, tmp_path):
    monkeypatch.setattr(repo, "_LOCAL_FILE", tmp_path / "history.json")
    monkeypatch.setattr(repo, "_USE_UPSTASH", False)
    down = [{"name": "A", "url": "http://x", "status": "ERROR"}]
    up = [{"name": "A", "url": "http://x", "status": "ONLINE"}]
    first = repo.save_cycle(down, min_interval=300)
    assert repo.save_cycle(down, min_interval=300) == first
    assert len(repo.get_history()) == 1
    repo.save_cycle(down)
    assert len(repo.get_incidents()) == 1
    assert repo.get_incidents()[0]["resolved_at"] is None
    repo.save_cycle(up)
    incident = repo.get_incidents()[0]
    assert incident["resolved_at"] is not None
    assert incident["duration_seconds"] >= 0
    repo.save_cycle(down)
    assert len(repo.get_incidents()) == 2
