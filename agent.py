# ============================================
# VULCAN - Main Brain
# ============================================
# Built by @nechecodes
# The AI That Builds, Fixes & Deploys

import os
import time
from datetime import datetime
from scanner import scan_project
from fixer import fix_all_issues
from reporter import generate_report, quick_summary
from vault import show_vault, lock_file

def print_banner():
    print("""
╔══════════════════════════════════════════════╗
║                                              ║
║      ██╗   ██╗██╗   ██╗██╗      ██████╗    ║
║      ██║   ██║██║   ██║██║     ██╔════╝    ║
║      ██║   ██║██║   ██║██║     ██║         ║
║      ╚██╗ ██╔╝██║   ██║██║     ██║         ║
║       ╚████╔╝ ╚██████╔╝███████╗╚██████╗    ║
║        ╚═══╝   ╚═════╝ ╚══════╝ ╚═════╝    ║
║                                              ║
║       █████╗ ███╗   ██╗                     ║
║     ██╔══██╗████╗  ██║                     ║
║     ███████║██╔██╗ ██║                     ║
║     ██╔══██║██║╚██╗██║                     ║
║     ██║  ██║██║ ╚████║                     ║
║     ╚═╝  ╚═╝╚═╝  ╚═══╝                     ║
║                                              ║
║    The AI That Builds, Fixes & Deploys      ║
║            by @nechecodes                   ║
║                                              ║
║  🔌 Offline Mode  →  Ollama (Local)         ║
║  ⚡ Online Mode   →  Gemini (Cloud)         ║
║  🔒 Vault Active  →  Files Protected        ║
║                                              ║
╚══════════════════════════════════════════════╝
    """)

def get_project_path():
    """Ask user which project to scan"""
    print("\n📁 WHICH PROJECT DO YOU WANT TO SCAN?")
    print("─────────────────────────────────────")
    print("  Enter the full path to your project folder")
    print("  Example: C:\\Users\\Neche\\Desktop\\BAYA")
    print("")
    path = input("  Project path: ").strip().strip('"')
    
    if not os.path.exists(path):
        print(f"❌ Path not found: {path}")
        return None
    
    return path

def show_menu():
    """Show main menu"""
    print("""
🤖 WHAT DO YOU WANT TO DO?
─────────────────────────────────────
  1 → Scan project for issues
  2 → Scan and auto-fix all issues
  3 → View locked files (Vault)
  4 → Lock a file (protect from AI)
  5 → Run continuous monitoring
  6 → Exit
─────────────────────────────────────
    """)
    return input("  Choose (1-6): ").strip()

def run_once(project_path, auto_fix=False):
    """Run one full scan and optionally fix"""
    print(f"\n⏰ Started at: {datetime.now().strftime('%H:%M:%S')}")
    
    # Step 1: Scan
    scan_results = scan_project(project_path)
    
    # Step 2: Fix if requested
    fixes_made = []
    if auto_fix:
        fixes_made = fix_all_issues(scan_results)
    
    # Step 3: Report
    generate_report(scan_results, fixes_made)
    
    return scan_results, fixes_made

def run_continuous(project_path, interval=30):
    """Run agent continuously every X seconds"""
    print(f"\n🔄 CONTINUOUS MODE ACTIVE")
    print(f"   Scanning every {interval} seconds")
    print(f"   Press Ctrl+C to stop\n")
    
    session_count = 0
    total_fixes = 0
    
    try:
        while True:
            session_count += 1
            print(f"\n{'='*50}")
            print(f"🔄 Session #{session_count}")
            print(f"{'='*50}")
            
            scan_results, fixes_made = run_once(project_path, auto_fix=True)
            total_fixes += len(fixes_made)
            
            print(f"\n💤 Sleeping {interval} seconds...")
            print(f"   Total fixes this session: {total_fixes}")
            print(f"   Press Ctrl+C to stop")
            time.sleep(interval)
            
    except KeyboardInterrupt:
        print(f"\n\n⛔ Vulcan stopped by user")
        print(f"   Total sessions run: {session_count}")
        print(f"   Total fixes made: {total_fixes}")
        print(f"   Report saved to: vulcan_report.txt")

def main():
    """Main entry point"""
    print_banner()
    
    project_path = get_project_path()
    if not project_path:
        return
    
    while True:
        choice = show_menu()
        
        if choice == '1':
            scan_results, _ = run_once(project_path, auto_fix=False)
            quick_summary(scan_results)
            
        elif choice == '2':
            print("\n⚠️  AUTO-FIX MODE")
            print("   Vulcan will modify your files.")
            confirm = input("   Are you sure? (yes/no): ").strip().lower()
            if confirm == 'yes':
                run_once(project_path, auto_fix=True)
            else:
                print("   Cancelled.")
                
        elif choice == '3':
            show_vault()
            
        elif choice == '4':
            filepath = input("\n  Enter file path to lock: ").strip().strip('"')
            lock_file(filepath)
            
        elif choice == '5':
            interval = input("\n  Scan every how many seconds? (default 30): ").strip()
            interval = int(interval) if interval.isdigit() else 30
            run_continuous(project_path, interval)
            
        elif choice == '6':
            print("\n🔥 Vulcan signing off. Built by @nechecodes")
            break
            
        else:
            print("❌ Invalid choice. Pick 1-6.")

if __name__ == "__main__":
    main()