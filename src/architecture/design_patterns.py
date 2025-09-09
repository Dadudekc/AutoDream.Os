"""
Unified Design Patterns - KISS Principle Implementation
======================================================

Essential design patterns consolidated into a single, simple module.
Follows KISS principle: Keep It Simple, Stupid.

V2 Compliance: < 150 lines, single responsibility.

Author: Agent-2 (Architecture & Design Specialist) - KISS Leadership
License: MIT
"""
import logging
from dataclasses import dataclass
from datetime import datetime
from enum import Enum
from typing import Any
logger = logging.getLogger(__name__)


class PatternType(Enum):
    """Design pattern type enumeration."""
    SINGLETON = 'singleton'
    FACTORY = 'factory'
    OBSERVER = 'observer'
    STRATEGY = 'strategy'
    ADAPTER = 'adapter'


@dataclass
class DesignPattern:
    """Design pattern data structure."""
    name: str
    pattern_type: PatternType
    description: str
    implementation: str
    use_cases: list[str]


class UnifiedDesignPatterns:
    """
    Unified Design Patterns - Essential patterns only.

    Consolidates all design patterns into a single, simple module
    following KISS principles.
    """

    def __init__(self):
        """Initialize unified design patterns."""
        self.patterns: dict[str, DesignPattern] = {}
        self.logger = logging.getLogger(__name__)
        self._initialize_patterns()

    def _initialize_patterns(self):
        """Initialize essential design patterns."""
        self.patterns['singleton'] = DesignPattern(name='Singleton',
            pattern_type=PatternType.SINGLETON, description=
            'Ensure only one instance of a class exists', implementation=
            """class Singleton:
    _instance = None
    def __new__(cls):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
        return cls._instance"""
            , use_cases=['Configuration managers', 'Database connections',
            'Logging systems'])
        self.patterns['factory'] = DesignPattern(name='Factory',
            pattern_type=PatternType.FACTORY, description=
            'Create objects without specifying their exact class',
            implementation=
            """class ObjectFactory:
    @staticmethod
    def create_object(object_type):
        if object_type == 'type1':
            return Type1Object()
        elif object_type == 'type2':
            return Type2Object()
        return None"""
            , use_cases=['Object creation', 'Plugin systems',
            'Database drivers'])
        self.patterns['observer'] = DesignPattern(name='Observer',
            pattern_type=PatternType.OBSERVER, description=
            'Notify multiple objects about state changes', implementation=
            """class Subject:
    def __init__(self):
        self._observers = []
    def attach(self, observer):
        self._observers.append(observer)
    def notify(self):
        for observer in self._observers:
            observer.update()"""
            , use_cases=['Event systems', 'Model-View architectures',
            'Notification systems'])

    def get_pattern(self, name: str) ->(DesignPattern | None):
        """Get design pattern by name."""
        return self.patterns.get(name.lower())

    def list_patterns(self) ->list[DesignPattern]:
        """List all available design patterns."""
        return list(self.patterns.values())

    def get_pattern_by_type(self, pattern_type: PatternType) ->list[
        DesignPattern]:
        """Get patterns by type."""
        return [pattern for pattern in self.patterns.values() if pattern.
            pattern_type == pattern_type]

    def apply_pattern(self, pattern_name: str, context: dict[str, Any]) ->dict[
        str, Any]:
        """Apply design pattern in given context."""
        pattern = self.get_pattern(pattern_name)
        if not pattern:
            return {'error': f"Pattern '{pattern_name}' not found"}
        try:
            result = {'pattern': pattern.name, 'type': pattern.pattern_type
                .value, 'applied': True, 'context': context, 'timestamp':
                datetime.now().isoformat()}
            self.logger.info(f'✅ Applied pattern: {pattern.name}')
            return result
        except Exception as e:
            self.logger.error(f'❌ Failed to apply pattern {pattern_name}: {e}')
            return {'error': str(e), 'pattern': pattern_name}

    def get_pattern_recommendations(self, use_case: str) ->list[DesignPattern]:
        """Get pattern recommendations for specific use case."""
        recommendations = []
        for pattern in self.patterns.values():
            if any(use_case.lower() in case.lower() for case in pattern.
                use_cases):
                recommendations.append(pattern)
        return recommendations


def main():
    """Main function for unified design patterns."""
    logger.info('🎨 Unified Design Patterns - KISS Implementation')
    logger.info('=' * 50)
    patterns = UnifiedDesignPatterns()
    available_patterns = patterns.list_patterns()
    logger.info(f'📋 Available patterns: {len(available_patterns)}')
    for pattern in available_patterns:
        logger.info(f'  • {pattern.name} ({pattern.pattern_type.value})')
    recommendations = patterns.get_pattern_recommendations('configuration')
    logger.info(
        f"\n💡 Recommendations for 'configuration': {len(recommendations)}")
    for rec in recommendations:
        logger.info(f'  • {rec.name}: {rec.description}')
    return {'patterns_count': len(available_patterns), 'recommendations':
        len(recommendations)}


if __name__ == '__main__':
    main()
