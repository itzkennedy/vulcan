# ============================================
# NECHE CODING AGENT - Deployer
# ============================================
# Automatically deploys your projects to
# free hosting platforms

import os
import subprocess
import requests
from config import GEMINI_API_KEY

def check_netlify_cli():
    """Check if Netlify CLI is installed"""
    try:
        subprocess.run(['netlify', '--version'], 
                      capture_output=True, check=True)
        return True
    except:
        return False

def check_vercel_cli():
    """Check if Vercel CLI is installed"""
    try:
        subprocess.run(['vercel', '--version'], 
                      capture_output=True, check=True)
        return True
    except:
        return False

def install_netlify():
    """Install Netlify CLI"""
    print("📦 Installing Netlify CLI...")
    try:
        subprocess.run(['npm', 'install', '-g', 'netlify-cli'], 
                      check=True)
        print("✅ Netlify CLI installed!")
        return True
    except Exception as e:
        print(f"❌ Could not install Netlify CLI: {e}")
        print("   Make sure Node.js is installed first")
        return False

def install_vercel():
    """Install Vercel CLI"""
    print("📦 Installing Vercel CLI...")
    try:
        subprocess.run(['npm', 'install', '-g', 'vercel'], 
                      check=True)
        print("✅ Vercel CLI installed!")
        return True
    except Exception as e:
        print(f"❌ Could not install Vercel CLI: {e}")
        return False

def deploy_to_netlify(project_path):
    """Deploy project to Netlify"""
    print(f"\n🚀 Deploying to Netlify...")
    print(f"   Project: {project_path}")
    
    if not check_netlify_cli():
        print("⚠️ Netlify CLI not found")
        install = input("   Install it now? (yes/no): ").strip().lower()
        if install == 'yes':
            if not install_netlify():
                return False
        else:
            return False
    
    try:
        print("   Running deployment...")
        result = subprocess.run(
            ['netlify', 'deploy', '--prod', '--dir', project_path],
            capture_output=True,
            text=True
        )
        
        if result.returncode == 0:
            print("✅ Successfully deployed to Netlify!")
            print(result.stdout)
            return True
        else:
            print(f"❌ Deployment failed: {result.stderr}")
            return False
            
    except Exception as e:
        print(f"❌ Deployment error: {e}")
        return False

def deploy_to_vercel(project_path):
    """Deploy project to Vercel"""
    print(f"\n🚀 Deploying to Vercel...")
    print(f"   Project: {project_path}")
    
    if not check_vercel_cli():
        print("⚠️ Vercel CLI not found")
        install = input("   Install it now? (yes/no): ").strip().lower()
        if install == 'yes':
            if not install_vercel():
                return False
        else:
            return False
    
    try:
        print("   Running deployment...")
        result = subprocess.run(
            ['vercel', '--prod', project_path],
            capture_output=True,
            text=True
        )
        
        if result.returncode == 0:
            print("✅ Successfully deployed to Vercel!")
            print(result.stdout)
            return True
        else:
            print(f"❌ Deployment failed: {result.stderr}")
            return False
            
    except Exception as e:
        print(f"❌ Deployment error: {e}")
        return False

def analyze_costs(project_path):
    """Analyze project and tell user what costs money"""
    print(f"\n💰 COST ANALYSIS")
    print("=" * 50)
    
    findings = []
    
    # Check for database usage
    for root, dirs, files in os.walk(project_path):
        dirs[:] = [d for d in dirs if d not in 
                  ['node_modules', '.git', 'venv']]
        for file in files:
            filepath = os.path.join(root, file)
            try:
                with open(filepath, 'r', 
                         encoding='utf-8', errors='ignore') as f:
                    content = f.read()
                    
                    if 'supabase' in content.lower():
                        findings.append({
                            'item': 'Supabase Database',
                            'status': '🟢 Free tier available',
                            'limit': 'Up to 500MB storage, 2GB bandwidth',
                            'upgrade_when': 'Over 500 users or 500MB data'
                        })
                    
                    if 'stripe' in content.lower():
                        findings.append({
                            'item': 'Stripe Payments',
                            'status': '🟡 Pay per transaction',
                            'limit': '2.9% + 30¢ per transaction',
                            'upgrade_when': 'Always active when processing payments'
                        })
                    
                    if 'paystack' in content.lower():
                        findings.append({
                            'item': 'Paystack Payments',
                            'status': '🟡 Pay per transaction',
                            'limit': '1.5% per transaction (Nigeria)',
                            'upgrade_when': 'Always active when processing payments'
                        })
                    
                    if 'sendgrid' in content.lower() or 'nodemailer' in content.lower():
                        findings.append({
                            'item': 'Email Service',
                            'status': '🟢 Free tier available',
                            'limit': '100 emails/day free on SendGrid',
                            'upgrade_when': 'Over 100 emails per day'
                        })
                        
            except:
                continue
    
    # Remove duplicates
    seen = []
    unique_findings = []
    for f in findings:
        if f['item'] not in seen:
            seen.append(f['item'])
            unique_findings.append(f)
    
    if not unique_findings:
        print("✅ No paid services detected in your project")
        print("   Your project can run completely free!")
    else:
        for f in unique_findings:
            print(f"\n  📦 {f['item']}")
            print(f"     Status: {f['status']}")
            print(f"     Limit: {f['limit']}")
            print(f"     Pay when: {f['upgrade_when']}")
    
    print("\n" + "=" * 50)
    print("💡 Hosting recommendation:")
    print("   → Frontend: Netlify (free)")
    print("   → Backend: Railway (free tier)")
    print("   → Database: Supabase (free tier)")
    print("   → Total cost right now: $0")

def show_deploy_menu(project_path):
    """Show deployment options"""
    print(f"""
🚀 DEPLOYMENT OPTIONS
─────────────────────────────────────
  1 → Deploy to Netlify (free)
  2 → Deploy to Vercel (free)  
  3 → Analyze project costs
  4 → Back to main menu
─────────────────────────────────────
    """)
    
    choice = input("  Choose (1-4): ").strip()
    
    if choice == '1':
        deploy_to_netlify(project_path)
    elif choice == '2':
        deploy_to_vercel(project_path)
    elif choice == '3':
        analyze_costs(project_path)
    elif choice == '4':
        return
    else:
        print("❌ Invalid choice")