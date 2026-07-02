'''Metrics Reporter - Generates metrics reports

This module provides the MetricsReporter class for generating metrics reports.
'''

import os
import json
import logging
from datetime import datetime, timedelta

logger = logging.getLogger(__name__)

class MetricsReporter:
    """Generates metrics reports."""

    def __init__(self, data_dir='data'):
        self.data_dir = data_dir

    def report(self, product, period_days=7):
        """Generate a report for the specified product over the given period.

        Args:
            product (str): Product name
            period_days (int): Number of days to look back for metrics

        Returns:
            dict: A dictionary containing the metrics report
        """
        try:
            logger.info(f"Generating report for product: {product} (period: {period_days} days)")
            end_date = datetime.now()
            start_date = end_date - timedelta(days=period_days)

            metrics = {
                'calls': 0,
                'latency': 0,
                'error_rate': 0.0,
                'top_error': ''
            }

            # Process each day's data in the period
            for date in self._get_dates_in_period(start_date, end_date):
                file_path = os.path.join(self.data_dir, f"{date}.jsonl")
                if os.path.exists(file_path):
                    with open(file_path, 'r', encoding='utf-8') as f:
                        for line in f:
                            entry = json.loads(line)
                            if entry['product'] == product:
                                metrics['calls'] += 1
                                metrics['latency'] += entry['latency_ms']
                                if not entry['success']:
                                    metrics['error_rate'] += 1
                                    if entry['error']:
                                        metrics['top_error'] = entry['error']

            # Calculate average latency and error rate
            if metrics['calls'] > 0:
                metrics['latency'] = metrics['latency'] / metrics['calls']
                metrics['error_rate'] = metrics['error_rate'] / metrics['calls']

            logger.info(f"Report generated for product: {product}")
            return metrics
        except Exception as e:
            logger.error(f"Error generating report: {str(e)}")
            return {
                'calls': 0,
                'latency': 0,
                'error_rate': 0.0,
                'top_error': ''
            }

    def _get_dates_in_period(self, start_date, end_date):
        """Generate a list of dates in the given period."""
        dates = []
        current_date = start_date
        while current_date <= end_date:
            dates.append(current_date.strftime('%Y-%m-%d'))
            current_date += timedelta(days=1)
        return dates

if __name__ == '__main__':
    # This is for testing purposes only
    reporter = MetricsReporter()
    metrics = reporter.report('example_product')
    print("Metrics report:")
    for key, value in metrics.items():
        print(f"  {key}: {value}")