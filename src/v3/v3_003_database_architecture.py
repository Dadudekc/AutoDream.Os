#!/usr/bin/env python3
"""
V3-003: Database Architecture
=============================

V2 compliant database architecture coordinator.
Maintains all functionality while staying under 400 lines.
"""

import json
from datetime import datetime
from typing import Dict, List, Any, Optional
from pathlib import Path

# Import database modules
from v3.v3_003_database_core import (
    DatabaseManager, DatabaseFactory, DatabaseConfig, 
    ReplicationConfig, BackupConfig, ReplicationMode, BackupType
)
from v3.v3_003_database_monitoring import (
    DatabaseMonitor, DatabaseMetric, DatabaseAlert, AlertLevel
)


class DatabaseArchitectureCoordinator:
    """Coordinates database architecture components."""
    
    def __init__(self):
        self.db_manager = DatabaseManager()
        self.monitor = DatabaseMonitor()
        self.factory = DatabaseFactory()
        self.is_initialized = False
    
    def initialize(self):
        """Initialize database architecture."""
        try:
            # Register default databases
            self._register_default_databases()
            
            # Setup replication and backup
            self._setup_replication_and_backup()
            
            # Start monitoring
            self.monitor.start_monitoring()
            
            # Setup alert rules
            self._setup_alert_rules()
            
            self.is_initialized = True
            print("🗄️ Database Architecture Coordinator initialized successfully")
            return True
            
        except Exception as e:
            print(f"❌ Initialization error: {e}")
            return False
    
    def _register_default_databases(self):
        """Register default database configurations."""
        # PostgreSQL main database
        postgres_config = self.factory.create_postgresql_config(
            "localhost", 5432, "dream_os", "admin", "password"
        )
        self.db_manager.register_database("postgres_main", postgres_config)
        
        # MySQL backup database
        mysql_config = self.factory.create_mysql_config(
            "localhost", 3306, "dream_os_backup", "admin", "password"
        )
        self.db_manager.register_database("mysql_backup", mysql_config)
    
    def _setup_replication_and_backup(self):
        """Setup replication and backup configurations."""
        # Setup replication for PostgreSQL
        replication_config = self.factory.create_replication_config(
            ReplicationMode.MASTER_SLAVE, "localhost", ["slave1", "slave2"]
        )
        self.db_manager.setup_replication("postgres_main", replication_config)
        
        # Setup backup for PostgreSQL
        backup_config = self.factory.create_backup_config(
            BackupType.FULL, "0 2 * * *", 30
        )
        self.db_manager.setup_backup("postgres_main", backup_config)
    
    def _setup_alert_rules(self):
        """Setup monitoring alert rules."""
        self.monitor.add_alert_rule(
            "cpu_high", "postgres_main", "cpu_usage", 80.0, 
            AlertLevel.WARNING, "High CPU usage detected"
        )
        self.monitor.add_alert_rule(
            "memory_high", "postgres_main", "memory_usage", 90.0, 
            AlertLevel.CRITICAL, "High memory usage detected"
        )
        self.monitor.add_alert_rule(
            "connection_high", "postgres_main", "connection_count", 80.0, 
            AlertLevel.WARNING, "High connection count detected"
        )
    
    def get_database_status(self, database_id: str) -> Dict[str, Any]:
        """Get database status."""
        if not self.is_initialized:
            return {"error": "Database architecture not initialized"}
        
        # Get database configuration status
        db_status = self.db_manager.get_database_status(database_id)
        
        # Get health status
        health_status = self.monitor.get_database_health(database_id)
        
        return {
            **db_status,
            "health": health_status,
            "monitoring_active": self.monitor.monitoring_active
        }
    
    def get_all_databases_status(self) -> List[Dict[str, Any]]:
        """Get status of all databases."""
        if not self.is_initialized:
            return [{"error": "Database architecture not initialized"}]
        
        databases = self.db_manager.get_all_databases()
        return [self.get_database_status(db["database_id"]) for db in databases]
    
    def collect_metrics(self, database_id: str, metrics: Dict[str, float]):
        """Collect metrics for database."""
        if not self.is_initialized:
            return False
        
        for metric_name, value in metrics.items():
            self.monitor.collect_metric(
                database_id, metric_name, value, 
                unit="", labels={"source": "database_architecture"}
            )
        
        return True
    
    def get_monitoring_summary(self) -> Dict[str, Any]:
        """Get comprehensive monitoring summary."""
        if not self.is_initialized:
            return {"error": "Database architecture not initialized"}
        
        # Get database statuses
        databases = self.get_all_databases_status()
        
        # Get monitoring summary
        monitor_summary = self.monitor.get_monitoring_summary()
        
        # Get active alerts
        active_alerts = self.monitor.get_active_alerts()
        
        return {
            "databases": databases,
            "monitoring": monitor_summary,
            "active_alerts": [
                {
                    "alert_id": alert.alert_id,
                    "database_id": alert.database_id,
                    "level": alert.level.value,
                    "message": alert.message,
                    "triggered_at": alert.triggered_at.isoformat()
                }
                for alert in active_alerts
            ],
            "total_databases": len(databases),
            "healthy_databases": sum(1 for db in databases if db.get("health", {}).get("status") == "healthy"),
            "timestamp": datetime.now().isoformat()
        }
    
    def add_database(self, db_id: str, host: str, port: int, database: str, 
                    username: str, password: str) -> bool:
        """Add new database."""
        try:
            config = self.factory.create_postgresql_config(
                host, port, database, username, password
            )
            
            success = self.db_manager.register_database(db_id, config)
            if success:
                # Setup monitoring for new database
                self.monitor.add_alert_rule(
                    f"{db_id}_cpu", db_id, "cpu_usage", 80.0, 
                    AlertLevel.WARNING, f"High CPU usage on {db_id}"
                )
            
            return success
            
        except Exception as e:
            print(f"❌ Failed to add database {db_id}: {e}")
            return False
    
    def remove_database(self, db_id: str) -> bool:
        """Remove database."""
        try:
            # Remove from database manager
            if db_id in self.db_manager.configs:
                del self.db_manager.configs[db_id]
            
            # Remove from replication configs
            if db_id in self.db_manager.replication_configs:
                del self.db_manager.replication_configs[db_id]
            
            # Remove from backup configs
            if db_id in self.db_manager.backup_configs:
                del self.db_manager.backup_configs[db_id]
            
            print(f"🗑️ Removed database: {db_id}")
            return True
            
        except Exception as e:
            print(f"❌ Failed to remove database {db_id}: {e}")
            return False
    
    def export_configuration(self, filepath: str) -> bool:
        """Export database configuration."""
        try:
            config_data = {
                "databases": self.db_manager.get_all_databases(),
                "monitoring_summary": self.monitor.get_monitoring_summary(),
                "exported_at": datetime.now().isoformat()
            }
            
            with open(filepath, 'w') as f:
                json.dump(config_data, f, indent=2, default=str)
            
            print(f"📊 Database configuration exported to {filepath}")
            return True
            
        except Exception as e:
            print(f"❌ Export error: {e}")
            return False


def main():
    """Main execution function."""
    print("🗄️ V3-003 Database Architecture - Testing...")
    
    try:
        # Initialize coordinator
        coordinator = DatabaseArchitectureCoordinator()
        coordinator.initialize()
        
        # Collect sample metrics
        print("\n📊 Collecting sample metrics...")
        coordinator.collect_metrics("postgres_main", {
            "cpu_usage": 75.5,
            "memory_usage": 60.2,
            "connection_count": 45
        })
        
        # Get database status
        postgres_status = coordinator.get_database_status("postgres_main")
        
        print(f"\n🗄️ PostgreSQL Status:")
        print(f"   Host: {postgres_status['host']}:{postgres_status['port']}")
        print(f"   Replication: {postgres_status['replication_configured']}")
        print(f"   Backup: {postgres_status['backup_configured']}")
        print(f"   Health: {postgres_status['health']['status']}")
        
        # Get monitoring summary
        monitoring_summary = coordinator.get_monitoring_summary()
        
        print(f"\n📊 Monitoring Summary:")
        print(f"   Total Databases: {monitoring_summary['total_databases']}")
        print(f"   Healthy Databases: {monitoring_summary['healthy_databases']}")
        print(f"   Active Alerts: {len(monitoring_summary['active_alerts'])}")
        print(f"   Monitoring Active: {monitoring_summary['monitoring']['monitoring_active']}")
        
        # Export configuration
        coordinator.export_configuration("database_architecture_config.json")
        
        print("\n✅ V3-003 Database Architecture completed successfully!")
        return 0
        
    except Exception as e:
        print(f"❌ V3-003 implementation error: {e}")
        return 1


if __name__ == "__main__":
    exit(main())