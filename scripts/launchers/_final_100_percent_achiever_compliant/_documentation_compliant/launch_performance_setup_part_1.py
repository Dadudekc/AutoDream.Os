"""
launch_performance_setup_part_1.py
Module: launch_performance_setup_part_1.py
Purpose: Automated documentation compliance
Created: 2025-08-31 00:37:00
"""

# Part 1 of launch_performance_setup.py
# Original file: .\scripts\launchers\launch_performance_setup.py

    """Initialize performance monitor and add collectors."""
    try:
        perf_monitor = PerformanceMonitor(config_file)
        collectors_config = config.get("performance_monitoring", {}).get("collectors", {})

        # System metrics collector
        if collectors_config.get("system_metrics", {}).get("enabled", True):
            sys_conf = collectors_config.get("system_metrics", {})
            system_collector = SystemMetricsCollector(
                collection_interval=sys_conf.get("collection_interval", 30)
            )
            system_collector.collect_cpu = sys_conf.get("collect_cpu", True)
            system_collector.collect_memory = sys_conf.get("collect_memory", True)
            system_collector.collect_disk = sys_conf.get("collect_disk", True)
            system_collector.collect_network = sys_conf.get("collect_network", True)
            perf_monitor.add_collector(system_collector)
            logger.info("System metrics collector added")

        # Application metrics collector
        if collectors_config.get("application_metrics", {}).get("enabled", True):
            app_conf = collectors_config.get("application_metrics", {})
            app_collector = ApplicationMetricsCollector(
                collection_interval=app_conf.get("collection_interval", 60)
            )
            perf_monitor.add_collector(app_collector)
            logger.info("Application metrics collector added")

        # Network metrics collector
        if collectors_config.get("network_metrics", {}).get("enabled", True):
            net_conf = collectors_config.get("network_metrics", {})
            network_collector = NetworkMetricsCollector(
                collection_interval=net_conf.get("collection_interval", 60)
            )
            for port in net_conf.get("monitored_ports", []):
                network_collector.add_monitored_port(port)
            perf_monitor.add_collector(network_collector)
            logger.info("Network metrics collector added")

        # Custom metrics collector
        if collectors_config.get("custom_metrics", {}).get("enabled", True):
            cust_conf = collectors_config.get("custom_metrics", {})
            custom_collector = CustomMetricsCollector(
                collection_interval=cust_conf.get("collection_interval", 120)
            )
            for metric_name in cust_conf.get("metrics", {}).keys():
                custom_collector.add_custom_metric(metric_name, lambda: 100.0)
            perf_monitor.add_collector(custom_collector)
            logger.info("Custom metrics collector added")

        return perf_monitor

