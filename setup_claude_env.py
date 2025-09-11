import os
import subprocess
import sys

def check_anthropic_installed():
    try:
        import anthropic
        print("[OK] 'anthropic' package is installed.")
        return True
    except ImportError:
        print("[INFO] Installing 'anthropic' package...")
        subprocess.check_call([sys.executable, "-m", "pip", "install", "anthropic"])
        print("[OK] 'anthropic' package installed.")
        return True

def check_api_key():
    api_key = os.environ.get("ANTHROPIC_API_KEY")
    if api_key:
        print("[OK] ANTHROPIC_API_KEY is set.")
        return True
    else:
        print("[ERROR] ANTHROPIC_API_KEY is not set.")
        key = input("Enter your Anthropic API key: ").strip()
        os.environ["ANTHROPIC_API_KEY"] = key
        print("[OK] ANTHROPIC_API_KEY set for this session.")
        return True

def test_claude():
    try:
        import anthropic
        client = anthropic.Anthropic()
        message = client.messages.create(
            model="claude-3-5-sonnet-20240620",
            max_tokens=50,
            messages=[{"role": "user", "content": "Say hello Claude."}]
        )
        print("[CLAUDE RESPONSE]", message.content[0].text)
        print("[OK] Claude API is working.")
    except Exception as e:
        print(f"[ERROR] Claude API test failed: {e}")

if __name__ == "__main__":
    print("--- Claude API Setup Automation ---")
    check_anthropic_installed()
    check_api_key()
    test_claude()