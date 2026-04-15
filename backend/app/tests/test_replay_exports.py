def test_replay_and_exports(client, telemetry_points_factory) -> None:
    session_id = client.post(
        "/api/v1/sessions/start",
        json={
            "name": "Replay Session",
            "track_name": "Monza",
            "total_laps": 1,
            "mode": "replay",
            "configuration": {"replay_speed": 1.5},
        },
    ).json()["session_id"]

    client.post("/api/v1/telemetry/ingest", json={"session_id": session_id, "points": telemetry_points_factory(session_id, 1)})
    client.post(f"/api/v1/sessions/{session_id}/stop", json={"status": "completed"})

    replay_metadata = client.get(f"/api/v1/replay/{session_id}")
    replay_lap = client.get(f"/api/v1/replay/{session_id}/laps/1")
    csv_export = client.get(f"/api/v1/exports/{session_id}", params={"format": "csv"})
    json_export = client.get(f"/api/v1/exports/{session_id}", params={"format": "json"})

    assert replay_metadata.status_code == 200
    assert replay_lap.status_code == 200
    assert len(replay_lap.json()["points"]) == 3
    assert csv_export.status_code == 200
    assert "text/csv" in csv_export.headers["content-type"]
    assert json_export.status_code == 200
    assert "application/json" in json_export.headers["content-type"]
