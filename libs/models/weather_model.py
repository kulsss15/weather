from sqlalchemy import Column, Integer, String, Float, DateTime, func
from apps.weather_service.db.base import Base

class WeatherData(Base):
    """
    Model representing weather data for a city.
    Stores city name, temperature, condition, and timestamps.
    """
    __tablename__ = "weather_data"

    id = Column(Integer, primary_key=True, index=True)
    city = Column(String(100), index=True, nullable=False)  # Max length of 100
    temperature = Column(Float, nullable=False)  # Ensure temperature is required
    condition = Column(String(50), nullable=False)  # Max length of 50
    created_at = Column(DateTime(timezone=True), server_default=func.now(), nullable=False)
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())

    def __repr__(self) -> str:
        return f"<WeatherData(city={self.city}, temperature={self.temperature}, condition={self.condition})>"

