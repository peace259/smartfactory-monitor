
from app.core.database import AsyncSessionLocal
from app.services.anomaly_service import AnomalyService
from app.services.alert_service import AlertService

async def check_anomalies():
    async with AsyncSessionLocal() as db:
        anomalies = await AnomalyService(db).detect_anomalies()
        if not anomalies.empty:
            alert_service = AlertService()
            message = f"⚠️ Знайдено {len(anomalies)} аномалій!\n{anomalies[['sensor_id', 'value', 'sensor_type']].to_string()}"
            await alert_service.send_alert(message)
