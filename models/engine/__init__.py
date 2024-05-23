#!/usr/bin/python3
"""
This module initializes a unique instance of FileStorage for the application.
"""

# Import the FileStorage class from the file_storage module
from models.engine.file_storage import FileStorage

# Create an instance of the FileStorage class
storage = FileStorage()

# Load data from storage into memory to set up the initial application state
storage.reload()
