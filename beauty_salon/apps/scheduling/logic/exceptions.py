# Custom exception for handling multiple validation errors.
class ValidationError(Exception):

    # Initializes the exception with a list of errors.
    def __init__(self, error_list: list):
        
        # Store the list of error messages for the view to access.
        self.errors = error_list
        
        # Set a generic message for the base Exception class.
        super().__init__(f"{len(error_list)} validation errors occurred.")