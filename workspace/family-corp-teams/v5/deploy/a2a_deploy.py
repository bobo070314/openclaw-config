import threading
import http.server
import socketserver
import urllib.parse
import json

# Agent A (Code Review Agent)
class CodeReviewAgent(http.server.BaseHTTPRequestHandler):
    def do_POST(self):
        if self.path == '/task':
            content_length = int(self.headers['Content-Length'])
            post_data = self.rfile.read(content_length).decode('utf-8')
            task = json.loads(post_data)
            
            print(f"Received task: {task}")
            
            # Simulate processing the task
            response = {
                'status': 'success',
                'result': 'Code review completed successfully.'
            }
            
            self.send_response(200)
            self.send_header('Content-type', 'application/json')
            self.end_headers()
            self.wfile.write(json.dumps(response).encode('utf-8'))
        else:
            self.send_response(404)
            self.end_headers()

# Agent B (Translation Agent)
class TranslationAgent(http.server.BaseHTTPRequestHandler):
    def do_POST(self):
        if self.path == '/task':
            content_length = int(self.headers['Content-Length'])
            post_data = self.rfile.read(content_length).decode('utf-8')
            task = json.loads(post_data)
            
            print(f"Received task: {task}")
            
            # Simulate processing the task
            response = {
                'status': 'success',
                'result': 'Translation completed successfully.'
            }
            
            self.send_response(200)
            self.send_header('Content-type', 'application/json')
            self.end_headers()
            self.wfile.write(json.dumps(response).encode('utf-8'))
        else:
            self.send_response(404)
            self.end_headers()

# Start Agent A server
agent_a_port = 5001
agent_a_server = socketserver.TCPServer(('', agent_a_port), CodeReviewAgent)

# Start Agent B server
agent_b_port = 5002
agent_b_server = socketserver.TCPServer(('', agent_b_port), TranslationAgent)

# Function to send a task from Agent A to Agent B
def send_task_to_agent_b(task):
    import requests
    url = f'http://localhost:{agent_b_port}/task'
    headers = {'Content-Type': 'application/json'}
    response = requests.post(url, data=json.dumps(task), headers=headers)
    return response.json()

# Start servers in threads
threading.Thread(target=agent_a_server.serve_forever).start()
threading.Thread(target=agent_b_server.serve_forever).start()

# Example task
example_task = {
    'type': 'code_review',
    'content': 'def add(a, b):\n    return a + b\n\nprint(add(2, 3))'
}

# Send task and print response
response = send_task_to_agent_b(example_task)
print(f"Response from Agent B: {response}")

# Keep the script running to allow communication
while True:
    pass;