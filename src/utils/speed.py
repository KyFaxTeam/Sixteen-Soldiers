import math


class GameSpeed:
    """Manages game speed and calculates appropriate delay times with improved scaling"""
    
    def __init__(self, base_delay=1.0, current_speed=1.5, min_speed=0.5, max_speed=2.5):
        """
        Initialize the speed manager with improved defaults
        
        Args:
            base_delay (float): Base delay time in seconds
            current_speed (float): Initial speed setting (1.5 is normal speed)
            min_speed (float): Minimum speed multiplier (0.5 for slowest)
            max_speed (float): Maximum speed multiplier (2.5 for fastest)
        """
        self.base_delay = base_delay
        self.min_speed = min_speed
        self.max_speed = max_speed
        self.current_speed = current_speed
        self._set_min_max_delay()
        
        # # Constants for delay calculation
        # self.MIN_VISIBLE_DELAY = 500  # Minimum delay in milliseconds
        # self.MAX_VISIBLE_DELAY = 4000  # Maximum delay in milliseconds
        self.BASELINE_THINKING_TIME = 1000  # Baseline AI thinking time in milliseconds
        
    def set_speed(self, slider_value):
        """Set speed based on slider value"""
        self.current_speed = max(self.min_speed, min(slider_value, self.max_speed))
        self._set_min_max_delay()

    def _set_min_max_delay(self): 
        
        if 0.5 <= self.current_speed < 1: 
            self.MIN_VISIBLE_DELAY = 1500
            self.MAX_VISIBLE_DELAY = 7000

        elif 1 <= self.current_speed < 1.5: 
            self.MIN_VISIBLE_DELAY = 1000
            self.MAX_VISIBLE_DELAY = 5000

        elif 1.5 <= self.current_speed < 2: 
            self.MIN_VISIBLE_DELAY = 600
            self.MAX_VISIBLE_DELAY = 4000

        elif 2 <= self.current_speed <= 2.5: 
            self.MIN_VISIBLE_DELAY = 200
            self.MAX_VISIBLE_DELAY = 1500

    
    def get_delay_time(self, ai_thinking_time):
        thinking_time_ms = ai_thinking_time * 1000
        
        # More aggressive logarithmic compression
        compressed_time = math.log1p(thinking_time_ms) / math.log1p(self.BASELINE_THINKING_TIME)
        
        # Speed factor with smoother curve
        # speed_factor = (3 - self.current_speed) ** 2
        speed_factor = (3 - self.current_speed) ** (3 - self.current_speed)
        
        delay = compressed_time * speed_factor * 1000
        final_delay = max(self.MIN_VISIBLE_DELAY, 
                        min(self.MAX_VISIBLE_DELAY, delay))

        
        return final_delay / 1000

    
    def get_current_speed(self) -> float:
        return self.current_speed


    def get_board_speed(self, delay) -> int:
        max_value = 15
        min_value = 5

        calculated_speed = ((3 - self.current_speed) * delay)

        return int(min(max(calculated_speed, min_value), max_value))
