#!/usr/bin/env python3
"""
Internationalization Manager for Agent Cellphone V2
Handles multi-language support, localization, and cultural adaptation
"""

import json
import os
import sys
import argparse

from src.utils.stability_improvements import stability_manager, safe_import
from pathlib import Path
from typing import Dict, List, Optional, Any
from dataclasses import dataclass, asdict
from enum import Enum
import locale
import gettext
from datetime import datetime
import threading
import time

# Add src to path for imports
src_path = Path(__file__).parent.parent
sys.path.insert(0, str(src_path))

from core.persistent_data_storage import (
    PersistentDataStorage,
    StorageType,
    DataIntegrityLevel,
)


class LanguageCode(Enum):
    """Supported language codes"""

    EN = "en"  # English
    ES = "es"  # Spanish
    FR = "fr"  # French
    DE = "de"  # German
    IT = "it"  # Italian
    PT = "pt"  # Portuguese
    RU = "ru"  # Russian
    ZH = "zh"  # Chinese
    JA = "ja"  # Japanese
    KO = "ko"  # Korean
    AR = "ar"  # Arabic
    HI = "hi"  # Hindi


class CulturalRegion(Enum):
    """Cultural regions for adaptation"""

    NORTH_AMERICA = "north_america"
    EUROPE = "europe"
    ASIA_PACIFIC = "asia_pacific"
    LATIN_AMERICA = "latin_america"
    MIDDLE_EAST = "middle_east"
    AFRICA = "africa"
    OCEANIA = "oceania"


class LocalizationLevel(Enum):
    """Localization depth levels"""

    BASIC = "basic"  # Text translation only
    STANDARD = "standard"  # Text + date/time formats
    ADVANCED = "advanced"  # Text + formats + cultural norms
    FULL = "full"  # Complete cultural adaptation


@dataclass
class LanguageConfig:
    """Language configuration data"""

    language_code: str
    display_name: str
    native_name: str
    script_direction: str  # ltr or rtl
    date_format: str
    time_format: str
    number_format: str
    currency_symbol: str
    decimal_separator: str
    thousands_separator: str


@dataclass
class CulturalConfig:
    """Cultural configuration data"""

    region: str
    cultural_norms: Dict[str, Any]
    communication_style: str
    formality_levels: List[str]
    color_preferences: Dict[str, str]
    taboos: List[str]
    celebrations: List[str]


@dataclass
class LocalizationData:
    """Localization data structure"""

    language_code: str
    cultural_region: str
    translations: Dict[str, str]
    formats: Dict[str, str]
    cultural_adaptations: Dict[str, Any]
    last_updated: str


class InternationalizationManager:
    """
    Manages multi-language support, localization, and cultural adaptation
    for global agent swarm operations
    """

    def __init__(self, storage: Optional[PersistentDataStorage] = None):
        """Initialize the internationalization manager"""
        self.storage = storage or PersistentDataStorage()
        self.current_language = LanguageCode.EN
        self.current_region = CulturalRegion.NORTH_AMERICA
        self.localization_level = LocalizationLevel.STANDARD

        # Language and cultural configurations
        self.language_configs: Dict[str, LanguageConfig] = {}
        self.cultural_configs: Dict[str, CulturalConfig] = {}
        self.localization_data: Dict[str, LocalizationData] = {}

        # Translation cache
        self.translation_cache: Dict[str, str] = {}
        self.cache_lock = threading.Lock()

        # Initialize system
        self._initialize_internationalization()
        self._load_language_configs()
        self._load_cultural_configs()
        self._setup_gettext()

    def _initialize_internationalization(self):
        """Initialize internationalization system"""
        # Create localization directories
        loc_dirs = [
            "localization",
            "localization/languages",
            "localization/cultures",
            "localization/translations",
            "localization/formats",
        ]

        for dir_path in loc_dirs:
            Path(dir_path).mkdir(parents=True, exist_ok=True)

        # Initialize storage for internationalization data
        self.storage.store_data(
            "i18n_config",
            {
                "current_language": self.current_language.value,
                "current_region": self.current_region.value,
                "localization_level": self.localization_level.value,
                "initialized_at": datetime.now().isoformat(),
            },
            "i18n",
            DataIntegrityLevel.ADVANCED,
        )

    def _load_language_configs(self):
        """Load language configurations"""
        # Default language configurations
        self.language_configs = {
            "en": LanguageConfig(
                language_code="en",
                display_name="English",
                native_name="English",
                script_direction="ltr",
                date_format="MM/DD/YYYY",
                time_format="HH:MM:SS",
                number_format="1,234.56",
                currency_symbol="$",
                decimal_separator=".",
                thousands_separator=",",
            ),
            "es": LanguageConfig(
                language_code="es",
                display_name="Spanish",
                native_name="Español",
                script_direction="ltr",
                date_format="DD/MM/YYYY",
                time_format="HH:MM:SS",
                number_format="1.234,56",
                currency_symbol="€",
                decimal_separator=",",
                thousands_separator=".",
            ),
            "fr": LanguageConfig(
                language_code="fr",
                display_name="French",
                native_name="Français",
                script_direction="ltr",
                date_format="DD/MM/YYYY",
                time_format="HH:MM:SS",
                number_format="1 234,56",
                currency_symbol="€",
                decimal_separator=",",
                thousands_separator=" ",
            ),
        }

        # Store language configs
        for lang_code, config in self.language_configs.items():
            self.storage.store_data(
                f"lang_config_{lang_code}",
                asdict(config),
                "i18n/languages",
                DataIntegrityLevel.BASIC,
            )

    def _load_cultural_configs(self):
        """Load cultural configurations"""
        # Default cultural configurations
        self.cultural_configs = {
            "north_america": CulturalConfig(
                region="north_america",
                cultural_norms={
                    "direct_communication": True,
                    "individualism": "high",
                    "time_orientation": "future",
                    "power_distance": "low",
                },
                communication_style="direct",
                formality_levels=["casual", "professional", "formal"],
                color_preferences={
                    "success": "green",
                    "warning": "yellow",
                    "error": "red",
                    "info": "blue",
                },
                taboos=["politics", "religion", "personal_questions"],
                celebrations=["christmas", "thanksgiving", "independence_day"],
            ),
            "europe": CulturalConfig(
                region="europe",
                cultural_norms={
                    "direct_communication": True,
                    "individualism": "medium",
                    "time_orientation": "present",
                    "power_distance": "medium",
                },
                communication_style="balanced",
                formality_levels=["formal", "professional", "casual"],
                color_preferences={
                    "success": "green",
                    "warning": "orange",
                    "error": "red",
                    "info": "blue",
                },
                taboos=["personal_income", "age", "weight"],
                celebrations=["christmas", "easter", "national_days"],
            ),
        }

        # Store cultural configs
        for region, config in self.cultural_configs.items():
            self.storage.store_data(
                f"culture_config_{region}",
                asdict(config),
                "i18n/cultures",
                DataIntegrityLevel.BASIC,
            )

    def _setup_gettext(self):
        """Setup gettext for translation support"""
        try:
            # Set locale
            locale.setlocale(locale.LC_ALL, "")

            # Setup gettext
            gettext.install("agent_cellphone", "localization/translations")

        except Exception as e:
            print(f"Warning: Could not setup gettext: {e}")

    def set_language(self, language_code: str) -> bool:
        """Set the current language"""
        if language_code in [lang.value for lang in LanguageCode]:
            self.current_language = LanguageCode(language_code)

            # Update storage
            self.storage.store_data(
                "current_language", language_code, "i18n", DataIntegrityLevel.BASIC
            )

            # Clear translation cache
            with self.cache_lock:
                self.translation_cache.clear()

            return True
        return False

    def set_cultural_region(self, region: str) -> bool:
        """Set the current cultural region"""
        if region in [reg.value for reg in CulturalRegion]:
            self.current_region = CulturalRegion(region)

            # Update storage
            self.storage.store_data(
                "current_region", region, "i18n", DataIntegrityLevel.BASIC
            )

            return True
        return False

    def set_localization_level(self, level: str) -> bool:
        """Set the localization level"""
        if level in [lev.value for lev in LocalizationLevel]:
            self.localization_level = LocalizationLevel(level)

            # Update storage
            self.storage.store_data(
                "localization_level", level, "i18n", DataIntegrityLevel.BASIC
            )

            return True
        return False

    def translate_text(self, text: str, context: str = "general") -> str:
        """Translate text to current language"""
        cache_key = f"{text}_{self.current_language.value}_{context}"

        # Check cache first
        with self.cache_lock:
            if cache_key in self.translation_cache:
                return self.translation_cache[cache_key]

        # Get translation from storage
        translation_data = self.storage.retrieve_data(
            f"translation_{self.current_language.value}_{context}"
        )

        if translation_data and text in translation_data:
            translated = translation_data[text]
        else:
            # Fallback to original text
            translated = text

        # Cache result
        with self.cache_lock:
            self.translation_cache[cache_key] = translated

        return translated

    def format_date(self, date_obj: datetime, format_type: str = "default") -> str:
        """Format date according to current cultural settings"""
        lang_config = self.language_configs.get(self.current_language.value)
        if not lang_config:
            return date_obj.strftime("%Y-%m-%d")

        # Get custom format
        custom_format = self.storage.retrieve_data(
            f"date_format_{self.current_language.value}_{format_type}"
        )

        if custom_format:
            return date_obj.strftime(custom_format)

        # Use default format
        return date_obj.strftime("%Y-%m-%d")

    def format_number(self, number: float, format_type: str = "default") -> str:
        """Format number according to current cultural settings"""
        lang_config = self.language_configs.get(self.current_language.value)
        if not lang_config:
            return str(number)

        # Apply cultural formatting
        if format_type == "currency":
            return f"{lang_config.currency_symbol}{number:,.2f}"
        elif format_type == "decimal":
            return str(number).replace(".", lang_config.decimal_separator)
        else:
            return str(number)

    def get_cultural_adaptation(self, element: str, context: str = "general") -> Any:
        """Get cultural adaptation for UI elements"""
        if self.localization_level == LocalizationLevel.BASIC:
            return None

        # Get cultural adaptation data
        adaptation_data = self.storage.retrieve_data(
            f"cultural_adaptation_{self.current_region.value}_{element}_{context}"
        )

        return adaptation_data

    def add_translation(
        self, language_code: str, context: str, translations: Dict[str, str]
    ) -> bool:
        """Add new translations"""
        try:
            # Store translations
            self.storage.store_data(
                f"translation_{language_code}_{context}",
                translations,
                "i18n/translations",
                DataIntegrityLevel.BASIC,
            )

            # Clear cache for this language/context
            with self.cache_lock:
                keys_to_remove = [
                    k
                    for k in self.translation_cache.keys()
                    if language_code in k and context in k
                ]
                for key in keys_to_remove:
                    del self.translation_cache[key]

            return True
        except Exception as e:
            print(f"Error adding translation: {e}")
            return False

    def get_supported_languages(self) -> List[Dict[str, str]]:
        """Get list of supported languages"""
        return [
            {
                "code": lang.value,
                "name": config.display_name,
                "native_name": config.native_name,
            }
            for lang, config in self.language_configs.items()
        ]

    def get_system_status(self) -> Dict[str, Any]:
        """Get internationalization system status"""
        return {
            "current_language": self.current_language.value,
            "current_region": self.current_region.value,
            "localization_level": self.localization_level.value,
            "supported_languages": len(self.language_configs),
            "supported_regions": len(self.cultural_configs),
            "translation_cache_size": len(self.translation_cache),
            "storage_status": self.storage.get_storage_status(),
        }

    def shutdown(self):
        """Shutdown the internationalization manager"""
        # Save current state
        self.storage.store_data(
            "i18n_final_state",
            self.get_system_status(),
            "i18n",
            DataIntegrityLevel.ADVANCED,
        )

        # Clear cache
        with self.cache_lock:
            self.translation_cache.clear()


def main():
    """CLI interface for InternationalizationManager"""
    parser = argparse.ArgumentParser(description="Internationalization Manager CLI")
    parser.add_argument("--test", action="store_true", help="Run system test")
    parser.add_argument("--set-language", type=str, help="Set language code")
    parser.add_argument("--set-region", type=str, help="Set cultural region")
    parser.add_argument("--translate", type=str, help="Translate text")
    parser.add_argument(
        "--add-translation",
        nargs=3,
        metavar=("LANG", "CONTEXT", "TEXT"),
        help="Add translation (LANG CONTEXT 'TEXT')",
    )
    parser.add_argument("--status", action="store_true", help="Show system status")
    parser.add_argument(
        "--supported-languages", action="store_true", help="Show supported languages"
    )

    args = parser.parse_args()

    # Initialize manager
    manager = InternationalizationManager()

    try:
        if args.test:
            print("🧪 Running Internationalization Manager Test...")

            # Test language switching
            print(f"Current language: {manager.current_language.value}")
            manager.set_language("es")
            print(f"Switched to: {manager.current_language.value}")

            # Test translation
            test_text = "Hello, world!"
            translated = manager.translate_text(test_text)
            print(f"Translation test: '{test_text}' -> '{translated}'")

            # Test cultural adaptation
            adaptation = manager.get_cultural_adaptation("colors", "ui")
            print(f"Cultural adaptation: {adaptation}")

            print("✅ Test completed successfully!")

        elif args.set_language:
            if manager.set_language(args.set_language):
                print(f"✅ Language set to: {args.set_language}")
            else:
                print(f"❌ Invalid language code: {args.set_language}")

        elif args.set_region:
            if manager.set_cultural_region(args.set_region):
                print(f"✅ Cultural region set to: {args.set_region}")
            else:
                print(f"❌ Invalid region: {args.set_region}")

        elif args.translate:
            translated = manager.translate_text(args.translate)
            print(f"Translation: '{args.translate}' -> '{translated}'")

        elif args.add_translation:
            lang, context, text = args.add_translation
            if manager.add_translation(lang, context, {"test_key": text}):
                print(f"✅ Translation added for {lang}/{context}")
            else:
                print(f"❌ Failed to add translation")

        elif args.status:
            status = manager.get_system_status()
            print("🌍 Internationalization System Status:")
            for key, value in status.items():
                print(f"  {key}: {value}")

        elif args.supported_languages:
            languages = manager.get_supported_languages()
            print("🌍 Supported Languages:")
            for lang in languages:
                print(f"  {lang['code']}: {lang['name']} ({lang['native_name']})")

        else:
            parser.print_help()

    except KeyboardInterrupt:
        print("\n🛑 Shutting down...")
    finally:
        manager.shutdown()


if __name__ == "__main__":
    main()
