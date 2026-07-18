# Domain Specific Exceptions

class DomainException(Exception):
    """Base domain exception"""
    pass

class UserAlreadyExistsException(DomainException):
    """Raised when attempting to create a user with an email that already exists"""
    def __init__(self, message: str = "User with this email already exists."):
        self.message = message
        super().__init__(self.message)

class UserNotFoundException(DomainException):
    """Raised when a requested user cannot be found in the system"""
    def __init__(self, message: str = "User not found."):
        self.message = message
        super().__init__(self.message)

class VehicleNotFoundException(DomainException):
    """Raised when a requested vehicle cannot be found in the system"""
    def __init__(self, message: str = "Vehicle not found."):
        self.message = message
        super().__init__(self.message)

class OutOfStockException(DomainException):
    """Raised when attempting to purchase more vehicle units than are in stock"""
    def __init__(self, message: str = "Requested purchase quantity exceeds stock limits."):
        self.message = message
        super().__init__(self.message)

class InvalidQuantityException(DomainException):
    """Raised when purchase or restock quantities are negative or zero"""
    def __init__(self, message: str = "Quantity must be greater than zero."):
        self.message = message
        super().__init__(self.message)

class UnauthorizedInventoryAccessException(DomainException):
    """Raised when an unauthorized user attempts to access or modify inventory"""
    def __init__(self, message: str = "Unauthorized inventory access."):
        self.message = message
        super().__init__(self.message)
