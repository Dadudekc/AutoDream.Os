#!/usr/bin/env python3
"""
Unified Systems Deployment Script - Direct Execution
Deploys unified systems across remaining agents
"""


def deploy_unified_systems():
    """Deploy unified systems to all target agents"""
    
    # Deployment targets
    deployment_targets = ["Agent-2", "Agent-3", "Agent-5", "Agent-6"]
    
    # Source files
    source_files = [
        "src/core/unified-logging-system.py",
        "src/core/unified-configuration-system.py", 
        "src/core/agent-8-ssot-integration.py"
    ]
    
    deployment_results = {}
    
    get_logger(__name__).info("🚨 UNIFIED SYSTEMS DEPLOYMENT MISSION ACTIVATED!")
    get_logger(__name__).info(f"📊 Deployment Targets: {', '.join(deployment_targets)}")
    get_logger(__name__).info(f"📁 Source Files: {', '.join(source_files)}")
    get_logger(__name__).info("=" * 60)
    
    for agent_id in deployment_targets:
        get_logger(__name__).info(f"\n🎯 Deploying to {agent_id}...")
        
        agent_results = {}
        target_path = get_unified_utility().Path(f"agent_workspaces/{agent_id}/src/core")
        target_path.mkdir(parents=True, exist_ok=True)
        
        for source_file in source_files:
            source_path = get_unified_utility().Path(source_file)
            target_file = target_path / source_path.name
            
            try:
                if source_path.exists():
                    shutil.copy2(source_path, target_file)
                    agent_results[source_path.name] = "✅ DEPLOYED"
                    get_logger(__name__).info(f"  ✅ {source_path.name} → {target_file}")
                else:
                    agent_results[source_path.name] = "❌ SOURCE NOT FOUND"
                    get_logger(__name__).info(f"  ❌ {source_path.name} - Source file not found")
                    
            except Exception as e:
                agent_results[source_path.name] = f"❌ ERROR: {e}"
                get_logger(__name__).info(f"  ❌ {source_path.name} - Error: {e}")
        
        deployment_results[agent_id] = agent_results
        
        # Create deployment status file
        status_file = target_path / "deployment-status.json"
        status_data = {
            "agent_id": agent_id,
            "deployment_timestamp": datetime.utcnow().isoformat(),
            "deployment_results": agent_results,
            "deployed_by": "Agent-7",
            "mission": "Unified Systems Deployment"
        }
        
        try:
            with open(status_file, 'w') as f:
                write_json(status_data, f, indent=2)
            get_logger(__name__).info(f"  📄 Deployment status saved: {status_file}")
        except Exception as e:
            get_logger(__name__).info(f"  ⚠️  Failed to save deployment status: {e}")
    
    get_logger(__name__).info("\n" + "=" * 60)
    get_logger(__name__).info("🏆 UNIFIED SYSTEMS DEPLOYMENT COMPLETED!")
    get_logger(__name__).info("=" * 60)
    
    # Summary
    total_targets = len(deployment_targets)
    successful_deployments = 0
    
    for agent_id, results in deployment_results.items():
        all_deployed = all("✅ DEPLOYED" in str(result) for result in results.values())
        if all_deployed:
            successful_deployments += 1
            get_logger(__name__).info(f"✅ {agent_id}: All systems deployed successfully")
        else:
            get_logger(__name__).info(f"⚠️  {agent_id}: Partial deployment - check results")
    
    success_rate = (successful_deployments / total_targets * 100) if total_targets > 0 else 0
    get_logger(__name__).info(f"\n📊 DEPLOYMENT SUMMARY:")
    get_logger(__name__).info(f"   Total Targets: {total_targets}")
    get_logger(__name__).info(f"   Successful Deployments: {successful_deployments}")
    get_logger(__name__).info(f"   Success Rate: {success_rate:.1f}%")
    
    return deployment_results

if __name__ == "__main__":
    results = deploy_unified_systems()
    get_logger(__name__).info(f"\n🎯 Mission Status: UNIFIED SYSTEMS DEPLOYMENT COMPLETED")
    get_logger(__name__).info("⚡ WE. ARE. SWARM. ⚡")

