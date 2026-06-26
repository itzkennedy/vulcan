# ============================================
# NECHE CODING AGENT - Fixer
# ============================================
# Uses AI to fix issues found by the scanner
# Has anti-loop protection to save your data

import os
import requests
import json
from config import (OFFLINE_MODEL, ONLINE_MODEL, 
                   GEMINI_API_KEY, MAX_LOOP_COUNT)
from vault import is_locked

# Anti-loop protection
loop_tracker = {}

def check_internet():
    """Check if internet is available"""
    try:
        requests.get("http://google.com", timeout=3)
        return True
    except:
        return False

def call_offline_ai(code, instruction):
    """Send code to local Ollama model"""
    try:
        response = requests.post(
            'http://localhost:11434/api/generate',
            json={
                "model": OFFLINE_MODEL,
                "prompt": f"{instruction}\n\nCode:\n{code}\n\nReturn only the fixed code, no explanation:",
                "stream": False
            },
            timeout=60
        )
        if response.status_code == 200:
            return response.json().get('response', '')
        return None
    except Exception as e:
        print(f"❌ Offline AI error: {e}")
        return None

def call_online_ai(code, instruction):
    """Send code to Deepseek API"""
    from config import DEEPSEEK_API_KEY
    
    if not DEEPSEEK_API_KEY:
        print("⚠️ No Deepseek API key set — using offline mode")
        return call_offline_ai(code, instruction)
    
    try:
        response = requests.post(
            "https://api.deepseek.com/chat/completions",
            headers={
                "Content-Type": "application/json",
                "Authorization": f"Bearer {DEEPSEEK_API_KEY}"
            },
            json={
                "model": "deepseek-chat",
                "messages": [
                    {
                        "role": "system",
                        "content": "You are an expert coding assistant. Fix code issues and return only the fixed code with no explanation."
                    },
                    {
                        "role": "user",
                        "content": f"{instruction}\n\nCode:\n{code}"
                    }
                ],
                "temperature": 0.1
            },
            timeout=30
        )
        
        if response.status_code == 200:
            return response.json()['choices'][0]['message']['content']
        else:
            print(f"⚠️ Deepseek API error: {response.status_code}")
            print("   Falling back to offline mode...")
            return call_offline_ai(code, instruction)
            
    except Exception as e:
        print(f"❌ Online AI error: {e}")
        print("   Falling back to offline mode...")
        return call_offline_ai(code, instruction)

def fix_code(filepath, content, issues):
    """Fix a file using AI — offline or online"""
    
    # Check vault protection
    if is_locked(filepath):
        print(f"🔒 Skipping locked file: {filepath}")
        return None
    
    filename = os.path.basename(filepath)
    
    # Anti-loop protection
    if filepath in loop_tracker:
        loop_tracker[filepath] += 1
        if loop_tracker[filepath] >= MAX_LOOP_COUNT:
            print(f"🛡️ DATA SHIELD: AI looping on {filename} — stopped to save data!")
            print(f"   Flag this file for manual review.")
            loop_tracker[filepath] = 0
            return None
    else:
        loop_tracker[filepath] = 1
    
    # Build instruction from issues
    issue_list = "\n".join([f"- Line {i['line']}: {i['message']}" 
                           for i in issues])
    instruction = f"""Fix these issues in the code:
{issue_list}

Rules:
1. Return only the fixed code
2. Do not change working code
3. Do not add unnecessary comments
4. Keep the same structure"""

    # Choose online or offline
    is_online = check_internet()
    
    if is_online and GEMINI_API_KEY:
        print(f"⚡ Online Mode: Fixing {filename}...")
        fixed_code = call_online_ai(content, instruction)
    else:
        print(f"🔌 Offline Mode: Fixing {filename}...")
        fixed_code = call_offline_ai(content, instruction)
    
    if fixed_code:
        # Save fixed code back to file
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(fixed_code)
        print(f"✅ Fixed: {filename}")
        loop_tracker[filepath] = 0
        return filepath
    else:
        print(f"❌ Could not fix: {filename}")
        return None

def fix_all_issues(scan_results):
    """Fix all issues found in scan"""
    fixes_made = []
    
    files_with_issues = [r for r in scan_results if r['issue_count'] > 0]
    
    if not files_with_issues:
        print("✅ No issues to fix!")
        return fixes_made
    
    print(f"\n🔧 Fixing {len(files_with_issues)} files...")
    print("=" * 50)
    
    for result in files_with_issues:
        fixed = fix_code(
            result['file'],
            result['content'],
            result['issues']
        )
        if fixed:
            fixes_made.append(fixed)
    
    print(f"\n✅ Fixed {len(fixes_made)} out of {len(files_with_issues)} files")
    return fixes_made