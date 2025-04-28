class ItsSoBigForIntegerError(ValueError):
    """класс кастомной ошибки (просто для понимания что простого понимания в коде)"""
    def __init__(self, message: str):
        super().__init__(message)
