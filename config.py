# ============================================
# VULCAN - Configuration File
# ============================================
# Built by @nechecodes

import os

# --- VULCAN IDENTITY ---
AGENT_NAME = "Vulcan"
AGENT_VERSION = "1.0"
AGENT_TAGLINE = "The AI That Builds, Fixes & Deploys"

# --- AI MODEL SETTINGS ---
OFFLINE_MODEL = "qwen2.5-coder:1.5b"
ONLINE_MODEL = "deepseek-chat"

# --- API KEYS ---
GEMINI_API_KEY = ""
DEEPSEEK_API_KEY = ""

# --- AGENT SETTINGS ---
MAX_LOOP_COUNT = 2
SCAN_INTERVAL = 30
MAX_FILE_SIZE_KB = 500

# --- FILE TYPES TO SCAN ---
SUPPORTED_EXTENSIONS = [
    '.py', '.js', '.ts', '.html',
    '.css', '.php', '.jsx', '.tsx',
    '.json', '.sql'
]

# --- VAULT ---
VAULT_FILE = "vault_locked.json"

# --- REPORTS ---
REPORT_FILE = "vulcan_report.txt"
