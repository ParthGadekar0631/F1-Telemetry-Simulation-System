def test_lap_and_sector_comparisons(client, telemetry_points_factory) -> None:
    session_id = client.post(
        "/api/v1/sessions/start",
        json={
            "name": "Comparison Session",
            "track_name": "Monza",
            "total_laps": 2,
            "mode": "live",
            "configuration": {"replay_speed": 1.0},
        },
    ).json()["session_id"]

    client.post("/api/v1/telemetry/ingest", json={"session_id": session_id, "points": telemetry_points_factory(session_id, 1)})
    client.post("/api/v1/telemetry/ingest", json={"session_id": session_id, "points": telemetry_points_factory(session_id, 2, offset_seconds=10)})
    client.post(f"/api/v1/sessions/{session_id}/stop", json={"status": "completed"})

    summary_response = client.get(f"/api/v1/analytics/sessions/{session_id}/summary")
    comparison_response = client.get(
        f"/api/v1/analytics/sessions/{session_id}/laps/compare",
        params={"lap_a": 1, "lap_b": 2},
    )
    sector_response = client.get(
        f"/api/v1/analytics/sessions/{session_id}/sectors/compare",
        params={"lap_a": 1, "lap_b": 2},
    )

    assert summary_response.status_code == 200
    assert len(summary_response.json()["lap_summaries"]) == 2
    assert comparison_response.status_code == 200
    assert sector_response.status_code == 200
    assert len(sector_response.json()) == 3
