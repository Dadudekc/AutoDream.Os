"""Command Handler - V2 Compliance Module."""
import logging
import time
from typing import Any
try:
    from ..agent_registry import format_agent_list
    from ..utils.agent_registry import list_agents as registry_list_agents
except ImportError:

    def format_agent_list(agents):
        return '\n'.join(f'• {agent}' for agent in agents)

    def registry_list_agents():
        return [f'Agent-{i}' for i in range(1, 9)]


class CommandHandler:
    """Handler for CLI command processing and response handling."""

    def can_handle(self, args) -> bool:
        """Check if this handler can handle the given arguments."""
        return False  # Base handler doesn't handle anything specific

    def __init__(self) ->None:
        """Initialize command handler."""
        self.logger = logging.getLogger(__name__)
        self.command_count = 0
        self.successful_commands = 0
        self.failed_commands = 0
        self.command_history: list[dict[str, Any]] = []

    async def process_command(self, command: str, args: dict[str, Any],
        coordinate_handler, message_handler, service) ->dict[str, Any]:
        """Process CLI command."""
        try:
            self.command_count += 1
            start_time = time.time()
            if command == 'coordinates':
                result = await self._handle_coordinates_command(
                    coordinate_handler)
            elif command == 'list_agents':
                agents = registry_list_agents()
                formatted = format_agent_list(agents)
                count = formatted['data']['agent_count']
                logger.info(f'\n🤖 Available Agents ({count}):')
                for agent in formatted['data']['agents']:
                    logger.info(f'  - {agent}')
                result = formatted
            elif command == 'send_message':
                result = await self._handle_send_message_command(args,
                    message_handler, service)
            elif command == 'bulk_message':
                result = await self._handle_bulk_message_command(args,
                    message_handler, service)
            elif command == 'status':
                result = await self._handle_status_command()
            else:
                result = {'success': False, 'error':
                    f'Unknown command: {command}'}
            execution_time = time.time() - start_time
            if result.get('success', False):
                self.successful_commands += 1
            else:
                self.failed_commands += 1
            self.command_history.append({'command': command, 'args': args,
                'success': result.get('success', False), 'execution_time':
                execution_time, 'timestamp': time.time()})
            if len(self.command_history) > 100:
                self.command_history.pop(0)
            return result
        except Exception as e:
            self.failed_commands += 1
            self.logger.error(f'Error processing command {command}: {e}')
            return {'success': False, 'error': str(e)}

    async def _handle_coordinates_command(self, coordinate_handler) ->dict[
        str, Any]:
        """Handle coordinates command."""
        try:
            result = await coordinate_handler.load_coordinates_async()
            if result.get('success', False):
                coordinate_handler.print_coordinates_table(result[
                    'coordinates'])
            return result
        except Exception as e:
            return {'success': False, 'error': str(e)}

    async def _handle_send_message_command(self, args: dict[str, Any],
        message_handler, service) ->dict[str, Any]:
        """Handle send message command."""
        try:
            message_data = message_handler.create_message_data(recipient=
                args.get('recipient', ''), message=args.get('message', ''),
                sender=args.get('sender', 'Captain Agent-4'), message_type=
                args.get('message_type', 'text'), priority=args.get(
                'priority', 'regular'), tags=args.get('tags', []))
            return await message_handler.send_message_async(service,
                message_data)
        except Exception as e:
            return {'success': False, 'error': str(e)}

    async def _handle_bulk_message_command(self, args: dict[str, Any],
        message_handler, service) ->dict[str, Any]:
        """Handle bulk message command."""
        try:
            coordinate_handler = args.get('coordinate_handler')
            if not coordinate_handler:
                return {'success': False, 'error':
                    'Coordinate handler not provided'}
            coords_result = await coordinate_handler.load_coordinates_async()
            if not coords_result.get('success', False):
                return coords_result
            agents = list(coords_result['coordinates'].keys())
            results = []
            for agent in agents:
                message_data = message_handler.create_message_data(recipient
                    =agent, message=args.get('message', ''), sender=args.
                    get('sender', 'Captain Agent-4'), message_type=args.get
                    ('message_type', 'broadcast'), priority=args.get(
                    'priority', 'regular'), tags=args.get('tags', []))
                result = await message_handler.send_message_async(service,
                    message_data)
                results.append({'agent': agent, 'result': result})
            return {'success': True, 'results': results, 'total_agents':
                len(agents)}
        except Exception as e:
            return {'success': False, 'error': str(e)}

    async def _handle_status_command(self) ->dict[str, Any]:
        """Handle status command."""
        try:
            stats = self.get_command_statistics()
            logger.info('\n📊 Command Statistics:')
            logger.info(f"  Total Commands: {stats['total_commands']}")
            logger.info(f"  Successful: {stats['successful_commands']}")
            logger.info(f"  Failed: {stats['failed_commands']}")
            logger.info(f"  Success Rate: {stats['success_rate']:.1f}%")
            return {'success': True, 'statistics': stats}
        except Exception as e:
            return {'success': False, 'error': str(e)}

    def get_command_statistics(self) ->dict[str, Any]:
        """Get command processing statistics."""
        total = self.command_count
        success_rate = (self.successful_commands / total * 100 if total > 0
             else 0)
        return {'total_commands': total, 'successful_commands': self.
            successful_commands, 'failed_commands': self.failed_commands,
            'success_rate': success_rate, 'recent_commands': self.
            command_history[-10:] if len(self.command_history) > 10 else
            self.command_history}


MessageCommandHandler = CommandHandler
