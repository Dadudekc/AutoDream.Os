# Messaging Systems Inventory

_Last generated: 2025-09-12T23:05:58.143789Z_

This document provides a comprehensive inventory of all messaging systems in the Agent Cellphone V2 repository. It is automatically generated from the messaging systems registry.

## 📊 Overview

- **Total Systems**: 19
- **Healthy Systems**: 7
- **Unhealthy Systems**: 12
- **Critical Systems**: 4/10 healthy

## 🏥 Health Status

- **Overall Health**: 7/19 (36.8%)
- **Critical Systems**: 4/10 (40.0%)

### By Category:
- **Ai**: 0/2 (0.0%)
- **Cli**: 2/4 (50.0%)
- **Core**: 3/4 (75.0%)
- **External**: 1/4 (25.0%)
- **Supporting**: 1/5 (20.0%)

## 📋 Systems Inventory

| Status | ID | Name | Category | Module.Entrypoint | Critical |
|---|---|---|---|---|---|
| ⚠️ | `thea_comm_manager` | Thea Communication Manager | `ai` | `src.services.thea.communication.communication_manager.TheaCommunicationMan...` | 🟡 |
| ⚠️ | `thea_messaging_service` | Thea Messaging Service | `ai` | `src.services.thea.messaging.thea_messaging_service.TheaMessagingService...` | 🟡 |
| ❌ | `fallback_delivery` | Fallback Delivery | `cli` | `src.services.messaging.providers.fallback_provider.FallbackDeliveryProv...` | 🔴 |
| ✅ | `messaging_cli` | Messaging CLI | `cli` | `src.services.messaging.cli.messaging_cli.MessagingCLI...` | 🟡 |
| ⚠️ | `messaging_perf_cli` | Messaging Performance CLI | `cli` | `src.services.messaging.cli.perf_cli.PerfCLI` | 🟡 |
| ✅ | `swarm_onboarding_script` | Swarm Onboarding Script | `cli` | `swarm_onboarding.main` | 🟡 |
| ✅ | `consolidated_messaging_service` | Consolidated Messaging Service | `core` | `src.services.messaging.consolidated_messaging_service.ConsolidatedMessagin...` | 🔴 |
| ✅ | `inbox_delivery` | Inbox Delivery Provider | `core` | `src.services.messaging.providers.inbox_delivery.InboxMessageDelivery...` | 🟡 |
| ❌ | `messaging_interfaces` | Messaging Interfaces | `core` | `src.services.messaging.interfaces.messaging_interfaces.MessagingProvider...` | 🔴 |
| ✅ | `pyautogui_delivery` | PyAutoGUI Delivery Provider | `core` | `src.services.messaging.providers.pyautogui_delivery.PyAutoGUIMessageDeli...` | 🔴 |
| ✅ | `discord_agent_bot` | Discord Agent Bot | `external` | `src.discord_commander.discord_agent_bot.DiscordAgentBot...` | 🔴 |
| ❌ | `discord_comm_engine` | Discord Communication Engine | `external` | `src.discord_commander.communication_engine.DiscordCommunication...` | 🔴 |
| ⚠️ | `discord_webhook` | Discord Webhook Integration | `external` | `src.discord_commander.webhook.send_webhook` | 🟡 |
| ❌ | `messaging_gateway` | Messaging Gateway (Discord↔PyAutoGUI) | `external` | `src.discord_commander.messaging_gateway.MessagingGateway...` | 🔴 |
| ❌ | `broadcast_service` | Broadcast Service | `supporting` | `src.services.messaging.broadcast_service.BroadcastService...` | 🔴 |
| ✅ | `coordinate_service` | Coordinate Service | `supporting` | `src.core.coordinate_loader.get_coordinate_loader` | 🔴 |
| ❌ | `message_history_service` | Message History Service | `supporting` | `src.services.messaging.history_service.MessageHistoryServic...` | 🔴 |
| ⚠️ | `onboarding_bridge` | Onboarding Bridge | `supporting` | `src.onboarding.onboarding_bridge.OnboardingBridge...` | 🟡 |
| ⚠️ | `task_handlers` | Task Handlers | `supporting` | `src.services.messaging.task_handlers.TaskHandlers...` | 🟡 |

## 🔧 Ai Systems

### Thea Communication Manager
**ID**: `thea_comm_manager`
**Status**: ⚠️ **Non-Critical Issue**
**Module**: `src.services.thea.communication.communication_manager.TheaCommunicationManager`
**Critical**: No

**Error**: IndentationError: expected an indented block after function definition on line 81 (thea_config.py, line 83)

### Thea Messaging Service
**ID**: `thea_messaging_service`
**Status**: ⚠️ **Non-Critical Issue**
**Module**: `src.services.thea.messaging.thea_messaging_service.TheaMessagingService`
**Critical**: No

**Error**: IndentationError: expected an indented block after function definition on line 81 (thea_config.py, line 83)

## 🔧 Cli Systems

### Fallback Delivery
**ID**: `fallback_delivery`
**Status**: ❌ **Critical Failure**
**Module**: `src.services.messaging.providers.fallback_provider.FallbackDeliveryProvider`
**Critical**: Yes

**Error**: ImportError: Failed to import module src.services.messaging.providers.fallback_provider: No module named 'src.services.messaging.providers.fallback_provider'

### Messaging CLI
**ID**: `messaging_cli`
**Status**: ✅ **Healthy**
**Module**: `src.services.messaging.cli.messaging_cli.MessagingCLI`
**Critical**: No

### Messaging Performance CLI
**ID**: `messaging_perf_cli`
**Status**: ⚠️ **Non-Critical Issue**
**Module**: `src.services.messaging.cli.perf_cli.PerfCLI`
**Critical**: No

**Error**: ImportError: Failed to import module src.services.messaging.cli.perf_cli: No module named 'src.services.messaging.cli.perf_cli'

### Swarm Onboarding Script
**ID**: `swarm_onboarding_script`
**Status**: ✅ **Healthy**
**Module**: `swarm_onboarding.main`
**Critical**: No

## 🔧 Core Systems

### Consolidated Messaging Service
**ID**: `consolidated_messaging_service`
**Status**: ✅ **Healthy**
**Module**: `src.services.messaging.consolidated_messaging_service.ConsolidatedMessagingService`
**Critical**: Yes

### Inbox Delivery Provider
**ID**: `inbox_delivery`
**Status**: ✅ **Healthy**
**Module**: `src.services.messaging.providers.inbox_delivery.InboxMessageDelivery`
**Critical**: No

### Messaging Interfaces
**ID**: `messaging_interfaces`
**Status**: ❌ **Critical Failure**
**Module**: `src.services.messaging.interfaces.messaging_interfaces.MessagingProvider`
**Critical**: Yes

**Error**: AttributeError: Entrypoint MessagingProvider not found in src.services.messaging.interfaces.messaging_interfaces: module 'src.services.messaging.interfaces.messaging_interfaces' has no attribute 'MessagingProvider'

### PyAutoGUI Delivery Provider
**ID**: `pyautogui_delivery`
**Status**: ✅ **Healthy**
**Module**: `src.services.messaging.providers.pyautogui_delivery.PyAutoGUIMessageDelivery`
**Critical**: Yes

## 🔧 External Systems

### Discord Agent Bot
**ID**: `discord_agent_bot`
**Status**: ✅ **Healthy**
**Module**: `src.discord_commander.discord_agent_bot.DiscordAgentBot`
**Critical**: Yes

### Discord Communication Engine
**ID**: `discord_comm_engine`
**Status**: ❌ **Critical Failure**
**Module**: `src.discord_commander.communication_engine.DiscordCommunicationEngine`
**Critical**: Yes

**Error**: ImportError: Failed to import module src.discord_commander.communication_engine: No module named 'src.discord_commander.communication_engine'

### Discord Webhook Integration
**ID**: `discord_webhook`
**Status**: ⚠️ **Non-Critical Issue**
**Module**: `src.discord_commander.webhook.send_webhook`
**Critical**: No

**Error**: ImportError: Failed to import module src.discord_commander.webhook: No module named 'src.discord_commander.webhook'

### Messaging Gateway (Discord↔PyAutoGUI)
**ID**: `messaging_gateway`
**Status**: ❌ **Critical Failure**
**Module**: `src.discord_commander.messaging_gateway.MessagingGateway`
**Critical**: Yes

**Error**: ImportError: Failed to import module src.discord_commander.messaging_gateway: No module named 'src.discord_commander.messaging_gateway'

## 🔧 Supporting Systems

### Broadcast Service
**ID**: `broadcast_service`
**Status**: ❌ **Critical Failure**
**Module**: `src.services.messaging.broadcast_service.BroadcastService`
**Critical**: Yes

**Error**: ImportError: Failed to import module src.services.messaging.broadcast_service: No module named 'src.services.messaging.broadcast_service'

### Coordinate Service
**ID**: `coordinate_service`
**Status**: ✅ **Healthy**
**Module**: `src.core.coordinate_loader.get_coordinate_loader`
**Critical**: Yes

### Message History Service
**ID**: `message_history_service`
**Status**: ❌ **Critical Failure**
**Module**: `src.services.messaging.history_service.MessageHistoryService`
**Critical**: Yes

**Error**: ImportError: Failed to import module src.services.messaging.history_service: No module named 'src.services.messaging.history_service'

### Onboarding Bridge
**ID**: `onboarding_bridge`
**Status**: ⚠️ **Non-Critical Issue**
**Module**: `src.onboarding.onboarding_bridge.OnboardingBridge`
**Critical**: No

**Error**: ImportError: Failed to import module src.onboarding.onboarding_bridge: No module named 'src.onboarding'

### Task Handlers
**ID**: `task_handlers`
**Status**: ⚠️ **Non-Critical Issue**
**Module**: `src.services.messaging.task_handlers.TaskHandlers`
**Critical**: No

**Error**: ImportError: Failed to import module src.services.messaging.task_handlers: cannot import name 'map_priority' from 'src.services.messaging.models' (D:\Agent_Cellphone_V2_Repository\src\services\messaging\models\__init__.py)


## 🛠️ Tools

This inventory is generated using the messaging systems registry tools:

- **Registry**: `config/messaging_systems.yaml`
- **Schema**: `config/messaging_systems.schema.json`
- **Health Check**: `python -m scripts.messaging.doctor`
- **Stub Generator**: `python -m scripts.messaging.generate_stubs`
- **Documentation**: `python -m scripts.messaging.generate_docs`

## 📝 Notes

- ✅ = System is healthy and importable
- ❌ = Critical system with import failures
- ⚠️ = Non-critical system with issues
- 🔴 = Critical system (must be healthy for operations)
- 🟡 = Non-critical system (can have issues)

This document is automatically generated and should not be edited manually.
