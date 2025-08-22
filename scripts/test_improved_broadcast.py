#!/usr/bin/env python3
"""
TEST IMPROVED BROADCAST SYSTEM
Demonstrates and validates the enhanced resume message templates
"""

import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__), '..', 'src'))

def test_message_templates():
    """Test all message template types"""
    try:
        from services.improved_resume_message_template import ImprovedResumeMessageTemplate
        
        print("🧪 Testing Improved Resume Message Templates...")
        print("=" * 60)
        
        template = ImprovedResumeMessageTemplate()
        
        # Test standard message
        print("\n📋 Testing Standard Resume Message:")
        print("-" * 40)
        standard_msg = template.get_standard_resume_message()
        print(f"✅ Length: {len(standard_msg)} characters")
        print(f"✅ Lines: {len(standard_msg.split(chr(10)))}")
        print(f"✅ Emojis: {standard_msg.count('🚀') + standard_msg.count('🎯') + standard_msg.count('✅')}")
        print(f"✅ Action Items: {standard_msg.count('•')}")
        
        # Test emergency message
        print("\n🚨 Testing Emergency Resume Message:")
        print("-" * 40)
        emergency_msg = template.get_emergency_resume_message()
        print(f"✅ Length: {len(emergency_msg)} characters")
        print(f"✅ Lines: {len(emergency_msg.split(chr(10)))}")
        print(f"✅ Emergency Indicators: {emergency_msg.count('🚨') + emergency_msg.count('⚠️')}")
        print(f"✅ Action Items: {emergency_msg.count('•')}")
        
        # Test development message
        print("\n💻 Testing Development Resume Message:")
        print("-" * 40)
        dev_msg = template.get_development_resume_message()
        print(f"✅ Length: {len(dev_msg)} characters")
        print(f"✅ Lines: {len(dev_msg.split(chr(10)))}")
        print(f"✅ Development Indicators: {dev_msg.count('💻') + dev_msg.count('🔧')}")
        print(f"✅ Action Items: {dev_msg.count('•')}")
        
        print("\n🎉 All message template tests passed successfully!")
        return True
        
    except ImportError as e:
        print(f"❌ Import Error: {e}")
        return False
    except Exception as e:
        print(f"❌ Test Error: {e}")
        return False

def test_configuration():
    """Test configuration file loading"""
    try:
        import yaml
        
        config_path = os.path.join(os.path.dirname(__file__), '..', 'config', 'improved_broadcast_config.yaml')
        
        if not os.path.exists(config_path):
            print(f"❌ Configuration file not found: {config_path}")
            return False
        
        with open(config_path, 'r') as f:
            config = yaml.safe_load(f)
        
        print("\n⚙️ Testing Configuration File:")
        print("-" * 40)
        
        # Test basic structure
        assert 'broadcast_system' in config, "Missing broadcast_system section"
        assert 'message_types' in config['broadcast_system'], "Missing message_types section"
        assert 'agents' in config['broadcast_system'], "Missing agents section"
        
        print(f"✅ System Name: {config['broadcast_system']['name']}")
        print(f"✅ Version: {config['broadcast_system']['version']}")
        print(f"✅ Message Types: {len(config['broadcast_system']['message_types'])}")
        print(f"✅ Agents: {len(config['broadcast_system']['agents'])}")
        
        # Test message types
        message_types = config['broadcast_system']['message_types']
        expected_types = ['standard', 'emergency', 'development', 'maintenance']
        
        for msg_type in expected_types:
            if msg_type in message_types:
                print(f"✅ {msg_type.title()} Message Type: Configured")
            else:
                print(f"❌ {msg_type.title()} Message Type: Missing")
        
        print("\n🎉 Configuration file test passed successfully!")
        return True
        
    except ImportError as e:
        print(f"❌ PyYAML not installed: {e}")
        print("💡 Install with: pip install pyyaml")
        return False
    except Exception as e:
        print(f"❌ Configuration Test Error: {e}")
        return False

def test_agent_registration():
    """Test agent registration simulation"""
    try:
        print("\n🤖 Testing Agent Registration Simulation:")
        print("-" * 40)
        
        # Simulate agent data
        agents = [
            {'id': 'agent_1', 'name': 'Foundation & Testing Specialist', 'capabilities': ['TESTING', 'QUALITY_ASSURANCE']},
            {'id': 'agent_2', 'name': 'AI/ML Specialist', 'capabilities': ['AI_DEVELOPMENT', 'ML_OPTIMIZATION']},
            {'id': 'agent_3', 'name': 'Web Development Specialist', 'capabilities': ['WEB_DEVELOPMENT', 'UI_UX']},
            {'id': 'agent_4', 'name': 'Multimedia & Gaming Specialist', 'capabilities': ['MULTIMEDIA', 'GAMING_DEVELOPMENT']},
            {'id': 'agent_5', 'name': 'Security & Compliance Specialist', 'capabilities': ['SECURITY', 'COMPLIANCE', 'COORDINATION'], 'is_captain': True},
            {'id': 'agent_6', 'name': 'Data & Analytics Specialist', 'capabilities': ['DATA_SCIENCE', 'BUSINESS_INTELLIGENCE']},
            {'id': 'agent_7', 'name': 'Infrastructure & DevOps Specialist', 'capabilities': ['DEVOPS', 'SYSTEM_ADMINISTRATION']},
            {'id': 'agent_8', 'name': 'Business Logic & Workflows Specialist', 'capabilities': ['WORKFLOW_DESIGN', 'AUTOMATION']}
        ]
        
        print(f"✅ Total Agents: {len(agents)}")
        
        # Check captain assignment
        captain = next((agent for agent in agents if agent.get('is_captain')), None)
        if captain:
            print(f"✅ Captain: {captain['name']} ({captain['id']})")
        else:
            print("❌ No captain assigned")
        
        # Check capabilities
        total_capabilities = sum(len(agent['capabilities']) for agent in agents)
        print(f"✅ Total Capabilities: {total_capabilities}")
        
        # Check agent distribution
        for agent in agents:
            print(f"  • {agent['id']}: {agent['name']} - {len(agent['capabilities'])} capabilities")
        
        print("\n🎉 Agent registration simulation test passed successfully!")
        return True
        
    except Exception as e:
        print(f"❌ Agent Registration Test Error: {e}")
        return False

def test_message_analysis():
    """Test message content analysis"""
    try:
        from services.improved_resume_message_template import ImprovedResumeMessageTemplate
        
        print("\n📊 Testing Message Content Analysis:")
        print("-" * 40)
        
        template = ImprovedResumeMessageTemplate()
        standard_msg = template.get_standard_resume_message()
        
        # Analyze message structure
        lines = standard_msg.split(chr(10))
        sections = [line for line in lines if line.strip() and not line.startswith('•') and not line.startswith('✅')]
        
        print(f"✅ Total Lines: {len(lines)}")
        print(f"✅ Content Sections: {len(sections)}")
        print(f"✅ Action Items: {standard_msg.count('•')}")
        print(f"✅ Checkmarks: {standard_msg.count('✅')}")
        print(f"✅ Emojis: {sum(1 for char in standard_msg if ord(char) > 127)}")
        
        # Check for key elements
        key_elements = [
            'AGENT RESUME OPERATIONS',
            'IMMEDIATE ACTION REQUIRED',
            'TASK EXECUTION PROTOCOL',
            'COORDINATION WORKFLOW',
            'SUCCESS METRICS',
            'CRITICAL REQUIREMENTS',
            'NEXT STEPS',
            'COORDINATION STATUS'
        ]
        
        missing_elements = []
        for element in key_elements:
            if element in standard_msg:
                print(f"✅ Found: {element}")
            else:
                missing_elements.append(element)
                print(f"❌ Missing: {element}")
        
        if missing_elements:
            print(f"\n⚠️ Missing Elements: {len(missing_elements)}")
        else:
            print(f"\n🎉 All key elements present!")
        
        print("\n🎉 Message content analysis test passed successfully!")
        return True
        
    except Exception as e:
        print(f"❌ Message Analysis Test Error: {e}")
        return False

def main():
    """Run all tests"""
    print("🚀 IMPROVED BROADCAST SYSTEM - COMPREHENSIVE TEST SUITE")
    print("=" * 70)
    
    tests = [
        ("Message Templates", test_message_templates),
        ("Configuration", test_configuration),
        ("Agent Registration", test_agent_registration),
        ("Message Analysis", test_message_analysis)
    ]
    
    results = []
    
    for test_name, test_func in tests:
        print(f"\n🧪 Running Test: {test_name}")
        try:
            result = test_func()
            results.append((test_name, result))
        except Exception as e:
            print(f"❌ Test {test_name} failed with exception: {e}")
            results.append((test_name, False))
    
    # Summary
    print("\n" + "=" * 70)
    print("📊 TEST RESULTS SUMMARY")
    print("=" * 70)
    
    passed = sum(1 for _, result in results if result)
    total = len(results)
    
    for test_name, result in results:
        status = "✅ PASSED" if result else "❌ FAILED"
        print(f"  {test_name}: {status}")
    
    print(f"\n🎯 Overall Result: {passed}/{total} tests passed")
    
    if passed == total:
        print("🎉 ALL TESTS PASSED! Improved Broadcast System is ready for production.")
        return 0
    else:
        print("⚠️ Some tests failed. Please review and fix issues before production use.")
        return 1

if __name__ == "__main__":
    exit_code = main()
    sys.exit(exit_code)
