"""
Configuration Module

This module contains configuration settings for the application, such as Cloudinary API credentials.

Attributes:
    CLOUDINARY_API_KEY (str): Cloudinary API key obtained from your Cloudinary account.
    CLOUDINARY_API_SECRET (str): Cloudinary API secret obtained from your Cloudinary account.
    CLOUDINARY_CLOUD_NAME (str): Cloudinary cloud name associated with your Cloudinary account.

Note:
    Make sure to provide valid Cloudinary API credentials to use the Cloudinary services.

Example:
    To use these configurations in other modules, you can import them like this:

    >>> from .config import CLOUDINARY_API_KEY, CLOUDINARY_API_SECRET, CLOUDINARY_CLOUD_NAME
"""

from decouple import config

CLOUDINARY_API_KEY = config('CLOUDINARY_API_KEY')
CLOUDINARY_API_SECRET = config('CLOUDINARY_API_SECRET')
CLOUDINARY_CLOUD_NAME = config('CLOUDINARY_CLOUD_NAME')

"""
CLOUDINARY_API_KEY = 'your-cloudinary-api-key'
CLOUDINARY_API_SECRET = 'your-cloudinary-api-secret'
CLOUDINARY_CLOUD_NAME = 'your-cloudinary-cloud-name'
"""