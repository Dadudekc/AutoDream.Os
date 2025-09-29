#!/usr/bin/env python3
"""
Thea Login Detector - V2 Compliant Login Status Detection
=========================================================

Handles login status detection for Thea/ChatGPT.
Extracted from thea_login_handler.py to maintain V2 compliance.

Features:
- Comprehensive login status detection
- Multiple detection strategies
- ChatGPT-specific selectors and indicators
- Robust fallback mechanisms

Usage:
    from src.services.thea.thea_login_detector import TheaLoginDetector

    detector = TheaLoginDetector()
    is_logged_in = detector.is_logged_in(driver)
"""

import logging

# Selenium imports
try:
    from selenium import webdriver
    from selenium.common.exceptions import NoSuchElementException
    from selenium.webdriver.common.by import By

    SELENIUM_AVAILABLE = True
except ImportError:
    SELENIUM_AVAILABLE = False
    print("⚠️  Selenium not available - login detector will use fallback methods")

logger = logging.getLogger(__name__)


class TheaLoginDetector:
    """
    Handles login status detection for Thea/ChatGPT.

    Uses multiple indicators to detect login status:
    - Send button presence
    - Conversation elements
    - Input field availability
    - Profile/account indicators
    """

    def __init__(self):
        """Initialize the login detector."""
        pass

    def is_logged_in(self, driver) -> bool:
        """
        Check if user is logged in to Thea/ChatGPT.

        Args:
            driver: Selenium webdriver instance

        Returns:
            True if logged in, False otherwise
        """
        if not SELENIUM_AVAILABLE:
            logger.warning("Selenium not available - cannot check login status")
            return False

        try:
            # First, let's debug what we can see on the page
            page_title = driver.title
            current_url = driver.current_url
            logger.debug(f"Page title: {page_title}")
            logger.debug(f"Current URL: {current_url}")

            # Look for logged-in indicators (Thea/ChatGPT specific)
            # More specific and accurate selectors
            logged_in_indicators = [
                # Most specific indicators first
                "//button[contains(@data-testid, 'send-button')]",
                "//button[contains(@aria-label, 'Send')]",
                "//textarea[contains(@data-testid, 'prompt-textarea')]",
                "//textarea[contains(@placeholder, 'Message')]",
                "//div[contains(@data-testid, 'conversation-turn')]",
                # Input area with specific attributes
                "textarea[data-testid*='prompt']",
                "textarea[placeholder*='Message']",
                # Specific ChatGPT elements that indicate logged-in state
                "//div[contains(@class, 'conversation-turn')]",
                "//div[contains(@class, 'message user-message')]",
                "//div[contains(@class, 'message assistant-message')]",
                # Navigation and UI elements that appear when logged in
                "//button[contains(@class, 'new-chat-button')]",
                "//div[contains(@class, 'sidebar')]",
            ]

            found_indicators = []
            login_page_found = False

            for indicator in logged_in_indicators:
                try:
                    if indicator.startswith("//"):
                        elements = driver.find_elements(By.XPATH, indicator)
                    else:
                        elements = driver.find_elements(By.CSS_SELECTOR, indicator)

                    visible_elements = [elem for elem in elements if elem.is_displayed()]
                    if visible_elements:
                        found_indicators.append(f"{indicator} ({len(visible_elements)} found)")
                        logger.debug(
                            f"✅ Found login indicator: {indicator} ({len(visible_elements)} visible)"
                        )
                except Exception as e:
                    logger.debug(f"Error checking {indicator}: {e}")
                    continue

            logger.debug(f"Found {len(found_indicators)} potential login indicators")

            # Check for login page indicators (strong evidence of not logged in)
            login_indicators = [
                "//button[contains(text(), 'Log in')]",
                "//button[contains(text(), 'Sign up')]",
                "//a[contains(text(), 'Log in')]",
                "//a[contains(text(), 'Sign up')]",
                "//input[@name='username']",
                # SECURITY: Password placeholder - replace with environment variable
                "//input[@type='email']",
                "//div[contains(text(), 'Welcome to ChatGPT')]",
                "//div[contains(text(), 'Log in to ChatGPT')]",
                "//h1[contains(text(), 'Welcome')]",
                "//div[contains(@class, 'login')]",
                "//form",  # Login forms
            ]

            for indicator in login_indicators:
                try:
                    element = driver.find_element(By.XPATH, indicator)
                    if element.is_displayed():
                        logger.debug(f"🔒 Found login page indicator: {indicator}")
                        login_page_found = True
                        break
                except NoSuchElementException:
                    continue

            # Decision logic:
            # If we found login page elements AND no logged-in indicators, definitely not logged in
            if login_page_found and len(found_indicators) == 0:
                logger.info(
                    "🔒 Login page detected with no logged-in indicators - user is NOT logged in"
                )
                return False

            # If we found login page elements but also have logged-in indicators, probably logged in
            # (e.g., "Sign up for free" might appear even when logged in)
            if login_page_found and len(found_indicators) > 0:
                logger.info(
                    "⚠️ Mixed signals: Login page elements found but also logged-in indicators"
                )
                # Prioritize logged-in indicators
                if len(found_indicators) >= 2:
                    logger.info("✅ Prioritizing logged-in indicators - user appears logged in")
                    return True

            # Check for strong indicators of being logged in
            # Look for profile/account selector button - very specific indicator
            try:
                # Look for the profile selector button that appears when logged in
                profile_selectors = [
                    "//button[contains(@class, '__menu-item')]",
                    "//button[contains(text(), 'Personal account')]",
                    "//button[contains(text(), 'account')]",
                    "//img[@alt='Profile image']",  # Profile image in account selector
                    "//div[contains(@class, 'bg-gray-500/30')]",  # Profile image container
                ]

                for selector in profile_selectors:
                    try:
                        if selector.startswith("//"):
                            elements = driver.find_elements(By.XPATH, selector)
                        else:
                            elements = driver.find_elements(By.CSS_SELECTOR, selector)

                        visible_elements = [elem for elem in elements if elem.is_displayed()]
                        if visible_elements:
                            logger.info(
                                f"✅ Found profile selector element: {selector} - user is logged in"
                            )
                            return True
                    except Exception:
                        continue
            except Exception:
                pass

            # Look for textarea (message input) - strongest indicator
            try:
                textareas = driver.find_elements(By.TAG_NAME, "textarea")
                visible_textareas = [ta for ta in textareas if ta.is_displayed()]
                if visible_textareas:
                    logger.info(
                        f"✅ Found {len(visible_textareas)} visible textarea(s) - user is logged in"
                    )
                    return True
            except Exception:
                pass

            # Look for send button or similar
            try:
                buttons = driver.find_elements(By.TAG_NAME, "button")
                send_buttons = []
                for btn in buttons:
                    try:
                        if btn.is_displayed():
                            btn_text = str(btn.text or "").lower()
                            if "send" in btn_text or "submit" in btn_text:
                                send_buttons.append(btn)
                    except Exception:
                        continue  # Skip buttons that cause errors
                if send_buttons:
                    logger.info(f"✅ Found {len(send_buttons)} send button(s) - user is logged in")
                    return True
            except Exception as e:
                logger.debug(f"Error checking send buttons: {e}")

            # If we found multiple logged-in indicators, probably logged in
            if len(found_indicators) >= 2:
                logger.info(
                    f"✅ Found {len(found_indicators)} login indicators - user appears logged in"
                )
                return True

            # If we have buttons + inputs + textarea, likely logged in
            try:
                buttons = len(
                    [
                        btn
                        for btn in driver.find_elements(By.TAG_NAME, "button")
                        if btn.is_displayed()
                    ]
                )
                inputs = len(
                    [
                        inp
                        for inp in driver.find_elements(By.TAG_NAME, "input")
                        if inp.is_displayed()
                    ]
                )
                textareas = len(
                    [
                        ta
                        for ta in driver.find_elements(By.TAG_NAME, "textarea")
                        if ta.is_displayed()
                    ]
                )

                # Heuristic: if we have many buttons and some inputs/textareas, likely logged in
                if buttons > 10 and (inputs > 0 or textareas > 0):
                    logger.info(
                        f"✅ Found {buttons} buttons, {inputs} inputs, {textareas} textareas - user appears logged in"
                    )
                    return True
            except Exception:
                pass

            # Additional check: look for any input field that could be a message input
            try:
                # Look for any textarea or contenteditable div
                input_selectors = [
                    "textarea",
                    "div[contenteditable='true']",
                    "div[data-testid*='input']",
                    "input[type='text']",
                ]

                for selector in input_selectors:
                    elements = driver.find_elements(By.CSS_SELECTOR, selector)
                    for element in elements:
                        if element.is_displayed() and element.is_enabled():
                            # Check if it's likely a message input (not search, etc.)
                            placeholder = element.get_attribute("placeholder") or ""
                            if any(
                                # SECURITY: Key placeholder - replace with environment variable
                                # SECURITY: Key placeholder - replace with environment variable
                            ):
                                logger.debug(
                                    f"✅ Found message input: {selector} with placeholder '{placeholder}'"
                                )
                                return True
                            # If no placeholder, check size/position (message inputs are usually large)
                            rect = element.rect
                            if rect["height"] > 50:  # Likely a message input
                                logger.debug(
                                    f"✅ Found large input field: {selector} (size: {rect['width']}x{rect['height']})"
                                )
                                return True
            except Exception as e:
                logger.debug(f"Error checking input fields: {e}")

            # If we found some indicators but not definitive ones, log what we found
            if found_indicators:
                logger.info(f"Found potential indicators but not definitive: {found_indicators}")

            # Final fallback: if we're on the Thea URL and haven't found login indicators,
            # assume we need to login (safer assumption)
            if "thea-manager" in current_url and not any(
                "login" in current_url.lower() or "auth" in current_url.lower()
            ):
                logger.warning(
                    "On Thea page but couldn't confirm login status - assuming not logged in"
                )
                return False

            logger.warning("⚠️ Could not definitively determine login status")
            logger.info(f"Debug info - Title: {page_title}, URL: {current_url}")
            return False

        except Exception as e:
            logger.error(f"Error checking login status: {e}")
            return False

    def is_on_thea_page(self, driver) -> bool:
        """Check if we're currently on the Thea page."""
        try:
            current_url = driver.current_url
            page_title = driver.title

            # Check URL contains Thea identifier
            if "g-67f437d96d7c81918b2dbc12f0423867" in current_url:
                return True

            # Check title contains Thea
            if "thea" in page_title.lower():
                return True

            return False
        except Exception:
            return False


# Convenience functions for easy integration
def create_login_detector() -> TheaLoginDetector:
    """
    Create a Thea login detector with default settings.

    Returns:
        TheaLoginDetector instance
    """
    return TheaLoginDetector()


def check_login_status(driver) -> bool:
    """
    Quick check of Thea login status.

    Args:
        driver: Selenium webdriver instance

    Returns:
        True if logged in, False otherwise
    """
    detector = create_login_detector()
    return detector.is_logged_in(driver)


if __name__ == "__main__":
    # Example usage
    print("🐝 V2_SWARM Thea Login Detector")
    print("=" * 40)

    # Create detector
    detector = create_login_detector()

    print("✅ Thea Login Detector created")
    print("📝 To use:")
    print("   detector = create_login_detector()")
    print("   is_logged_in = detector.is_logged_in(driver)")
