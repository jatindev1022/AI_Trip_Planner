class Calculator:
    @staticmethod
    def multiply(a, b) -> float:
        """
        Multiply two numbers. Handles strings passed by LLMs.
        """
        try:
            # Force conversion to float to prevent "sequence * float" error
            return float(a) * float(b)
        except (ValueError, TypeError):
            return 0.0
    
    @staticmethod
    def calculate_total(*x) -> float:
        """
        Calculate sum of the given numbers, ensuring all are floats.
        """
        try:
            # Convert every item in the tuple to a float before summing
            return sum(float(i) for i in x)
        except (ValueError, TypeError):
            return 0.0
    
    @staticmethod
    def calculate_daily_budget(total, days) -> float:
        """
        Calculate daily budget safely.
        """
        try:
            t = float(total)
            d = float(days)
            return t / d if d > 0 else 0.0
        except (ValueError, TypeError):
            return 0.0