#!/usr/bin/env python3
"""
Test script with dry-run mode to verify MessagingGateway functionality
"""
import asyncio
import sys
import os
sys.path.append('src')

from integration.messaging_gateway import MessagingGateway

async def test_message_dry_run():
    print('🔧 Testing MessagingGateway (DRY RUN MODE)...')
    print('=' * 50)

    try:
        # Initialize gateway in dry-run mode
        gateway = MessagingGateway(dry_run=True)
        print('✅ MessagingGateway initialized (DRY RUN)')

        # Send test message to Agent-4
        print('📨 Sending test message to Agent-4 (DRY RUN)...')

        result = await gateway.send(
            agent_key='Agent-4',
            message='DRY RUN TEST: This is a test message to verify messaging functionality',
            meta={
                'source': 'system_test',
                'message_type': 'general_to_agent',
                'author_tag': 'SystemTest-Agent4'
            }
        )

        print('✅ Message processed successfully!')
        print('-' * 30)
        print(f'Status: {result.get("status")}')
        print(f'Agent: {result.get("agent")}')
        print(f'Backend: {result.get("backend")}')
        print(f'Request ID: {result.get("request_id")}')
        print(f'Timestamp: {result.get("timestamp")}')
        print(f'Extra: {result.get("extra")}')

        if result.get("status") == "skipped":
            print('🎯 DRY RUN SUCCESSFUL - No UI interaction attempted')
        else:
            print('⚠️  Unexpected status in dry run mode')

        return result

    except Exception as e:
        print(f'❌ Test failed with error: {e}')
        import traceback
        traceback.print_exc()
        return None

if __name__ == "__main__":
    print('🚀 Starting MessagingGateway DRY RUN Test')
    result = asyncio.run(test_message_dry_run())
    print('=' * 50)
    print('🏁 DRY RUN Test completed')
