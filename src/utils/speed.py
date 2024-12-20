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
            self.MIN_VISIBLE_DELAY = 2000  # De 1500 à 2000
            self.MAX_VISIBLE_DELAY = 8000  # De 7000 à 8000

        elif 1 <= self.current_speed < 1.5: 
            self.MIN_VISIBLE_DELAY = 1500  # De 1000 à 1500
            self.MAX_VISIBLE_DELAY = 6000  # De 5000 à 6000

        elif 1.5 <= self.current_speed < 2: 
            self.MIN_VISIBLE_DELAY = 800   # De 600 à 800
            self.MAX_VISIBLE_DELAY = 5000  # De 4000 à 5000

        elif 2 <= self.current_speed <= 2.5: 
            self.MIN_VISIBLE_DELAY = 300   # De 200 à 300
            self.MAX_VISIBLE_DELAY = 2000  # De 1500 à 2000

    
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


    def get_board_speed(self, delay) -> dict:
        """Get animation parameters based on current speed"""
        # Base values - plus conservateurs
        base_steps = 35  # Plus de steps pour plus de fluidité
        base_min_delay = 12  # Délai minimum plus élevé
        
        # Adjust steps and delay based on speed - changements plus graduels
        if self.current_speed < 1.0:  # Slow
            steps = int(base_steps * 1.15)  # ~40 steps
            min_delay = int(base_min_delay * 1.3)  # ~15-16ms
        elif self.current_speed < 1.5:  # Normal
            steps = base_steps  # 35 steps
            min_delay = base_min_delay  # 12ms
        else:  # Fast
            steps = int(base_steps * 0.9)  # ~31 steps
            min_delay = max(8, int(base_min_delay * 0.85))  # ~10ms

        # Animation delay avec scaling plus doux
        speed_factor = 3.5 - (self.current_speed * 0.8)  # Réduction plus progressive
        animation_delay = int(speed_factor * delay)

        return {
            'steps': steps,
            'min_delay': min_delay,
            'animation_delay': animation_delay
        }
