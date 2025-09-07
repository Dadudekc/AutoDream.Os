"""
run_unified_portal_part_5.py
Module: run_unified_portal_part_5.py
Purpose: Automated documentation compliance
Created: 2025-08-31 00:37:00
"""

# Part 5 of run_unified_portal.py
# Original file: .\scripts\launchers\run_unified_portal.py

                logger.info("Portal Statistics:")
                logger.info(f"  Total Agents: {stats.get('total_agents', 0)}")
                logger.info(f"  Online Agents: {stats.get('online_agents', 0)}")
                logger.info(
                    f"  Active Integrations: {stats.get('active_integrations', 0)}"
                )

            # Get agent list
            if hasattr(self.portal, "portal") and hasattr(
                self.portal.portal, "get_all_agents"
            ):
                agents = self.portal.portal.get_all_agents()
                logger.info(f"\nAgent Status ({len(agents)} agents):")
                for agent in agents:
                    status_icon = "🟢" if agent.status == "online" else "🔴"
                    logger.info(
                        f"  {status_icon} {agent.name} ({agent.agent_id}) - {agent.status}"
                    )

        except Exception as e:
            logger.error(f"Error getting portal status: {e}")

    def test_integration(self):
        """Test portal integration"""
        if not self.portal:
            logger.info("Portal not created yet. Use 'launch' command first.")
            return

        try:
            logger.info("Testing portal integration...")

            # Test basic functionality
            if hasattr(self.portal, "portal"):
                logger.info("✅ Portal core accessible")

                if hasattr(self.portal.portal, "get_all_agents"):
                    agents = self.portal.portal.get_all_agents()
                    logger.info(f"✅ Agent management: {len(agents)} agents registered")

                if hasattr(self.portal.portal, "get_portal_stats"):
                    stats = self.portal.portal.get_portal_stats()
                    logger.info("✅ Portal statistics accessible")

                logger.info("✅ Portal integration test completed successfully")
            else:
                logger.error("❌ Portal core not accessible")

        except Exception as e:
            logger.error(f"❌ Portal integration test failed: {e}")


