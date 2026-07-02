import json
import logging
from collections import defaultdict

logger = logging.getLogger(__name__)

class MCP_PK_Rank:
    """MCP PK ranking module"""
    
    def __init__(self):
        self.servers = {}  # server_id -> {call_count, success_rate, token_efficiency}
        
    def update_ranking(self, server_id, call_count, success_rate, token_efficiency):
        """Update the ranking data for a server"""
        if server_id not in self.servers:
            self.servers[server_id] = {
                'call_count': 0,
                'success_rate': 0.0,
                'token_efficiency': 0.0
            }
        
        self.servers[server_id]['call_count'] += call_count
        self.servers[server_id]['success_rate'] = success_rate
        self.servers[server_id]['token_efficiency'] = token_efficiency
        
    def get_ranked_servers(self):
        """Get servers ranked by token efficiency"""
        return sorted(
            self.servers.items(),
            key=lambda x: x[1]['token_efficiency'],
            reverse=True
        )

    def check_eligibility(self, server_id):
        """Check if a server is eligible for promotion or demotion"""
        if server_id not in self.servers:
            return False
        
        # Check if the server has been inefficient for 3 consecutive checks
        # This is a placeholder for actual logic
        return self.servers[server_id]['token_efficiency'] < 0.5

    def promote_server(self, server_id):
        """Promote a server"""
        if server_id in self.servers:
            self.servers[server_id]['token_efficiency'] += 0.1

    def demote_server(self, server_id):
        """Demote a server"""
        if server_id in self.servers:
            self.servers[server_id]['token_efficiency'] -= 0.1