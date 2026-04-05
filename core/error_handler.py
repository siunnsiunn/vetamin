class VetError(Exception):
    """Base class for all veterinary reasoning errors."""
    def __init__(self, message, field=None, suggestion=None):
        super().__init__(message)
        self.message = message
        self.field = field
        self.suggestion = suggestion

    def to_ai_message(self):
        """Format the error for AI consumption."""
        error_type = self.__class__.__name__
        msg = f"[{error_type}] {self.message}"
        if self.field:
            msg += f" (Field: {self.field})"
        if self.suggestion:
            msg += f"\nSuggestion: {self.suggestion}"
        return msg

class DataMissingError(VetError):
    """Raised when a required piece of clinical data is missing from the SSOT."""
    def __init__(self, field, message=None):
        if not message:
            message = f"Required clinical data '{field}' is missing."
        super().__init__(message, field=field, suggestion=f"Please provide the {field} to proceed.")

class DataStaleError(VetError):
    """Raised when data is too old for safe clinical reasoning."""
    def __init__(self, field, message=None, last_updated=None):
        if not message:
            message = f"Clinical data '{field}' is out of date."
        suggestion = f"Please re-assess or update {field}."
        if last_updated:
            message += f" (Last updated: {last_updated})"
        super().__init__(message, field=field, suggestion=suggestion)

class ContraindicationError(VetError):
    """Raised when a proposed treatment or drug is contraindicated for this patient."""
    def __init__(self, contraindication, suggestion=None):
        message = f"Contraindication detected: {contraindication}"
        super().__init__(message, field=None, suggestion=suggestion)
