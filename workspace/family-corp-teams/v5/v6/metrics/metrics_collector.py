'''Metrics Collector - Collects and stores metrics data

This module provides the MetricsCollector class for collecting and storing metrics data.
'''

import os
import json
import logging
from datetime import datetime

logger = logging.getLogger(__name__)

class MetricsCollector:
    """Collects and stores metrics data."""

    def __init__(self, data_dir='data'):
        self.data_dir = data_dir
        os.makedirs(self.data_dir, exist_ok=True)

    def record(self, product, method, latency_ms, success, error=""):
        """Record a metric entry.

        Args:
            product (str): Product name
            method (str): Method name
            latency_ms (int): Latency in milliseconds
            success (bool): Whether the operation was successful
            error (str): Error message if operation failed
        """
        try:
            logger.info(f"Recording metric: {product} - {method}")
            timestamp = datetime.now().strftime('%Y-%m-%d')
            file_path = os.path.join(self.data_dir, f"{timestamp}.jsonl")

            with open(file_path, 'a', encoding='utf-8') as f:
                entry = {
                    'timestamp': datetime.now().isoformat(),
                    'product': product,
                    'method': method,
                    'latency_ms': latency_ms,
                    'success': success,
                    'error': error
                }
                f.write(json.dumps(entry) + '\n')
            logger.info(f"Metric recorded: {product} - {method}")
        except Exception as e:
            logger.error(f"Error recording metric: {str(e)}")

if __name__ == '__main__':
    # This is for testing purposes only
    collector = MetricsCollector()
    collector.record('example_product', 'example_method', 100, True)