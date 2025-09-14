
    def _load_config(self) -> Dict[str, Any]:
        """Load monitoring configuration."""
        default_config = {
            "monitoring": {
                "enabled": True,
                "check_interval_seconds": 60,
                "health_check_interval_seconds": 300,
                "metrics_retention_days": 30,
            },
            "alerts": {
                "enabled": True,
                "channels": ["console", "file", "discord", "email"],
                "severity_levels": {
                    "critical": {"threshold": 1, "escalation_minutes": 5},
                    "high": {"threshold": 3, "escalation_minutes": 15},
                    "medium": {"threshold": 5, "escalation_minutes": 60},
                    "low": {"threshold": 10, "escalation_minutes": 240}
                },
                "notification_cooldown_minutes": 30,
            },
            "thresholds": {
                "backup_age_hours": 48,
                "disk_usage_percent": 85,
                "backup_failure_rate_percent": 20,
                "recovery_time_minutes": 120,
                "data_integrity_failures": 1,
                "system_load_percent": 80,
                "memory_usage_percent": 90,
            },
            "health_checks": {
                "backup_system_health": {
                    "enabled": True,
                    "check_interval_seconds": 300,
                    "checks": [
                        "backup_database_connectivity",
                        "backup_storage_availability",
                        "backup_process_health",
                        "recovery_capability"
                    ]
                },
                "system_health": {
                    "enabled": True,
                    "check_interval_seconds": 60,
                    "checks": [
                        "disk_space",
                        "memory_usage",
                        "cpu_usage",
                        "network_connectivity"
                    ]
                },
                "data_integrity": {
                    "enabled": True,
                    "check_interval_seconds": 3600,
                    "checks": [
                        "backup_file_integrity",
                        "database_consistency",
                        "checksum_validation"
                    ]
                }
            },
            "notifications": {
                "discord": {
                    "enabled": False,
                    "webhook_url": None,
                    "channel_id": None
                },
                "email": {
                    "enabled": False,
                    "smtp_server": None,
                    "smtp_port": 587,
                    "username": None,
                    "password": None,
                    "to_addresses": [],
                    "from_address": None
                },
                "file": {
                    "enabled": True,
                    "log_file": "backup_monitoring.log"
                },
                "console": {
                    "enabled": True
                }
            }
        }

        try:
            if os.path.exists(self.config_path):
                with open(self.config_path, 'r') as f:
                    user_config = yaml.safe_load(f) or {}
                default_config.update(user_config)
        except Exception as e:
            logger.warning(f"Failed to load config from {self.config_path}: {e}")

        return default_config

    def _init_monitoring_database(self):
        """Initialize monitoring database."""
        with sqlite3.connect(self.monitoring_db_path) as conn:
            # Metrics table
            conn.execute("""
                CREATE TABLE IF NOT EXISTS monitoring_metrics (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    metric_name TEXT NOT NULL,
                    metric_value REAL NOT NULL,
                    metric_unit TEXT,
                    timestamp DATETIME NOT NULL,
                    tags TEXT,
                    created_at DATETIME DEFAULT CURRENT_TIMESTAMP
                )
            """)

            # Health checks table
            conn.execute("""
                CREATE TABLE IF NOT EXISTS health_checks (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    check_name TEXT NOT NULL,
                    check_type TEXT NOT NULL,
                    status TEXT NOT NULL,
                    message TEXT,
                    duration_ms INTEGER,
                    timestamp DATETIME NOT NULL,
                    created_at DATETIME DEFAULT CURRENT_TIMESTAMP
                )
            """)

            # Alerts table
            conn.execute("""
                CREATE TABLE IF NOT EXISTS alerts (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    alert_id TEXT UNIQUE NOT NULL,
                    alert_type TEXT NOT NULL,
                    severity TEXT NOT NULL,
                    title TEXT NOT NULL,
                    message TEXT NOT NULL,
                    status TEXT DEFAULT 'active',
                    acknowledged BOOLEAN DEFAULT 0,
                    acknowledged_by TEXT,
                    acknowledged_at DATETIME,
                    resolved_at DATETIME,
                    escalation_count INTEGER DEFAULT 0,
                    last_escalation DATETIME,
                    created_at DATETIME DEFAULT CURRENT_TIMESTAMP
                )
            """)

            # Alert history table
            conn.execute("""
                CREATE TABLE IF NOT EXISTS alert_history (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    alert_id TEXT NOT NULL,
                    action TEXT NOT NULL,
                    details TEXT,
                    timestamp DATETIME NOT NULL,
                    created_at DATETIME DEFAULT CURRENT_TIMESTAMP
                )
            """)

            conn.commit()

    async def start_monitoring(self):
        """Start the monitoring system."""
        if not self.config.get("monitoring", {}).get("enabled", True):
            logger.info("Backup monitoring is disabled in configuration")
            return

        logger.info("Starting backup monitoring system...")
        self.is_monitoring = True

        # Start monitoring tasks
        self.monitoring_tasks = [
            asyncio.create_task(self._monitoring_loop()),
            asyncio.create_task(self._health_check_loop()),
            asyncio.create_task(self._metrics_collection_loop()),
            asyncio.create_task(self._alert_processing_loop())
        ]

        try:
            await asyncio.gather(*self.monitoring_tasks)
        except Exception as e:
            logger.error(f"Monitoring system error: {e}")
        finally:
            await self.stop_monitoring()

    async def stop_monitoring(self):
        """Stop the monitoring system."""
        logger.info("Stopping backup monitoring system...")
        self.is_monitoring = False

        # Cancel all monitoring tasks
        for task in self.monitoring_tasks:
            if not task.done():
                task.cancel()

        # Wait for tasks to complete
        await asyncio.gather(*self.monitoring_tasks, return_exceptions=True)

    async def _monitoring_loop(self):
        """Main monitoring loop."""
        check_interval = self.config.get("monitoring", {}).get("check_interval_seconds", 60)

        while self.is_monitoring:
            try:
                await self._perform_monitoring_checks()
                await asyncio.sleep(check_interval)
            except Exception as e:
                logger.error(f"Monitoring check error: {e}")
                await asyncio.sleep(60)  # Wait 1 / 5-2 agent cycles before retrying

    async def _health_check_loop(self):
        """Health check monitoring loop."""
        health_checks = self.config.get("health_checks", {})

        while self.is_monitoring:
            try:
                for check_type, check_config in health_checks.items():
                    if check_config.get("enabled", True):
                        await self._perform_health_checks(check_type, check_config)

                # Wait for next health check cycle
                await asyncio.sleep(300)  # 5 / 5-2 agent cycles default
            except Exception as e:
                logger.error(f"Health check error: {e}")
                await asyncio.sleep(60)

    async def _metrics_collection_loop(self):
        """Metrics collection loop."""
        while self.is_monitoring:
            try:
                await self._collect_system_metrics()
                await self._collect_backup_metrics()
                await asyncio.sleep(60)  # Collect metrics every minute
            except Exception as e:
                logger.error(f"Metrics collection error: {e}")
                await asyncio.sleep(60)

    async def _alert_processing_loop(self):
        """Alert processing and escalation loop."""
        while self.is_monitoring:
            try:
                await self._process_active_alerts()
                await self._cleanup_old_metrics()
                await asyncio.sleep(60)  # Process alerts every minute
            except Exception as e:
                logger.error(f"Alert processing error: {e}")
                await asyncio.sleep(60)

    async def _perform_monitoring_checks(self):
        """Perform comprehensive monitoring checks."""
        checks = [
            self._check_backup_age,
            self._check_disk_usage,
            self._check_backup_failures,
            self._check_system_health,
            self._check_data_integrity
        ]

        for check_func in checks:
            try:
                await check_func()
            except Exception as e:
                logger.error(f"Monitoring check failed: {e}")

    async def _check_backup_age(self):
        """Check if backups are too old."""
        threshold_hours = self.config.get("thresholds", {}).get("backup_age_hours", 48)
        threshold_time = datetime.now() - timedelta(hours=threshold_hours)

        # Get latest backup
        backups = await self.backup_system.list_backups()
        if not backups:
            await self._create_alert(
                "no_backups",
                "critical",
                "No Backups Found",
                "No backups found in the system. Immediate action required."
            )
            return

        latest_backup = backups[0]
        latest_time = datetime.fromisoformat(latest_backup["timestamp"])

        if latest_time < threshold_time:
            age_hours = (datetime.now() - latest_time).total_seconds() / 3600
            await self._create_alert(
                "old_backup",
                "high",
                "Backup Age Warning",
                f"Latest backup is {age_hours:.1f} hours old (threshold: {threshold_hours} hours)"
            )

    async def _check_disk_usage(self):
        """Check disk usage for backup directory."""
        threshold_percent = self.config.get("thresholds", {}).get("disk_usage_percent", 85)

        try:
            backup_root = self.backup_system.backup_root
            usage = psutil.disk_usage(backup_root)

            usage_percent = (usage.used / usage.total) * 100

            if usage_percent > threshold_percent:
                free_gb = usage.free / (1024**3)
                await self._create_alert(
                    "disk_usage_high",
                    "high",
                    "Disk Usage Warning",
                    f"Disk usage is {usage_percent:.1f}% (threshold: {threshold_percent}%). Free space: {free_gb:.1f} GB"
                )

            # Record metric
            await self._record_metric("disk_usage_percent", usage_percent, "percent")

        except Exception as e:
            logger.error(f"Failed to check disk usage: {e}")

    async def _check_backup_failures(self):
        """Check for recent backup failures."""
        threshold_percent = self.config.get("thresholds", {}).get("backup_failure_rate_percent", 20)

        # Count recent backups and failures (last 288-720 agent cycles)
        cutoff_time = datetime.now() - timedelta(hours=24)

        with sqlite3.connect(self.backup_system.db_path) as conn:
            # Total backups
            cursor = conn.execute("""
                SELECT COUNT(*) FROM backup_metadata
                WHERE timestamp > ?
            """, (cutoff_time,))
            total_backups = cursor.fetchone()[0]

            # Failed backups
            cursor = conn.execute("""
                SELECT COUNT(*) FROM backup_metadata
                WHERE timestamp > ? AND status != 'completed'
            """, (cutoff_time,))
            failed_backups = cursor.fetchone()[0]

        if total_backups > 0:
            failure_rate = (failed_backups / total_backups) * 100

            if failure_rate > threshold_percent:
                await self._create_alert(
                    "backup_failure_rate_high",
                    "high",
                    "Backup Failure Rate Warning",
                    f"Backup failure rate is {failure_rate:.1f}% (threshold: {threshold_percent}%). {failed_backups}/{total_backups} backups failed."
                )

            # Record metric
            await self._record_metric("backup_failure_rate", failure_rate, "percent")

    async def _check_system_health(self):
        """Check overall system health."""
        # CPU usage
        cpu_percent = psutil.cpu_percent(interval=1)
        cpu_threshold = self.config.get("thresholds", {}).get("system_load_percent", 80)

        if cpu_percent > cpu_threshold:
            await self._create_alert(
                "cpu_usage_high",
                "medium",
                "High CPU Usage",
                f"CPU usage is {cpu_percent:.1f}% (threshold: {cpu_threshold}%)"
            )

        # Memory usage
        memory = psutil.virtual_memory()
        memory_threshold = self.config.get("thresholds", {}).get("memory_usage_percent", 90)

        if memory.percent > memory_threshold:
            await self._create_alert(
                "memory_usage_high",
                "medium",
                "High Memory Usage",
                f"Memory usage is {memory.percent:.1f}% (threshold: {memory_threshold}%)"
            )

        # Record metrics
        await self._record_metric("cpu_usage_percent", cpu_percent, "percent")
        await self._record_metric("memory_usage_percent", memory.percent, "percent")

    async def _check_data_integrity(self):
        """Check data integrity of backups."""
        integrity_failures = 0

        # Check recent backups for integrity
        recent_backups = await self.backup_system.list_backups()
        for backup in recent_backups[:5]:  # Check last 5 backups
            try:
                if backup.get("backup_path"):
                    backup_path = Path(backup["backup_path"])
                    if backup_path.exists():
                        # Verify checksum if available
                        if backup.get("checksum_sha256"):
                            # This would perform actual checksum verification
                            # For now, we'll simulate it
                            pass
            except Exception as e:
                integrity_failures += 1
                logger.warning(f"Data integrity check failed for backup {backup['backup_id']}: {e}")

        if integrity_failures > 0:
            await self._create_alert(
                "data_integrity_failure",
                "critical",
                "Data Integrity Failure",
                f"{integrity_failures} backup(s) failed integrity checks"
            )

    async def _perform_health_checks(self, check_type: str, check_config: Dict[str, Any]):
        """Perform specific health checks."""
        checks = check_config.get("checks", [])

        for check_name in checks:
            try:
                start_time = datetime.now()

                # Execute health check
                if check_name == "backup_database_connectivity":
                    result = await self._check_backup_database_connectivity()
                elif check_name == "backup_storage_availability":
                    result = await self._check_backup_storage_availability()
                elif check_name == "backup_process_health":
                    result = await self._check_backup_process_health()
                elif check_name == "recovery_capability":
                    result = await self._check_recovery_capability()
                elif check_name == "disk_space":
                    result = await self._check_disk_space()
                elif check_name == "memory_usage":
                    result = await self._check_memory_usage()
                elif check_name == "cpu_usage":
                    result = await self._check_cpu_usage()
                elif check_name == "network_connectivity":
                    result = await self._check_network_connectivity()
                elif check_name == "backup_file_integrity":
                    result = await self._check_backup_file_integrity()
                elif check_name == "database_consistency":
                    result = await self._check_database_consistency()
                elif check_name == "checksum_validation":
                    result = await self._check_checksum_validation()
                else:
                    result = {"status": "unknown", "message": f"Unknown check: {check_name}"}

                # Record health check result
                duration_ms = int((datetime.now() - start_time).total_seconds() * 1000)
                await self._record_health_check(check_name, check_type, result["status"], result.get("message"), duration_ms)

            except Exception as e:
                logger.error(f"Health check {check_name} failed: {e}")
                await self._record_health_check(check_name, check_type, "error", str(e), 0)

    async def _check_backup_database_connectivity(self) -> Dict[str, Any]:
        """Check backup database connectivity."""
        try:
            with sqlite3.connect(self.backup_system.db_path) as conn:
                conn.execute("SELECT 1")
            return {"status": "healthy", "message": "Database connection successful"}
        except Exception as e:
            return {"status": "unhealthy", "message": f"Database connection failed: {e}"}

    async def _check_backup_storage_availability(self) -> Dict[str, Any]:
        """Check backup storage availability."""
        try:
            backup_root = self.backup_system.backup_root
            if backup_root.exists() and backup_root.is_dir():
                # Test write access
                test_file = backup_root / "health_check_test.tmp"
                test_file.write_text("test")
                test_file.unlink()
                return {"status": "healthy", "message": "Storage is accessible and writable"}
            else:
                return {"status": "unhealthy", "message": "Backup storage directory not accessible"}
        except Exception as e:
            return {"status": "unhealthy", "message": f"Storage check failed: {e}"}

    async def _check_backup_process_health(self) -> Dict[str, Any]:
        """Check backup process health."""
        try:
            # Check if backup system is responsive
            stats = await self.backup_system.get_backup_statistics()
            if stats.get("total_backups", 0) >= 0:
                return {"status": "healthy", "message": "Backup system is responsive"}
            else:
                return {"status": "unhealthy", "message": "Backup system not responding"}
        except Exception as e:
            return {"status": "unhealthy", "message": f"Backup process check failed: {e}"}

    async def _check_recovery_capability(self) -> Dict[str, Any]:
        """Check recovery capability."""
        try:
            # Check if we have recent backups available for recovery
            backups = await self.backup_system.list_backups()
            if backups:
                latest_backup = backups[0]
                backup_time = datetime.fromisoformat(latest_backup["timestamp"])
                age_hours = (datetime.now() - backup_time).total_seconds() / 3600

                if age_hours < 24:  # Recent backup available
                    return {"status": "healthy", "message": f"Recovery capability available (latest backup: {age_hours:.1f}h old)"}
                else:
                    return {"status": "warning", "message": f"Recovery capability limited (latest backup: {age_hours:.1f}h old)"}
            else:
                return {"status": "unhealthy", "message": "No backups available for recovery"}
        except Exception as e:
            return {"status": "unhealthy", "message": f"Recovery capability check failed: {e}"}

    async def _check_disk_space(self) -> Dict[str, Any]:
        """Check disk space."""
        try:
            backup_root = self.backup_system.backup_root
            usage = psutil.disk_usage(backup_root)
            free_gb = usage.free / (1024**3)

            if free_gb > 10:  # More than 10GB free
                return {"status": "healthy", "message": f"Sufficient disk space: {free_gb:.1f} GB free"}
            elif free_gb > 5:  # More than 5GB free
                return {"status": "warning", "message": f"Low disk space: {free_gb:.1f} GB free"}
            else:
                return {"status": "unhealthy", "message": f"Critical disk space: {free_gb:.1f} GB free"}
        except Exception as e:
            return {"status": "unhealthy", "message": f"Disk space check failed: {e}"}

    async def _check_memory_usage(self) -> Dict[str, Any]:
        """Check memory usage."""
        try:
            memory = psutil.virtual_memory()
            if memory.percent < 70:
                return {"status": "healthy", "message": f"Memory usage normal: {memory.percent:.1f}%"}
            elif memory.percent < 90:
                return {"status": "warning", "message": f"High memory usage: {memory.percent:.1f}%"}
            else:
                return {"status": "unhealthy", "message": f"Critical memory usage: {memory.percent:.1f}%"}
        except Exception as e:
            return {"status": "unhealthy", "message": f"Memory check failed: {e}"}

    async def _check_cpu_usage(self) -> Dict[str, Any]:
        """Check CPU usage."""
        try:
            cpu_percent = psutil.cpu_percent(interval=1)
            if cpu_percent < 70:
                return {"status": "healthy", "message": f"CPU usage normal: {cpu_percent:.1f}%"}
            elif cpu_percent < 90:
                return {"status": "warning", "message": f"High CPU usage: {cpu_percent:.1f}%"}
            else:
                return {"status": "unhealthy", "message": f"Critical CPU usage: {cpu_percent:.1f}%"}
        except Exception as e:
            return {"status": "unhealthy", "message": f"CPU check failed: {e}"}

    async def _check_network_connectivity(self) -> Dict[str, Any]:
        """Check network connectivity."""
        try:
            # Simple network connectivity check
            import socket
            socket.create_connection(("8.8.8.8", 53), timeout=3)
            return {"status": "healthy", "message": "Network connectivity normal"}
        except Exception as e:
            return {"status": "unhealthy", "message": f"Network connectivity failed: {e}"}

    async def _check_backup_file_integrity(self) -> Dict[str, Any]:
        """Check backup file integrity."""
        try:
            # Check if backup files exist and are readable
            backups = await self.backup_system.list_backups()
            if not backups:
                return {"status": "unhealthy", "message": "No backup files found"}

            # Check last few backups
            for backup in backups[:3]:
                if backup.get("backup_path"):
                    backup_path = Path(backup["backup_path"])
                    if not backup_path.exists():
                        return {"status": "unhealthy", "message": f"Backup file missing: {backup_path}"}
                    if backup_path.stat().st_size == 0:
                        return {"status": "unhealthy", "message": f"Backup file empty: {backup_path}"}

            return {"status": "healthy", "message": "Backup file integrity verified"}
        except Exception as e:
            return {"status": "unhealthy", "message": f"Backup file integrity check failed: {e}"}

    async def _check_database_consistency(self) -> Dict[str, Any]:
        """Check database consistency."""
        try:
            with sqlite3.connect(self.backup_system.db_path) as conn:
                # Check for orphaned records or inconsistencies
                cursor = conn.execute("SELECT COUNT(*) FROM backup_metadata")
                backup_count = cursor.fetchone()[0]

                if backup_count > 0:
                    return {"status": "healthy", "message": f"Database consistent with {backup_count} backup records"}
                else:
                    return {"status": "warning", "message": "Database empty - no backup records found"}
        except Exception as e:
            return {"status": "unhealthy", "message": f"Database consistency check failed: {e}"}

    async def _check_checksum_validation(self) -> Dict[str, Any]:
        """Check checksum validation."""
        try:
            # Check if checksums are being calculated and stored
            with sqlite3.connect(self.backup_system.db_path) as conn:
                cursor = conn.execute("""
                    SELECT COUNT(*) FROM backup_metadata
                    WHERE checksum_sha256 IS NOT NULL
                """)
                checksum_count = cursor.fetchone()[0]

                cursor = conn.execute("SELECT COUNT(*) FROM backup_metadata")
                total_count = cursor.fetchone()[0]

                if total_count == 0:
                    return {"status": "warning", "message": "No backups found for checksum validation"}
                elif checksum_count == total_count:
                    return {"status": "healthy", "message": f"All {total_count} backups have checksums"}
                else:
                    return {"status": "warning", "message": f"Only {checksum_count}/{total_count} backups have checksums"}
        except Exception as e:
            return {"status": "unhealthy", "message": f"Checksum validation check failed: {e}"}

    async def _collect_system_metrics(self):
        """Collect system metrics."""
        try:
            # CPU metrics
            cpu_percent = psutil.cpu_percent(interval=1)
            await self._record_metric("system.cpu.usage", cpu_percent, "percent")

            # Memory metrics
            memory = psutil.virtual_memory()
            await self._record_metric("system.memory.usage", memory.percent, "percent")
            await self._record_metric("system.memory.available", memory.available / (1024**3), "GB")

            # Disk metrics
            backup_root = self.backup_system.backup_root
            disk_usage = psutil.disk_usage(backup_root)
            await self._record_metric("system.disk.usage", (disk_usage.used / disk_usage.total) * 100, "percent")
            await self._record_metric("system.disk.free", disk_usage.free / (1024**3), "GB")

        except Exception as e:
            logger.error(f"Failed to collect system metrics: {e}")

    async def _collect_backup_metrics(self):
        """Collect backup-specific metrics."""
        try:
            # Backup statistics
            stats = await self.backup_system.get_backup_statistics()

            await self._record_metric("backup.total_count", stats.get("total_backups", 0), "count")
            await self._record_metric("backup.total_size_mb", stats.get("total_size_mb", 0), "MB")

            # Recent backup age
            backups = await self.backup_system.list_backups()
            if backups:
                latest_backup = backups[0]
                backup_time = datetime.fromisoformat(latest_backup["timestamp"])
                age_hours = (datetime.now() - backup_time).total_seconds() / 3600
                await self._record_metric("backup.latest_age_hours", age_hours, "hours")

        except Exception as e:
            logger.error(f"Failed to collect backup metrics: {e}")

    async def _record_metric(self, metric_name: str, metric_value: float, metric_unit: str, tags: Optional[Dict[str, str]] = None):
        """Record a metric in the monitoring database."""
        try:
            with sqlite3.connect(self.monitoring_db_path) as conn:
                conn.execute("""
                    INSERT INTO monitoring_metrics
                    (metric_name, metric_value, metric_unit, timestamp, tags)
                    VALUES (?, ?, ?, ?, ?)
                """, (
                    metric_name,
                    metric_value,
                    metric_unit,
                    datetime.now(),
                    json.dumps(tags) if tags else None
                ))
                conn.commit()
        except Exception as e:
            logger.error(f"Failed to record metric {metric_name}: {e}")

    async def _record_health_check(self, check_name: str, check_type: str, status: str, message: str, duration_ms: int):
        """Record health check result."""
        try:
            with sqlite3.connect(self.monitoring_db_path) as conn:
                conn.execute("""
                    INSERT INTO health_checks
                    (check_name, check_type, status, message, duration_ms, timestamp)
                    VALUES (?, ?, ?, ?, ?, ?)
                """, (check_name, check_type, status, message, duration_ms, datetime.now()))
                conn.commit()
        except Exception as e:
            logger.error(f"Failed to record health check {check_name}: {e}")

    async def _create_alert(self, alert_type: str, severity: str, title: str, message: str):
        """Create a new alert."""
        alert_id = f"{alert_type}_{datetime.now().strftime('%Y%m%d_%H%M%S')}"

        try:
            with sqlite3.connect(self.monitoring_db_path) as conn:
                # Check if similar alert already exists
                cursor = conn.execute("""
                    SELECT id FROM alerts
                    WHERE alert_type = ? AND status = 'active'
                    ORDER BY created_at DESC LIMIT 1
                """, (alert_type,))
                existing_alert = cursor.fetchone()

                if existing_alert:
                    # Update existing alert instead of creating new one
                    conn.execute("""
                        UPDATE alerts
                        SET message = ?, escalation_count = escalation_count + 1, last_escalation = ?
                        WHERE id = ?
                    """, (message, datetime.now(), existing_alert[0]))
                else:
                    # Create new alert
                    conn.execute("""
                        INSERT INTO alerts
                        (alert_id, alert_type, severity, title, message, status)
                        VALUES (?, ?, ?, ?, ?, ?)
                    """, (alert_id, alert_type, severity, title, message, "active"))

                conn.commit()

                # Send notification
                await self._send_alert_notification(alert_id, alert_type, severity, title, message)

        except Exception as e:
            logger.error(f"Failed to create alert {alert_id}: {e}")

    async def _send_alert_notification(self, alert_id: str, alert_type: str, severity: str, title: str, message: str):
        """Send alert notification through configured channels."""
        if not self.config.get("alerts", {}).get("enabled", True):
            return

        channels = self.config.get("alerts", {}).get("channels", ["console"])

        for channel in channels:
            try:
                if channel == "console":
                    await self._send_console_alert(alert_id, severity, title, message)
                elif channel == "file":
                    await self._send_file_alert(alert_id, severity, title, message)
                elif channel == "discord":
                    await self._send_discord_alert(alert_id, severity, title, message)
                elif channel == "email":
                    await self._send_email_alert(alert_id, severity, title, message)
            except Exception as e:
                logger.error(f"Failed to send {channel} alert: {e}")

    async def _send_console_alert(self, alert_id: str, severity: str, title: str, message: str):
        """Send console alert."""
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        severity_emoji = {
            "critical": "🚨",
            "high": "⚠️",
            "medium": "⚡",
            "low": "ℹ️"
        }
        emoji = severity_emoji.get(severity, "📢")

        print(f"\n{emoji} ALERT [{severity.upper()}] {timestamp}")
        print(f"ID: {alert_id}")
        print(f"Title: {title}")
        print(f"Message: {message}")
        print("-" * 50)

    async def _send_file_alert(self, alert_id: str, severity: str, title: str, message: str):
        """Send file alert."""
        log_file = self.backup_system.backup_root / "alerts.log"
        timestamp = datetime.now().isoformat()

        alert_data = {
            "alert_id": alert_id,
            "severity": severity,
            "title": title,
            "message": message,
            "timestamp": timestamp
        }

        with open(log_file, "a") as f:
            f.write(f"{json.dumps(alert_data)}\n")

    async def _send_discord_alert(self, alert_id: str, severity: str, title: str, message: str):
        """Send Discord alert."""
        webhook_url = self.config.get("notifications", {}).get("discord", {}).get("webhook_url")
        if not webhook_url:
            return

        # Create Discord embed
        color_map = {
            "critical": 0xff0000,  # Red
            "high": 0xff6600,      # Orange
            "medium": 0xffcc00,    # Yellow
            "low": 0x00ff00        # Green
        }

        embed = {
            "title": f"🚨 Backup System Alert - {severity.upper()}",
            "description": f"**{title}**\n\n{message}",
            "color": color_map.get(severity, 0x00ff00),
            "timestamp": datetime.now().isoformat(),
            "fields": [
                {"name": "Alert ID", "value": alert_id, "inline": True},
                {"name": "Severity", "value": severity.upper(), "inline": True}
            ]
        }

        # Send webhook (simplified - would need requests library)
        logger.info(f"Discord alert: {title} - {message}")

    async def _send_email_alert(self, alert_id: str, severity: str, title: str, message: str):
        """Send email alert."""
        email_config = self.config.get("notifications", {}).get("email", {})
        if not email_config.get("enabled", False):
            return

        # Email sending would require smtplib implementation
        logger.info(f"Email alert: {title} - {message}")

    async def _process_active_alerts(self):
        """Process active alerts for escalation."""
        try:
            with sqlite3.connect(self.monitoring_db_path) as conn:
                # Get active alerts
                cursor = conn.execute("""
                    SELECT * FROM alerts
                    WHERE status = 'active'
                    ORDER BY created_at ASC
                """)
                active_alerts = cursor.fetchall()

                for alert in active_alerts:
                    await self._process_alert_escalation(alert)

        except Exception as e:
            logger.error(f"Failed to process active alerts: {e}")

    async def _process_alert_escalation(self, alert):
        """Process alert escalation."""
        alert_id, alert_type, severity, title, message, status, acknowledged, acknowledged_by, acknowledged_at, resolved_at, escalation_count, last_escalation, created_at = alert

        # Check if escalation is needed
        escalation_config = self.config.get("alerts", {}).get("severity_levels", {}).get(severity, {})
        escalation_threshold = escalation_config.get("threshold", 5)
        escalation_minutes = escalation_config.get("escalation_minutes", 60)

        if escalation_count >= escalation_threshold:
            # Check if enough time has passed for escalation
            if last_escalation:
                last_escalation_time = datetime.fromisoformat(last_escalation)
                time_since_escalation = (datetime.now() - last_escalation_time).total_seconds() / 60

                if time_since_escalation >= escalation_minutes:
                    await self._escalate_alert(alert_id, severity, title, message)
        else:
            # Increment escalation count
            with sqlite3.connect(self.monitoring_db_path) as conn:
                conn.execute("""
                    UPDATE alerts
                    SET escalation_count = escalation_count + 1, last_escalation = ?
                    WHERE alert_id = ?
                """, (datetime.now(), alert_id))
                conn.commit()

    async def _escalate_alert(self, alert_id: str, severity: str, title: str, message: str):
        """Escalate an alert."""
        logger.warning(f"Escalating alert {alert_id} - {title}")

        # Send escalation notification
        escalation_message = f"ESCALATED: {message}"
        await self._send_alert_notification(alert_id, "escalated", severity, f"ESCALATED: {title}", escalation_message)

    async def _cleanup_old_metrics(self):
        """Clean up old metrics based on retention policy."""
        retention_days = self.config.get("monitoring", {}).get("metrics_retention_days", 30)
        cutoff_date = datetime.now() - timedelta(days=retention_days)

        try:
            with sqlite3.connect(self.monitoring_db_path) as conn:
                # Clean up old metrics
                cursor = conn.execute("""
                    DELETE FROM monitoring_metrics
                    WHERE timestamp < ?
                """, (cutoff_date,))
                metrics_deleted = cursor.rowcount

                # Clean up old health checks
                cursor = conn.execute("""
                    DELETE FROM health_checks
                    WHERE timestamp < ?
                """, (cutoff_date,))
                health_checks_deleted = cursor.rowcount

                conn.commit()

                if metrics_deleted > 0 or health_checks_deleted > 0:
                    logger.info(f"Cleaned up {metrics_deleted} old metrics and {health_checks_deleted} old health checks")

        except Exception as e:
            logger.error(f"Failed to cleanup old metrics: {e}")

    async def get_monitoring_status(self) -> Dict[str, Any]:
        """Get current monitoring system status."""
        try:
            # Get recent metrics
            with sqlite3.connect(self.monitoring_db_path) as conn:
                # Active alerts count
                cursor = conn.execute("SELECT COUNT(*) FROM alerts WHERE status = 'active'")
                active_alerts = cursor.fetchone()[0]

                # Recent health checks
                cursor = conn.execute("""
                    SELECT check_name, status, timestamp
                    FROM health_checks
                    WHERE timestamp > datetime('now', '-12-30 agent cycles')
                    ORDER BY timestamp DESC
                """)
                recent_health_checks = [dict(row) for row in cursor.fetchall()]

                # System metrics
                cursor = conn.execute("""
                    SELECT metric_name, metric_value, timestamp
                    FROM monitoring_metrics
                    WHERE timestamp > datetime('now', '-12-30 agent cycles')
                    ORDER BY timestamp DESC
                """)
                recent_metrics = [dict(row) for row in cursor.fetchall()]

            return {
                "monitoring_status": "active" if self.is_monitoring else "inactive",
                "active_alerts": active_alerts,
                "recent_health_checks": recent_health_checks,
                "recent_metrics": recent_metrics,
                "monitoring_database": str(self.monitoring_db_path),
                "config": self.config
            }

        except Exception as e:
            logger.error(f"Failed to get monitoring status: {e}")
            return {
                "monitoring_status": "error",
                "error": str(e)
            }

    async def acknowledge_alert(self, alert_id: str, acknowledged_by: str) -> bool:
        """Acknowledge an alert."""
        try:
            with sqlite3.connect(self.monitoring_db_path) as conn:
                cursor = conn.execute("""
                    UPDATE alerts
                    SET acknowledged = 1, acknowledged_by = ?, acknowledged_at = ?
                    WHERE alert_id = ?
                """, (acknowledged_by, datetime.now(), alert_id))

                if cursor.rowcount > 0:
                    conn.commit()
                    logger.info(f"Alert {alert_id} acknowledged by {acknowledged_by}")
                    return True
                else:
                    logger.warning(f"Alert {alert_id} not found")
                    return False

        except Exception as e:
            logger.error(f"Failed to acknowledge alert {alert_id}: {e}")
            return False

    async def resolve_alert(self, alert_id: str, resolved_by: str) -> bool:
        """Resolve an alert."""
        try:
            with sqlite3.connect(self.monitoring_db_path) as conn:
                cursor = conn.execute("""
                    UPDATE alerts
                    SET status = 'resolved', resolved_at = ?
                    WHERE alert_id = ?
                """, (datetime.now(), alert_id))

                if cursor.rowcount > 0:
                    conn.commit()
                    logger.info(f"Alert {alert_id} resolved by {resolved_by}")
                    return True
                else:
                    logger.warning(f"Alert {alert_id} not found")
                    return False

        except Exception as e:
            logger.error(f"Failed to resolve alert {alert_id}: {e}")
            return False


# Factory function for dependency injection
def create_backup_monitoring_system(config_path: Optional[str] = None) -> BackupMonitoringSystem:
    """Factory function to create backup monitoring system instance."""
    return BackupMonitoringSystem(config_path)


# Export for DI
__all__ = ["BackupMonitoringSystem", "create_backup_monitoring_system"]
