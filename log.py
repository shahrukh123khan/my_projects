import logging
import sys

# Configure logging
logging.basicConfig(filename='example.log', level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

# Create a separate logger for stdout
stdout_logger = logging.getLogger('stdout')

# Redirect stdout to the stdout logger
sys.stdout = stdout_logger

# Example usage
logging.debug('This is a debug message')
logging.info('This is an info message')
logging.warning('This is a warning message')
logging.error('This is an error message')
logging.critical('This is a critical message')

# This message will be logged to the file (because stdout i redirected to the stdout logger)
print('This message will be logged to the file')

# Configure loggin
logging.basicConfig(filename='example.log', level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

# Create a file-like object that writes to the log file
class LogWriter:
    def __init__(self, logger):
        self.logger = logger

    def write(self, message):
        if message.strip():
            self.logger.info(message.rstrip())

    def flush(self):
        pass

# Create a separate logger for stdout
stdout_logger = logging.getLogger('stdout')

# Redirect stdout to the file-like object
sys.stdout = LogWriter(stdout_logger)

# Example usage
logging.debug('This is a debug message')
logging.info('This is an info message')
logging.warning('This is a warning message')
logging.error('This is an error message')
logging.critical('This is a critical message')

# This message will be logged to the file (because stdout is redirected to the file-like object)
print('This message will be logged to the file')
