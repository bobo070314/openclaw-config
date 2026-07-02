'''Version Module - Version checking functionality

This module provides the version command for IGP CLI tool, which checks the version of a product.
'''

import sys
import os
import logging

# Add parent directory to sys.path for cross-module imports
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

logger = logging.getLogger(__name__)

def get_version(product_key):
    """Get the version of a product by its key.

    Args:
        product_key (str): Key of the product to check version

    Returns:
        str: Version of the product
    """
    try:
        logger.info(f"Getting version for product: {product_key}")
        # Implementation details would go here
        return "1.0.0"
    except Exception as e:
        logger.error(f"Error getting version: {str(e)}")
        return "Unknown"

if __name__ == '__main__':
    # This is for testing purposes only
    import sys
    if len(sys.argv) < 2:
        print("Usage: python version.py <product_key>")
        sys.exit(1)
    version = get_version(sys.argv[1])
    print(f"{sys.argv[1]} version: {version}")