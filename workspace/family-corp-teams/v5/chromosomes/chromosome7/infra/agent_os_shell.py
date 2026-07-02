import sys
import os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import os
import threading
import time
from agent_os_kernel import AgentOSKernel

class AgentOSShell:
    def __init__(self, kernel: AgentOSKernel):
        self.kernel = kernel
        self.running = True

    def start(self):
        print("Agent OS Shell started. Type 'help' for commands.")
        while self.running:
            try:
                try:
                    raw = input("> ")
                except (EOFError, OSError):
                    print("Shell: input unavailable (non-interactive)")
                    break
                command = raw.strip().split()
                if not command:
                    continue
                if command[0] == 'run':
                    self._run_chromosome(command[1] if len(command) > 1 else None)
                elif command[0] == 'ps':
                    self._show_processes()
                elif command[0] == 'top':
                    self._show_resource_usage()
                elif command[0] == 'logs':
                    self._show_logs(command[1] if len(command) > 1 else None)
                elif command[0] == 'exit':
                    self.running = False
                elif command[0] == 'help':
                    self._show_help()
                else:
                    print(f"Unknown command: {command[0]}")
            except KeyboardInterrupt:
                print("\nExiting shell...")
                self.running = False

    def _run_chromosome(self, process_id: Optional[str]):
        if process_id:
            if self.kernel.create_process(process_id, 100):  # Default token budget
                print(f"Chromosome {process_id} started.")
            else:
                print(f"Chromosome {process_id} already exists.")
        else:
            print("Please specify a chromosome ID.")

    def _show_processes(self):
        print("\nProcess List:")
        for pid, info in self.kernel.processes.items():
            print(f"{pid}: {info['status']}")

    def _show_resource_usage(self):
        print("\nResource Usage:")
        for pid, info in self.kernel.processes.items():
            print(f"{pid}: CPU - {info['status']}, Memory - {self.kernel.get_memory_usage(pid)} tokens")

    def _show_logs(self, process_id: Optional[str]):
        if process_id:
            # Placeholder for log retrieval logic
            print(f"Logs for {process_id}: No logs available.")
        else:
            print("Please specify a chromosome ID.")

    def _show_help(self):
        print("\nAvailable commands:")
        print("  run <chromosome_id>   - Start a chromosome")
        print("  ps                  - Show process list")
        print("  top                 - Show resource usage")
        print("  logs <chromosome_id> - Show logs")
        print("  exit                - Exit the shell")
        print("  help                - Show this help")

    def stop(self):
        self.running = False

# Example usage
if __name__ == "__main__":
    kernel = AgentOSKernel()
    shell = AgentOSShell(kernel)
    shell.start()