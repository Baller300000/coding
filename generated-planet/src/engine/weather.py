"""Weather and environmental systems"""

import random
import math
from ..utils.constants import (
    WEATHER_TYPES, WEATHER_DURATION, WEATHER_CHANGE_CHANCE,
    DAY_LENGTH, NIGHT_BRIGHTNESS, DAY_BRIGHTNESS,
    SEASON_DURATION, SEASONS, SEASON_COLORS,
    BASE_TEMPERATURE, SEASON_TEMPERATURE, WEATHER_TEMPERATURE
)

class WeatherSystem:
    """Manages weather and atmospheric effects"""
    
    def __init__(self):
        self.current_weather = "clear"
        self.weather_timer = 0
        self.time_of_day = 0  # 0-1
        self.season_index = 0
        self.temperature = BASE_TEMPERATURE
        self.humidity = 0.5
    
    def update(self):
        """Update weather and time"""
        self.time_of_day = (self.time_of_day + 1 / DAY_LENGTH) % 1.0
        self.weather_timer += 1
        
        # Weather changes
        if self.weather_timer > WEATHER_DURATION or random.random() < WEATHER_CHANGE_CHANCE:
            self.current_weather = random.choice(WEATHER_TYPES)
            self.weather_timer = 0
            self.humidity = random.uniform(0.5, 1.0) if self.current_weather != "clear" else random.uniform(0.2, 0.6)
        
        # Update temperature
        season = self.get_season()
        season_temp = SEASON_TEMPERATURE.get(season, 20)
        weather_temp = WEATHER_TEMPERATURE.get(self.current_weather, 0)
        self.temperature = season_temp + weather_temp + random.uniform(-1, 1)
    
    def get_brightness(self) -> float:
        """Get current brightness (0-1)"""
        # Brightness varies with time of day
        brightness = math.sin(self.time_of_day * math.pi)
        brightness = NIGHT_BRIGHTNESS + brightness * (DAY_BRIGHTNESS - NIGHT_BRIGHTNESS)
        
        # Weather reduces brightness
        if self.current_weather == "rain":
            brightness *= 0.8
        elif self.current_weather == "snow":
            brightness *= 0.7
        
        return brightness
    
    def get_season(self) -> str:
        """Get current season"""
        season_time = (self.time_of_day * SEASON_DURATION) % (SEASON_DURATION * 4)
        season_idx = int(season_time // SEASON_DURATION)
        return SEASONS[season_idx % len(SEASONS)]
    
    def get_season_color_multiplier(self) -> tuple:
        """Get color multiplier for current season"""
        season = self.get_season()
        return SEASON_COLORS.get(season, (1.0, 1.0, 1.0))
    
    def get_visibility_penalty(self) -> float:
        """Get movement penalty from weather"""
        if self.current_weather == "rain":
            return 0.8
        elif self.current_weather == "snow":
            return 0.6
        return 1.0
    
    def affects_animal_behavior(self) -> dict:
        """Get behavioral modifiers from weather"""
        return {
            "weather": self.current_weather,
            "temperature": self.temperature,
            "visibility": self.get_visibility_penalty(),
            "is_day": self.time_of_day > 0.25 and self.time_of_day < 0.75,
            "brightness": self.get_brightness(),
        }
