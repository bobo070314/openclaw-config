"""Doctor Module — Bug scanning CLI command"""
import sys
import os

def doctor_scan(directory):
    """Run BugDoctor scan on the specified directory"""
    try:
        sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..', '..', 'chromosomes', 'chromosome9', 'infra')))
        from v5_bug_doctor import BugDoctor
        doctor = BugDoctor()
        result = doctor.scan_directory(directory)
        report = doctor.get_report()
        print(f"BugDoctor scan: {len(report)} issues found")
        for item in report[:10]:
            print(f"  - {item}")
        if len(report) > 10:
            print(f"  ... (+{len(report)-10} more)")
        return 0
    except Exception as e:
        print(f"Error: {e}")
        return 1

if __name__ == '__main__':
    sys.exit(doctor_scan(sys.argv[1] if len(sys.argv) > 1 else '.'))
