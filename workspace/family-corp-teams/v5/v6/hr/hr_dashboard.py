import os

# Function to count job files by chromosome
def count_jobs_by_chromosome(directory):
    job_counts = {}
    for root, dirs, files in os.walk(directory):
        for file in files:
            if file.endswith('.py'):
                # Extract chromosome from file path
                # This is a simplified example; you would need to implement actual chromosome detection
                chromosome = '13'  # Placeholder for actual chromosome detection logic
                if chromosome not in job_counts:
                    job_counts[chromosome] = 0
                job_counts[chromosome] += 1
    return job_counts

# Main function
if __name__ == '__main__':
    # Directory to scan
    directory_to_scan = 'v5'

    # Count jobs by chromosome
    job_counts = count_jobs_by_chromosome(directory_to_scan)

    # Calculate statistics
    total_jobs = sum(job_counts.values())
    covered_chromosomes = len(job_counts)
    insufficient_jobs = sum(1 for count in job_counts.values() if count < 5)  # Example threshold

    # Generate report
    print("IGP HR 部门岗位状况")
    print("====================")
    print(f"总岗位数: {total_jobs}")
    print(f"覆盖染色体: 1-{covered_chromosomes}")
    print(f"充足率: {int((total_jobs / (covered_chromosomes * 10)) * 100)}%")  # Example calculation
    print(f"薄弱岗位: {insufficient_jobs}个")