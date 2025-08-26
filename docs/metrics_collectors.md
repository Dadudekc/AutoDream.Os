# Metrics Collector Requirements

This document describes the built-in metric collectors and the units they produce.

## SystemMetricsCollector
* **Requirements:** [`psutil`](https://pypi.org/project/psutil/)
* **Metrics:**
  * `cpu_usage_percent` – percent
  * `memory_usage_percent` – percent
  * `disk_usage_percent` – percent

## ApplicationMetricsCollector
* **Metrics:**
  * `app_uptime_seconds` – seconds
  * `event_loop_tasks` – count

## NetworkMetricsCollector
* **Requirements:** `psutil`
* **Metrics:**
  * `network_bytes_sent` – bytes
  * `network_bytes_recv` – bytes

## CustomMetricsCollector
* Collects user-defined metrics via callables.
* Units are determined by the provided functions.
