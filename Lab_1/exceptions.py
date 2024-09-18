class ConfigParsingError(Exception):
    pass

class UnsupportedFileTypeError(Exception):
    pass

def handle_exceptions(func):
    def wrapper(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except FileNotFoundError as e:
            print(f"An error occurred: {e}")
        except (ValueError, ConfigParsingError, UnsupportedFileTypeError) as e:
            print(f"Processing error: {e}")
        except Exception as e:
            print(f"Unexpected error: {e}")
    return wrapper

