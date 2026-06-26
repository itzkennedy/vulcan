# ============================================
# NECHE CODING AGENT - File Scanner
# ============================================
# Scans your project files for bugs, errors,
# missing things and security issues

import os
import json
from config import SUPPORTED_EXTENSIONS, MAX_FILE_SIZE_KB
from vault import is_locked

def get_all_files(project_path):
    """Get all supported code files in a project"""
    all_files = []
    
    for root, dirs, files in os.walk(project_path):
        # Skip these folders
        skip_folders = ['node_modules', '.git', 'venv', 
                       '__pycache__', '.next', 'dist', 'build']
        dirs[:] = [d for d in dirs if d not in skip_folders]
        
        for file in files:
            ext = os.path.splitext(file)[1].lower()
            if ext in SUPPORTED_EXTENSIONS:
                full_path = os.path.join(root, file)
                
                # Skip locked files
                if is_locked(full_path):
                    print(f"🔒 Skipping locked file: {file}")
                    continue
                
                # Skip files that are too large
                size_kb = os.path.getsize(full_path) / 1024
                if size_kb > MAX_FILE_SIZE_KB:
                    print(f"⚠️ Skipping large file: {file} ({size_kb:.0f}KB)")
                    continue
                    
                all_files.append(full_path)
    
    return all_files

def read_file(filepath):
    """Safely read a file"""
    try:
        with open(filepath, 'r', encoding='utf-8', errors='ignore') as f:
            return f.read()
    except Exception as e:
        print(f"❌ Could not read {filepath}: {e}")
        return None

def scan_for_basic_issues(filepath, content):
    """Scan file for common basic issues"""
    issues = []
    lines = content.split('\n')
    
    for i, line in enumerate(lines, 1):
        # Check for common problems
        if 'console.log(' in line and 'debug' in line.lower():
            issues.append({
                'line': i,
                'type': 'debug_code',
                'message': f'Debug console.log found at line {i}',
                'severity': 'low'
            })
        
        if 'TODO' in line or 'FIXME' in line:
            issues.append({
                'line': i,
                'type': 'incomplete_code',
                'message': f'Incomplete code marker at line {i}: {line.strip()}',
                'severity': 'medium'
            })
        
        # Check for exposed API keys
        suspicious_patterns = ['api_key =', 'apikey =', 'secret =', 
                              'password =', 'API_KEY =']
        for pattern in suspicious_patterns:
            if pattern.lower() in line.lower() and '""' not in line and "''" not in line:
                issues.append({
                    'line': i,
                    'type': 'security_risk',
                    'message': f'Possible exposed secret at line {i}',
                    'severity': 'high'
                })
        
        # Check for missing error handling in JS/PHP
        if 'fetch(' in line or 'axios(' in line:
            # Check if .catch is nearby
            nearby = '\n'.join(lines[i:min(i+5, len(lines))])
            if '.catch' not in nearby and 'try' not in '\n'.join(lines[max(0,i-3):i]):
                issues.append({
                    'line': i,
                    'type': 'missing_error_handling',
                    'message': f'API call without error handling at line {i}',
                    'severity': 'medium'
                })
    
    return issues

def scan_project(project_path):
    """Full project scan - returns all files and their issues"""
    print(f"\n🔍 Scanning project: {project_path}")
    print("=" * 50)
    
    files = get_all_files(project_path)
    print(f"📁 Found {len(files)} files to scan\n")
    
    scan_results = []
    
    for filepath in files:
        content = read_file(filepath)
        if content is None:
            continue
            
        issues = scan_for_basic_issues(filepath, content)
        
        scan_results.append({
            'file': filepath,
            'content': content,
            'issues': issues,
            'issue_count': len(issues)
        })
        
        if issues:
            print(f"⚠️  {os.path.basename(filepath)} — {len(issues)} issue(s) found")
        else:
            print(f"✅ {os.path.basename(filepath)} — Clean")
    
    total_issues = sum(r['issue_count'] for r in scan_results)
    print(f"\n📊 Scan complete: {total_issues} total issues found across {len(files)} files")
    
    return scan_results