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
        
        # Constants for delay calculation
        self.MIN_VISIBLE_DELAY = 500  # Minimum delay in milliseconds
        self.MAX_VISIBLE_DELAY = 5000  # Maximum delay in milliseconds
        self.BASELINE_THINKING_TIME = 1000  # Baseline AI thinking time in milliseconds
        
    def set_speed(self, slider_value):
        """Set speed based on slider value"""
        self.current_speed = max(self.min_speed, min(slider_value, self.max_speed))
        
    def get_delay_time(self, ai_thinking_time):
        """
        Calculate appropriate delay time using an improved algorithm
        
        Args:
            ai_thinking_time (float): Time taken by AI to make decision (in seconds)
            
        Returns:
            float: Adjusted delay time in seconds
        """
        # Convert AI thinking time to milliseconds
        thinking_time_ms = ai_thinking_time * 1000

        # print("AI_THINKING_TIME : ", ai_thinking_time)

        
        # Normalize thinking time relative to baseline
        normalized_thinking_time = thinking_time_ms / self.BASELINE_THINKING_TIME
        
        # Calculate base delay using a logarithmic scale to handle very long thinking times
        # This prevents excessive delays while maintaining proportionality
        base_delay = self.BASELINE_THINKING_TIME * math.log2(1 + normalized_thinking_time)
        
        # Apply speed modifier using an exponential scale
        # This gives finer control in the middle range and more extreme effects at the ends
        speed_factor = math.exp((4.0 - self.current_speed))
        
        # Calculate final delay
        delay = base_delay * speed_factor * 1000

        # Ensure delay stays within reasonable bounds
        final_delay = max(self.MIN_VISIBLE_DELAY, 
                         min(self.MAX_VISIBLE_DELAY, delay))
        
        # Convert back to seconds
        return final_delay / 1000
    
    def get_current_speed(self) -> float:
        return self.current_speed
    