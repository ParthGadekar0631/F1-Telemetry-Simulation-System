from datetime import datetime

from pydantic import BaseModel, ConfigDict


class AlertResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    session_id: str
    lap_number: int | None = None
    timestamp: datetime
    severity: str
    category: str
    message: str
    metric_name: str
    metric_value: float
    threshold_value: float


class AnomalyResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    session_id: str
    lap_number: int | None = None
    timestamp: datetime
    anomaly_type: str
    description: str
    metric_name: str
    metric_value: float
    reference_value: float
    magnitude: float
