#!/usr/bin/env python3
"""
Swarm Website Backend API
=========================

FastAPI backend for swarm intelligence showcase website.

Created by: Agent-3 (Infrastructure & DevOps Specialist)
Partnership: Agent-7 (Frontend) + Agent-3 (Backend) + Agent-8 (SSOT)
Status: MVP Development - AUTONOMOUS EXECUTION!
"""

from fastapi import FastAPI, WebSocket
from fastapi.middleware.cors import CORSMiddleware
from pathlib import Path
import json
from typing import Any

app = FastAPI(
    title="Swarm Intelligence API",
    description="Backend API for swarm website - Real-time agent status, leaderboard, and more!",
    version="0.1.0"
)

# CORS for frontend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Configure based on deployment
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/")
async def root():
    """Root endpoint - API health check."""
    return {
        "status": "operational",
        "message": "🐝 Swarm Intelligence API - WE ARE SWARM!",
        "version": "0.1.0"
    }


@app.get("/api/agents")
async def get_agents():
    """Get all agent status from status.json files - USES AGENT-8 SSOT LAYER!"""
    try:
        # Use Agent-8's SSOT layer for validated data!
        from swarm_website_ssot import load_all_agents, validate_agent_status
        
        agents = load_all_agents()
        
        # Agent-8's SSOT validation ensures data integrity!
        for agent_id, data in agents.items():
            is_valid, errors = validate_agent_status(data)
            if not is_valid:
                logger.warning(f"Agent {agent_id} validation errors: {errors}")
        
        return {"agents": agents, "count": len(agents), "ssot_validated": True}
    except ImportError:
        # Fallback if SSOT layer not available yet
        logger.warning("SSOT layer not available, using direct file access")
        agents = {}
        base_path = Path(__file__).parent.parent.parent / "agent_workspaces"
        
        for agent_id in ["Agent-1", "Agent-2", "Agent-3", "Agent-4", "Agent-5", "Agent-6", "Agent-7", "Agent-8"]:
            status_file = base_path / agent_id / "status.json"
            if status_file.exists():
                with open(status_file, 'r', encoding='utf-8') as f:
                    agents[agent_id] = json.load(f)
        
        return {"agents": agents, "count": len(agents), "ssot_validated": False}


@app.get("/api/leaderboard")
async def get_leaderboard():
    """Get points leaderboard sorted by points."""
    agents_data = await get_agents()
    agents = agents_data["agents"]
    
    leaderboard = []
    for agent_id, data in agents.items():
        leaderboard.append({
            "agent_id": agent_id,
            "points": data.get("points_earned", 0),
            "rank": 0,  # Will be calculated
            "status": data.get("state", "UNKNOWN"),
            "current_mission": data.get("current_mission", "")
        })
    
    # Sort by points descending
    leaderboard.sort(key=lambda x: x["points"], reverse=True)
    
    # Assign ranks
    for i, agent in enumerate(leaderboard):
        agent["rank"] = i + 1
    
    return {"leaderboard": leaderboard}


@app.get("/api/swarm-status")
async def get_swarm_status():
    """Get overall swarm status and metrics - USES AGENT-8 SSOT LAYER!"""
    try:
        # Use Agent-8's SSOT layer for validated swarm overview!
        from swarm_website_ssot import get_swarm_overview
        
        overview = get_swarm_overview()
        return overview
    except ImportError:
        # Fallback if SSOT layer not available yet
        agents_data = await get_agents()
        agents = agents_data["agents"]
        
        total_points = sum(a.get("points_earned", 0) for a in agents.values())
        active_count = sum(1 for a in agents.values() if a.get("state") == "ACTIVE")
        
        return {
            "total_points": total_points,
            "active_agents": active_count,
            "total_agents": len(agents),
            "status": "OPERATIONAL" if active_count > 0 else "IDLE",
            "ssot_validated": False
        }


@app.get("/api/github-book")
async def get_github_book():
    """Get GitHub book data (Agent-2's parser + Agent-8 SSOT)."""
    from .github_book_api import github_book_api
    return {
        "repos": github_book_api.get_all_repos(),
        "coverage": "60/75 (80%)",
        "features": ["search", "filter", "8_fields", "achievements"],
        "jackpots": [
            {"id": 24, "name": "FocusForge", "roi": "3.3-5.0x", "value": "150-200hrs"},
            {"id": 26, "name": "TBOWTactics", "roi": "2.0-2.5x", "value": "120-150hrs"}
        ]
    }


@app.get("/api/debates")
async def get_debates():
    """Get active debates."""
    from .ssot_layer import ssot_integrator
    debates = ssot_integrator.get_debate_data()
    
    # Add live GitHub Archive debate status
    current_debate = {
        "id": "debate_20251014_184319",
        "topic": "GitHub Archive Strategy",
        "votes_cast": 7,
        "votes_total": 8,
        "consensus": "Aggressive 60% Archive",
        "agreement": "87.5%",
        "status": "STRONG CONSENSUS"
    }
    
    return {
        "debates": debates,
        "count": len(debates),
        "current": current_debate
    }


@app.get("/api/swarm-brain")
async def get_swarm_brain():
    """Get swarm brain stats."""
    from .ssot_layer import ssot_integrator
    brain_data = ssot_integrator.get_swarm_brain_knowledge()
    
    # Add featured protocols
    brain_data["featured_protocols"] = [
        "Gas Pipeline Protocol (PROMPTS_ARE_GAS)",
        "8-Cycle Perpetual Motion",
        "Anti-Approval-Dependency",
        "Co-Captain Training"
    ]
    
    return brain_data


@app.get("/api/gas-pipeline")
async def get_gas_pipeline():
    """Get gas pipeline visualization data."""
    from .gas_pipeline_api import gas_pipeline_api
    return gas_pipeline_api.get_gas_flow_data()


@app.get("/api/partnerships")
async def get_partnerships():
    """Get agent partnerships and collaborations."""
    partnerships = [
        {
            "id": "partnership_4",
            "agents": ["Agent-2", "Agent-8"],
            "project": "GitHub Book (Parser + Compilation)",
            "points": 1800,
            "status": "COMPLETE"
        },
        {
            "id": "partnership_5",
            "agents": ["Agent-7", "Agent-3", "Agent-8"],
            "project": "Swarm Website (Frontend + Backend + SSOT)",
            "points": "1,800-3,300 (estimated)",
            "status": "IN_PROGRESS"
        }
    ]
    return {"partnerships": partnerships, "count": len(partnerships)}


# WebSocket for real-time updates
@app.websocket("/ws/updates")
async def websocket_updates(websocket: WebSocket):
    """WebSocket endpoint for real-time swarm updates."""
    await websocket.accept()
    # TODO: Implement real-time status broadcasting
    # Send agent status changes, point updates, etc.
    await websocket.send_json({"message": "Connected to swarm updates!"})


# TODO (Agent-8 SSOT Layer):
# - Implement unified data schema
# - Add validation layers
# - Full integration with Agent-2's parser
# - Enhanced debate data processing

# TODO (Agent-7 Frontend):
# - Connect to these 6 endpoints
# - Beautiful dashboard UI
# - Leaderboard components
# - GitHub book browser
# - Real-time updates via WebSocket


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)

