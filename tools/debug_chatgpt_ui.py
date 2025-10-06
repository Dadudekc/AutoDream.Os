#!/usr/bin/env python3
"""
Debug ChatGPT UI - See what elements are actually available
"""

import time
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from webdriver_manager.chrome import ChromeDriverManager

def debug_chatgpt_ui():
    """Debug what's actually on the ChatGPT page."""
    print("🔍 DEBUGGING CHATGPT UI")
    print("=" * 40)
    
    # Setup Chrome with stealth options
    options = Options()
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-dev-shm-usage")
    options.add_argument("--disable-gpu")
    options.add_argument("--window-size=1920,1080")
    
    # Stealth options to avoid detection
    options.add_argument("--disable-blink-features=AutomationControlled")
    options.add_experimental_option("excludeSwitches", ["enable-automation"])
    options.add_experimental_option('useAutomationExtension', False)
    options.add_argument("--user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/140.0.0.0 Safari/537.36")
    
    driver = None
    try:
        # Initialize driver
        service = Service(ChromeDriverManager().install())
        driver = webdriver.Chrome(service=service, options=options)
        driver.execute_script("Object.defineProperty(navigator, 'webdriver', {get: () => undefined})")
        
        print("✅ Driver initialized")
        
        # Navigate to Thea
        thea_url = "https://chatgpt.com/g/g-67f437d96d7c81918b2dbc12f0423867-thea-manager?model=gpt-5"
        print(f"🌐 Navigating to: {thea_url}")
        driver.get(thea_url)
        
        # Wait for page to load
        print("⏳ Waiting 10 seconds for page to load...")
        time.sleep(10)
        
        # Get page info
        print(f"📄 Page title: {driver.title}")
        print(f"🌐 Current URL: {driver.current_url}")
        
        # Check for common elements
        print("\n🔍 ELEMENT ANALYSIS:")
        print("-" * 30)
        
        # Check for input elements
        textareas = driver.find_elements(By.TAG_NAME, "textarea")
        print(f"📝 Textareas found: {len(textareas)}")
        
        inputs = driver.find_elements(By.TAG_NAME, "input")
        print(f"📝 Inputs found: {len(inputs)}")
        
        divs = driver.find_elements(By.TAG_NAME, "div")
        contenteditable_divs = driver.find_elements(By.CSS_SELECTOR, "div[contenteditable='true']")
        print(f"📝 Contenteditable divs: {len(contenteditable_divs)}")
        
        buttons = driver.find_elements(By.TAG_NAME, "button")
        print(f"🔘 Buttons found: {len(buttons)}")
        
        # Check for login indicators
        print("\n🔐 LOGIN STATUS CHECK:")
        print("-" * 30)
        
        login_indicators = [
            "Log in", "Sign up", "Welcome", "Login", "Signup"
        ]
        
        page_text = driver.page_source.lower()
        for indicator in login_indicators:
            if indicator.lower() in page_text:
                print(f"🔒 Found login indicator: '{indicator}'")
        
        # Check for specific ChatGPT selectors
        print("\n🎯 CHATGPT SELECTOR CHECK:")
        print("-" * 30)
        
        selectors_to_test = [
            "#prompt-textarea",
            "textarea[data-testid*='prompt']",
            "textarea[placeholder*='Message']",
            "div[contenteditable='true'][role='textbox']",
            "div[data-testid='conversation-composer-input']",
            "textarea[data-testid='prompt-textarea']",
            "p[data-placeholder='Ask anything']",
            "#prompt-textarea > p",
            "div[contenteditable='true']"
        ]
        
        for selector in selectors_to_test:
            try:
                elements = driver.find_elements(By.CSS_SELECTOR, selector)
                if elements:
                    print(f"✅ Found {len(elements)} elements with selector: {selector}")
                    for i, elem in enumerate(elements[:3]):  # Show first 3
                        try:
                            is_displayed = elem.is_displayed()
                            is_enabled = elem.is_enabled()
                            print(f"   Element {i+1}: displayed={is_displayed}, enabled={is_enabled}")
                        except:
                            print(f"   Element {i+1}: could not check properties")
                else:
                    print(f"❌ No elements found with selector: {selector}")
            except Exception as e:
                print(f"⚠️ Error testing selector {selector}: {e}")
        
        # Check page source for clues
        print("\n🔍 PAGE SOURCE ANALYSIS:")
        print("-" * 30)
        
        page_source = driver.page_source
        print(f"📄 Page source length: {len(page_source)} characters")
        
        # Look for key terms
        key_terms = ["prompt", "message", "input", "textarea", "conversation", "chat"]
        for term in key_terms:
            count = page_source.lower().count(term)
            if count > 0:
                print(f"🔍 Found '{term}' {count} times in page source")
        
        # Wait longer and check again
        print("\n⏳ Waiting 15 more seconds for dynamic loading...")
        time.sleep(15)
        
        # Recheck elements after longer wait
        print("\n🔍 RE-CHECKING AFTER LONGER WAIT:")
        print("-" * 30)
        
        textareas = driver.find_elements(By.TAG_NAME, "textarea")
        print(f"📝 Textareas found after wait: {len(textareas)}")
        
        contenteditable_divs = driver.find_elements(By.CSS_SELECTOR, "div[contenteditable='true']")
        print(f"📝 Contenteditable divs after wait: {len(contenteditable_divs)}")
        
        # Try to find any clickable input area
        print("\n🎯 SEARCHING FOR ANY INPUT AREA:")
        print("-" * 30)
        
        all_elements = driver.find_elements(By.XPATH, "//*[contains(@placeholder, 'message') or contains(@placeholder, 'ask') or contains(@placeholder, 'send') or @contenteditable='true' or @role='textbox']")
        print(f"🔍 Found {len(all_elements)} potential input elements")
        
        for i, elem in enumerate(all_elements[:5]):
            try:
                tag = elem.tag_name
                is_displayed = elem.is_displayed()
                is_enabled = elem.is_enabled()
                placeholder = elem.get_attribute("placeholder") or "none"
                role = elem.get_attribute("role") or "none"
                contenteditable = elem.get_attribute("contenteditable") or "none"
                
                print(f"   Element {i+1}: <{tag}> displayed={is_displayed}, enabled={is_enabled}")
                print(f"      placeholder='{placeholder}', role='{role}', contenteditable='{contenteditable}'")
            except Exception as e:
                print(f"   Element {i+1}: Error getting properties - {e}")
        
        print("\n✅ Debug complete - keeping browser open for 30 seconds for manual inspection...")
        time.sleep(30)
        
    except Exception as e:
        print(f"❌ Error: {e}")
    finally:
        if driver:
            driver.quit()

if __name__ == "__main__":
    debug_chatgpt_ui()
