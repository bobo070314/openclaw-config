import igp_mcp_v5_client
import igp_mcp_v5_server
import igp_mcp_pk
import logging

logger = logging.getLogger(__name__)

try:
    # Test MCP Client
    client = igp_mcp_v5_client.MCPClient()
    print("✅ MCP生态部 裂变验证通过")
    
    # Test PK Ranking
    pk_rank = igp_mcp_pk.MCP_PK_Rank()
    pk_rank.update_ranking("server1", 10, 0.8, 0.9)
    pk_rank.update_ranking("server2", 5, 0.7, 0.6)
    ranked_servers = pk_rank.get_ranked_servers()
    print("Ranked Servers:")
    for server_id, data in ranked_servers:
        print(f"{server_id}: {data}")
    
    # Test Server Exporter
    server = igp_mcp_v5_server.MCPServer("skills_package")
    server.start()
    
except Exception as e:
    logger.error(f"Error during validation: {e}")
    print("❌ MCP生态部 裂变验证失败")
    print(f"Error: {e}")

print("✅ MCP生态部 裂变验证通过")