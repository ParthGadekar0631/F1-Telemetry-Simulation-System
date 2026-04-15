def test_session_lifecycle_and_history(client, telemetry_points_factory) -> None:
    start_response = client.post(
        "/api/v1/sessions/start",
        json={
            "name": "API Flow Session",
            "track_name": "Monza",
            "total_laps": 2,
            "mode": "live",
            "configuration": {"replay_speed": 2.0},
        },
    )
    assert start_response.status_code == 200
    session_id = start_response.json()["session_id"]

    ingest_response = client.post(
        "/api/v1/telemetry/ingest",
        json={"session_id": session_id, "points": telemetry_points_factory(session_id, 1)},
    )
    assert ingest_response.status_code == 200
    assert ingest_response.json()["ingested"] == 3

    latest_response = client.get(f"/api/v1/telemetry/latest/{session_id}")
    assert latest_response.status_code == 200
    assert latest_response.json()["gear"] == 8

    history_response = client.get(f"/api/v1/telemetry/history/{session_id}", params={"lap_number": 1})
    assert history_response.status_code == 200
    assert len(history_response.json()) == 3

    stop_response = client.post(f"/api/v1/sessions/{session_id}/stop", json={"status": "completed"})
    assert stop_response.status_code == 200
    assert stop_response.json()["status"] == "completed"
