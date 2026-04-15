def test_alert_and_anomaly_generation(client, telemetry_points_factory) -> None:
    session_id = client.post(
        "/api/v1/sessions/start",
        json={
            "name": "Hot Session",
            "track_name": "Monza",
            "total_laps": 1,
            "mode": "live",
            "configuration": {"replay_speed": 1.0},
        },
    ).json()["session_id"]

    response = client.post(
        "/api/v1/telemetry/ingest",
        json={"session_id": session_id, "points": telemetry_points_factory(session_id, 1, hot=True)},
    )
    assert response.status_code == 200

    alerts_response = client.get("/api/v1/alerts", params={"session_id": session_id})
    anomalies_response = client.get("/api/v1/anomalies", params={"session_id": session_id})

    assert alerts_response.status_code == 200
    assert anomalies_response.status_code == 200
    assert len(alerts_response.json()) >= 3
    assert len(anomalies_response.json()) >= 1
