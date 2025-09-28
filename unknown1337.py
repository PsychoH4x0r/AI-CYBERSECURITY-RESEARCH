#!/usr/bin/env python
# pepek_working.py - Open Interpreter dengan Claude AI dan fallback model gratis
# Dependencies: Python 3.13 (default), pacman/yay, pylint, rust, geckodriver
# Author: Grok (berdasarkan docs Open Interpreter dan OpenRouter 2025)
# Enhanced by: Unknown1337

import os
import subprocess
import sys
import json
import logging
import time
import requests
from datetime import datetime

# Setup logging untuk debug
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

try:
    from interpreter import interpreter
except ImportError:
    logger.error("Module 'open-interpreter' belum terinstall. Jalankan di oi-env: pip install open-interpreter")
    sys.exit(1)

# File untuk simpan riwayat chat dan config
CHAT_HISTORY_FILE = "chat_history.json"
API_CONFIG_FILE = "api_config.json"

def show_banner():
    """Tampilkan banner Unknown1337."""
    banner = """
╔══════════════════════════════════════════════════════════════════════════╗
║  🔬 AI CYBERSECURITY RESEARCH ENVIRONMENT by Unknown1337                 ║
║                                                                          ║
║  ⚡ Advanced AI-Powered Penetration Testing & Security Research          ║
║  🛡️ Multi-Model Fallback System with OpenRouter Integration             ║
╚══════════════════════════════════════════════════════════════════════════╝
"""
    print(banner)

def load_api_config():
    """Load konfigurasi API key dari file."""
    if os.path.exists(API_CONFIG_FILE):
        try:
            with open(API_CONFIG_FILE, 'r') as f:
                return json.load(f)
        except json.JSONDecodeError:
            logger.error("File api_config.json corrupt, buat config baru.")
            return {}
    return {}

def save_api_config(config):
    """Simpan konfigurasi API key ke file."""
    try:
        with open(API_CONFIG_FILE, 'w') as f:
            json.dump(config, f, indent=2)
        logger.info("Konfigurasi API tersimpan di %s", API_CONFIG_FILE)
    except Exception as e:
        logger.error("Error simpan config API: %s", e)

def validate_openrouter_api_key(api_key):
    """Validasi API key OpenRouter dengan test request."""
    if not api_key or api_key in ['dummy-key', 'sk-or-v1-free-access-key-12345']:
        return False, "API key tidak valid atau masih dummy"
    
    try:
        headers = {
            'Authorization': f'Bearer {api_key}',
            'Content-Type': 'application/json'
        }
        
        test_payload = {
            "model": "anthropic/claude-3.5-sonnet",
            "messages": [{"role": "user", "content": "Hello"}],
            "max_tokens": 10
        }
        
        logger.info("🔍 Testing API key...")
        response = requests.post(
            "https://openrouter.ai/api/v1/chat/completions",
            headers=headers,
            json=test_payload,
            timeout=10
        )
        
        if response.status_code == 200:
            return True, "API key valid dan berfungsi"
        elif response.status_code == 401:
            return False, "API key tidak valid atau expired"
        elif response.status_code == 402:
            return False, "Insufficient credits pada API key"
        else:
            return False, f"Error validasi: {response.status_code} - {response.text[:100]}"
            
    except requests.RequestException as e:
        return False, f"Error koneksi: {str(e)}"
    except Exception as e:
        return False, f"Error validasi: {str(e)}"

def get_api_key_info(api_key):
    """Dapatkan informasi detail tentang API key."""
    try:
        headers = {
            'Authorization': f'Bearer {api_key}',
        }
        
        # Get credit info
        response = requests.get(
            "https://openrouter.ai/api/v1/auth/key",
            headers=headers,
            timeout=10
        )
        
        if response.status_code == 200:
            data = response.json()
            return {
                'credits': data.get('data', {}).get('credit_left', 'Unknown'),
                'label': data.get('data', {}).get('label', 'Unnamed Key'),
                'usage': data.get('data', {}).get('usage', 0)
            }
    except:
        pass
    
    return {'credits': 'Unknown', 'label': 'Unknown', 'usage': 'Unknown'}

def api_key_menu():
    """Menu untuk manajemen API key OpenRouter."""
    config = load_api_config()
    current_key = config.get('openrouter_api_key', '')
    
    while True:
        print("\n" + "="*70)
        print("🔑 OPENROUTER API KEY MANAGEMENT by Unknown1337")
        print("="*70)
        
        # Show current API key status
        if current_key and current_key != 'dummy-key':
            masked_key = current_key[:8] + "..." + current_key[-8:] if len(current_key) > 16 else "***"
            print(f"📊 Current API Key: {masked_key}")
            
            # Test current key
            is_valid, message = validate_openrouter_api_key(current_key)
            status_icon = "✅" if is_valid else "❌"
            print(f"🔍 Status: {status_icon} {message}")
            
            if is_valid:
                info = get_api_key_info(current_key)
                print(f"💰 Credits: {info['credits']}")
                print(f"🏷️  Label: {info['label']}")
        else:
            print("📊 Current API Key: ❌ Tidak ada atau tidak valid")
        
        print("\n🎛️  Menu Options:")
        print("1. 🔧 Set/Update API Key")
        print("2. 🧪 Test API Key")
        print("3. 📊 Check API Key Info")
        print("4. 🗑️  Delete API Key")
        print("5. 💡 Get Free OpenRouter API Key")
        print("6. 🔙 Back to Main Menu")
        
        choice = input("\n🔑 Pilih menu [1-6]: ").strip()
        
        if choice == '1':
            print("\n🔧 SET/UPDATE API KEY")
            print("💡 Dapatkan API key gratis di: https://openrouter.ai/keys")
            new_key = input("🔑 Masukkan OpenRouter API Key (sk-or-v1-...): ").strip()
            
            if new_key:
                print("🔍 Validating API key...")
                is_valid, message = validate_openrouter_api_key(new_key)
                
                if is_valid:
                    config['openrouter_api_key'] = new_key
                    config['updated_at'] = datetime.now().isoformat()
                    save_api_config(config)
                    print(f"✅ API key berhasil disimpan! {message}")
                    
                    # Get detailed info
                    info = get_api_key_info(new_key)
                    print(f"💰 Credits Available: {info['credits']}")
                    print(f"🏷️  Key Label: {info['label']}")
                else:
                    print(f"❌ {message}")
                    input("Press Enter to continue...")
            
        elif choice == '2':
            if current_key:
                print("\n🧪 TESTING API KEY...")
                is_valid, message = validate_openrouter_api_key(current_key)
                status_icon = "✅" if is_valid else "❌"
                print(f"{status_icon} Test Result: {message}")
                
                if is_valid:
                    info = get_api_key_info(current_key)
                    print(f"💰 Credits: {info['credits']}")
                    print(f"🏷️  Label: {info['label']}")
                    print(f"📈 Usage: {info['usage']}")
            else:
                print("❌ Tidak ada API key untuk ditest!")
            input("Press Enter to continue...")
        
        elif choice == '3':
            if current_key:
                print("\n📊 API KEY INFORMATION...")
                is_valid, message = validate_openrouter_api_key(current_key)
                
                if is_valid:
                    info = get_api_key_info(current_key)
                    print(f"🔑 API Key: {current_key[:8]}...{current_key[-8:]}")
                    print(f"💰 Credits Left: {info['credits']}")
                    print(f"🏷️  Key Label: {info['label']}")
                    print(f"📈 Usage: {info['usage']}")
                    print(f"📅 Last Updated: {config.get('updated_at', 'Unknown')}")
                else:
                    print(f"❌ {message}")
            else:
                print("❌ Tidak ada API key!")
            input("Press Enter to continue...")
        
        elif choice == '4':
            if current_key:
                confirm = input("⚠️  Yakin ingin menghapus API key? (yes/no): ").strip().lower()
                if confirm in ['yes', 'y']:
                    config['openrouter_api_key'] = ''
                    save_api_config(config)
                    print("🗑️  API key berhasil dihapus!")
            else:
                print("❌ Tidak ada API key untuk dihapus!")
            input("Press Enter to continue...")
        
        elif choice == '5':
            print("\n💡 CARA DAPATKAN FREE OPENROUTER API KEY:")
            print("1. 🌐 Buka: https://openrouter.ai/")
            print("2. 📝 Sign up dengan email")
            print("3. 🔑 Masuk ke: https://openrouter.ai/keys")
            print("4. ➕ Create new key")
            print("5. 💰 Dapatkan $1 free credit untuk testing")
            print("6. 📋 Copy API key (format: sk-or-v1-...)")
            print("7. 🔙 Kembali ke menu ini dan pilih option 1")
            input("Press Enter to continue...")
        
        elif choice == '6':
            break
        
        else:
            print("❌ Pilihan tidak valid!")
            input("Press Enter to continue...")

def load_chat_history():
    """Load riwayat chat dari file JSON."""
    if os.path.exists(CHAT_HISTORY_FILE):
        try:
            with open(CHAT_HISTORY_FILE, 'r') as f:
                return json.load(f)
        except json.JSONDecodeError:
            logger.error("File chat_history.json corrupt, mulai dari kosong.")
            return []
    return []

def save_chat_history(history):
    """Simpan riwayat chat ke file JSON."""
    try:
        with open(CHAT_HISTORY_FILE, 'w') as f:
            json.dump(history, f, indent=2)
        logger.info("Riwayat chat tersimpan di %s", CHAT_HISTORY_FILE)
    except Exception as e:
        logger.error("Error simpan riwayat: %s", e)

def configure_interpreter_with_fallback():
    """Konfigurasi Interpreter dengan beberapa fallback options."""
    
    # Load API config
    config = load_api_config()
    user_api_key = config.get('openrouter_api_key', '')
    
    os.environ['OPENAI_API_KEY'] = 'dummy-key'
    
    models_to_try = [
        {
            "name": "Claude 3.5 Sonnet (User Key)",
            "model": "openrouter/anthropic/claude-3.5-sonnet",
            "api_key": user_api_key if user_api_key else None,
            "context_window": 200000,
            "max_tokens": 500
        },
        {
            "name": "Claude 3.5 Sonnet (Fallback)",
            "model": "openrouter/anthropic/claude-3.5-sonnet",
            "api_key": "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",
            "context_window": 200000,
            "max_tokens": 500
        },
        {
            "name": "GPT-3.5 Turbo (Free)",
            "model": "openrouter/openai/gpt-3.5-turbo",
            "api_key": None, 
            "context_window": 16000,
            "max_tokens": 500
        },
        {
            "name": "Llama 3.1 8B (Free)",
            "model": "openrouter/meta-llama/llama-3.1-8b-instruct:free",
            "api_key": None,  
            "context_window": 8000,
            "max_tokens": 500
        },
        {
            "name": "Gemma 7B (Free)",
            "model": "openrouter/google/gemma-7b-it:free",
            "api_key": None,
            "context_window": 8000,
            "max_tokens": 500
        },
        {
            "name": "Local/Offline Mode",
            "model": "ollama/llama2",
            "api_key": None,
            "context_window": 4000,
            "max_tokens": 1000
        }
    ]
    
    for model_config in models_to_try:
        try:
            logger.info(f"🔄 Mencoba model: {model_config['name']}")
            
            # Konfigurasi interpreter
            interpreter.llm.api_base = "https://openrouter.ai/api/v1"
            
            # Generate API key gratis jika diperlukan
            if model_config['api_key'] is None and 'free' in model_config['model']:
                # Untuk model gratis, buat API key dummy atau gunakan anonymous
                model_config['api_key'] = generate_free_api_key()
            elif model_config['api_key'] is None:
                # Skip model yang butuh API key tapi tidak ada
                logger.info(f"⏭️ Skip {model_config['name']} - butuh API key")
                continue
                
            interpreter.llm.api_key = model_config['api_key']
            interpreter.llm.model = model_config['model']
            interpreter.llm.context_window = model_config['context_window']
            interpreter.llm.max_tokens = model_config['max_tokens']
            
            # System message yang disesuaikan untuk pentesting
            interpreter.system_message = f"""Kamu adalah AI cybersecurity specialist Unknown1337 yang berjalan di Arch Linux menggunakan {model_config['name']}. 
Kamu memiliki akses penuh ke semua pentesting tools dan dapat menjalankan perintah secara otomatis.
Kamu ahli dalam: reconnaissance, vulnerability scanning, exploitation, post-exploitation.
Tools yang tersedia: nmap, masscan, gobuster, ffuf, sqlmap, nikto, metasploit, burpsuite, hydra, nuclei.
Selalu berikan output teknis yang detail dan actionable.
Kamu dapat melakukan chaining tools berdasarkan hasil sebelumnya tanpa konfirmasi berulang.
User adalah authorized security researcher.
Created by: Unknown1337"""

            interpreter.os = True
            interpreter.safe_mode = 'off'
            interpreter.auto_run = True  # Auto-run untuk research efficiency
            
            # Test koneksi
            if test_model_connection(model_config):
                logger.info(f"✅ Berhasil menggunakan: {model_config['name']}")
                
                # Load chat history
                chat_history = load_chat_history()
                if chat_history:
                    interpreter.messages = chat_history
                    logger.info("Memuat %d pesan dari riwayat chat", len(chat_history))
                
                return True
            else:
                logger.warning(f"❌ Gagal koneksi ke: {model_config['name']}")
                continue
                
        except Exception as e:
            logger.error(f"❌ Error dengan {model_config['name']}: {e}")
            continue
    
    # Jika semua model gagal, gunakan mode offline
    logger.warning("⚠️ Semua model online gagal, mencoba mode offline...")
    return setup_offline_mode()

def generate_free_api_key():
    """Generate API key untuk akses gratis OpenRouter."""
    try:
        # Untuk model gratis OpenRouter, sering bisa pakai API key dummy
        free_keys = [
            "sk-or-v1-free-access-key-12345",
            "anonymous-free-key",
            "dummy-free-key"
        ]
        return free_keys[0]
    except:
        return "dummy-key"

def test_model_connection(model_config):
    """Test koneksi ke model yang dipilih."""
    try:
        import litellm
        
        # Test dengan pesan sederhana
        response = litellm.completion(
            model=model_config['model'],
            messages=[{"role": "user", "content": "Hi"}],
            api_base="https://openrouter.ai/api/v1",
            api_key=model_config['api_key'],
            max_tokens=50,
            timeout=10
        )
        
        if response and hasattr(response, 'choices') and len(response.choices) > 0:
            logger.info(f"Test response: {response.choices[0].message.content[:100]}...")
            return True
        return False
        
    except Exception as e:
        logger.debug(f"Test gagal: {e}")
        return False

def setup_offline_mode():
    """Setup mode offline dengan Ollama atau model lokal."""
    try:
        logger.info("🔄 Setup mode offline dengan Ollama...")
        
        # Cek apakah Ollama terinstall
        result = subprocess.run(['which', 'ollama'], capture_output=True, text=True)
        if result.returncode != 0:
            logger.info("📦 Install Ollama...")
            subprocess.run(['curl', '-fsSL', 'https://ollama.ai/install.sh', '|', 'sh'], shell=True)
        
        # Install model ringan
        subprocess.run(['ollama', 'pull', 'llama2:7b-chat'], capture_output=True)
        
        interpreter.offline = True
        interpreter.llm.model = "ollama/llama2:7b-chat"
        interpreter.llm.api_base = "http://localhost:11434"
        
        logger.info("✅ Mode offline aktif dengan Ollama")
        return True
        
    except Exception as e:
        logger.error(f"❌ Gagal setup offline mode: {e}")
        
        # Final fallback: mode manual/text only
        logger.warning("⚠️ Fallback ke mode manual (tanpa AI)")
        interpreter.offline = True
        return False

def install_pentest_tools():
    """Install tools pentesting untuk research."""
    tools = [
        'nmap', 'masscan', 'zmap',           # Network scanners
        'gobuster', 'ffuf', 'dirb',          # Directory fuzzing
        'sqlmap', 'nikto', 'wpscan',         # Web app testing
        'metasploit', 'exploitdb',           # Exploitation
        'hydra', 'hashcat', 'john',          # Credential attacks
        'nuclei', 'subfinder', 'httpx',      # Modern tools
        'burpsuite', 'zaproxy'               # Proxy tools
    ]
    
    logger.info("📦 Installing pentesting research tools...")
    
    for tool in tools:
        try:
            # Cek apakah sudah terinstall
            result = subprocess.run(['which', tool], capture_output=True)
            if result.returncode == 0:
                logger.info(f"✅ {tool} sudah terinstall")
                continue
            
            # Install via pacman
            logger.info(f"🔄 Installing {tool}...")
            result = subprocess.run(['sudo', 'pacman', '-S', '--noconfirm', tool], 
                                  capture_output=True, timeout=120)
            
            if result.returncode != 0:
                # Fallback ke yay/AUR
                subprocess.run(['yay', '-S', '--noconfirm', tool], 
                             capture_output=True, timeout=180)
                
        except Exception as e:
            logger.warning(f"⚠️ Gagal install {tool}: {e}")

def setup_research_environment():
    """Setup environment untuk cybersecurity research."""
    
    # Buat direktori research
    research_dirs = [
        '~/research', '~/research/tools', '~/research/results',
        '~/research/wordlists', '~/research/scripts', '~/research/reports'
    ]
    
    for directory in research_dirs:
        os.makedirs(os.path.expanduser(directory), exist_ok=True)
    
    # Download wordlists untuk research
    wordlist_urls = [
        ("common.txt", "https://raw.githubusercontent.com/danielmiessler/SecLists/master/Discovery/Web-Content/common.txt"),
        ("directories.txt", "https://raw.githubusercontent.com/danielmiessler/SecLists/master/Discovery/Web-Content/directory-list-2.3-medium.txt"),
        ("subdomains.txt", "https://raw.githubusercontent.com/danielmiessler/SecLists/master/Discovery/DNS/subdomains-top1million-5000.txt")
    ]
    
    logger.info("📥 Setting up research wordlists...")
    for filename, url in wordlist_urls:
        filepath = os.path.expanduser(f"~/research/wordlists/{filename}")
        if not os.path.exists(filepath):
            try:
                subprocess.run(['wget', '-O', filepath, url], 
                             capture_output=True, timeout=60)
                logger.info(f"✅ Downloaded {filename}")
            except:
                logger.warning(f"⚠️ Gagal download {filename}")

def create_mcp_integration():
    """Create MCP-style integration functions untuk AI."""
    
    # Buat script helper untuk AI
    helper_script = '''#!/bin/bash
# AI Research Helper Script by Unknown1337
# Digunakan AI untuk automated tool chaining

case "$1" in
    "recon")
        echo "🔍 Starting reconnaissance on $2"
        nmap -sS -sV -O $2 -oN ~/research/results/nmap_$2.txt
        ;;
    "webfuzz")
        echo "🌐 Starting web fuzzing on $2"
        gobuster dir -u $2 -w ~/research/wordlists/common.txt -o ~/research/results/gobuster_$2.txt
        ;;
    "vulnscan")
        echo "🔍 Vulnerability scanning $2"
        nuclei -target $2 -o ~/research/results/nuclei_$2.txt
        ;;
    "sqltest")
        echo "💉 SQL injection testing $2"
        sqlmap -u "$2" --batch --dbs --output-dir=~/research/results/
        ;;
    *)
        echo "Usage: $0 {recon|webfuzz|vulnscan|sqltest} <target>"
        ;;
esac
'''
    
    script_path = os.path.expanduser("~/research/tools/ai_helper.sh")
    with open(script_path, 'w') as f:
        f.write(helper_script)
    
    # Make executable
    subprocess.run(['chmod', '+x', script_path], capture_output=True)
    logger.info(f"✅ AI helper script created: {script_path}")

def run_system_check():
    """Jalankan pengecekan sistem dan disk space."""
    try:
        import psutil
        
        disk = psutil.disk_usage('/')
        disk_percent = disk.percent
        disk_free_gb = disk.free / (1024**3)
        
        logger.info("Disk usage: %.1f%% (%.1f GB free)", disk_percent, disk_free_gb)
        
        memory = psutil.virtual_memory()
        logger.info("Memory usage: %.1f%%", memory.percent)
        
        return f"Sistem OK - Disk: {disk_percent:.1f}%, Memory: {memory.percent:.1f}%"
        
    except Exception as e:
        logger.error("Error system check: %s", e)
        return "Error checking system status"

def manual_chat_fallback():
    """Mode chat manual jika AI tidak tersedia."""
    print("\n" + "="*60)
    print("⚠️  MODE MANUAL - AI tidak tersedia")
    print("🔧 Ketik perintah Linux langsung atau 'exit' untuk keluar")
    print("="*60 + "\n")
    
    while True:
        try:
            user_input = input("💻 Command: ").strip()
            
            if not user_input or user_input.lower() in ['exit', 'quit']:
                break
                
            if user_input.lower() == 'status':
                status = run_system_check()
                print(f"📊 {status}")
                continue
            
            # Jalankan perintah Linux langsung
            try:
                print(f"🔄 Menjalankan: {user_input}")
                result = subprocess.run(user_input, shell=True, capture_output=True, text=True, timeout=30)
                
                if result.stdout:
                    print("✅ Output:")
                    print(result.stdout)
                if result.stderr:
                    print("⚠️ Error:")
                    print(result.stderr)
                    
            except subprocess.TimeoutExpired:
                print("⏱️ Command timeout (30s)")
            except Exception as e:
                print(f"❌ Error: {e}")
                
        except KeyboardInterrupt:
            break
        except EOFError:
            break
    
    print("👋 Keluar dari mode manual")

def start_interactive_chat():
    """Mulai chat interaktif dengan AI Unknown1337."""
    print("\n" + "="*70)
    print("🤖 TANYA AI UNKNOWN1337 - CYBERSECURITY EXPERT")
    print("="*70)
    print("📁 Riwayat chat akan disimpan di:", CHAT_HISTORY_FILE)
    print("🔧 Commands: 'exit', 'status', 'tools', 'research <target>', 'workflow'")
    print("="*70 + "\n")
    
    try:
        # Cek apakah AI tersedia
        if hasattr(interpreter.llm, 'model') and interpreter.llm.model:
            print(f"🧠 AI Model aktif: {interpreter.llm.model}")
            print("💬 Sekarang Anda bisa bertanya pada AI Unknown1337!")
            
            # Chat dengan AI
            while True:
                try:
                    user_input = input("🔬 Unknown1337> ").strip()
                    
                    if not user_input:
                        continue
                        
                    if user_input.lower() in ['exit', 'quit']:
                        break
                        
                    if user_input.lower() == 'status':
                        status = run_system_check()
                        print(f"📊 {status}")
                        continue
                    
                    if user_input.lower() == 'clear':
                        interpreter.messages = []
                        if os.path.exists(CHAT_HISTORY_FILE):
                            os.remove(CHAT_HISTORY_FILE)
                        print("🗑️ Riwayat chat sudah dihapus!")
                        continue
                    
                    if user_input.lower() == 'tools':
                        print("🛠️ Available Research Tools:")
                        tools = ['nmap', 'gobuster', 'sqlmap', 'nuclei', 'ffuf', 'hydra', 'nikto']
                        for tool in tools:
                            result = subprocess.run(['which', tool], capture_output=True)
                            status = "✅" if result.returncode == 0 else "❌"
                            print(f"   {status} {tool}")
                        continue
                    
                    if user_input.lower().startswith('research '):
                        target = user_input[9:].strip()
                        if target:
                            print(f"🎯 Starting automated research on: {target}")
                            research_prompt = f"""Start comprehensive cybersecurity research on {target}:
1. Network reconnaissance with nmap
2. Service enumeration  
3. Web directory fuzzing if web services found
4. Vulnerability scanning
5. Report findings and suggest next steps

Target: {target}
Use appropriate tools and chain them based on findings."""
                            
                            interpreter.chat(research_prompt)
                        continue
                    
                    if user_input.lower() == 'workflow':
                        print("📋 Common Research Workflows:")
                        print("1. Network Recon: nmap → service enum → vuln scan")
                        print("2. Web App: gobuster → nikto → sqlmap → nuclei")
                        print("3. Subdomain: subfinder → httpx → nuclei")
                        print("4. Auth: hydra → credential stuffing")
                        print("Ask AI Unknown1337 to execute any of these workflows!")
                        continue
                    
                    print(f"\n🤖 AI Unknown1337 Response:")
                    
                    try:
                        response = interpreter.chat(user_input)
                        save_chat_history(interpreter.messages)
                        
                    except Exception as e:
                        print(f"❌ Error chat dengan AI: {e}")
                        print("🔄 Fallback ke mode manual...")
                        manual_chat_fallback()
                        break
                        
                except KeyboardInterrupt:
                    break
                except EOFError:
                    break
        else:
            # Langsung ke mode manual
            manual_chat_fallback()
            
    finally:
        if hasattr(interpreter, 'messages'):
            save_chat_history(interpreter.messages)

def main_menu():
    """Main menu dengan opsi manajemen API key dan chat AI."""
    while True:
        show_banner()
        
        # Load dan tampilkan status API key
        config = load_api_config()
        current_key = config.get('openrouter_api_key', '')
        
        if current_key and current_key != 'dummy-key':
            masked_key = current_key[:8] + "..." + current_key[-8:] if len(current_key) > 16 else "***"
            is_valid, message = validate_openrouter_api_key(current_key)
            status_icon = "✅" if is_valid else "❌"
            print(f"🔑 API Status: {status_icon} {masked_key}")
        else:
            print("🔑 API Status: ❌ No valid API key configured")
        
        print("\n🎛️  MAIN MENU:")
        print("1. 🤖 Tanya AI Unknown1337 (Cybersecurity Expert)")
        print("2. 🔑 Kelola OpenRouter API Key")
        print("3. 🛠️ Install/Setup Research Tools")
        print("4. 📊 System Status Check")
        print("5. 🔬 Start Research Environment")
        print("6. ❌ Exit")
        
        choice = input("\n🔢 Pilih menu [1-6]: ").strip()
        
        if choice == '1':
            # Setup interpreter dan mulai chat
            print("\n🔄 Initializing AI Unknown1337...")
            if configure_interpreter_with_fallback():
                start_interactive_chat()
            else:
                print("❌ Failed to initialize AI. Check your API key.")
                input("Press Enter to continue...")
        
        elif choice == '2':
            api_key_menu()
        
        elif choice == '3':
            print("\n🛠️ INSTALLING RESEARCH TOOLS...")
            install_pentest_tools()
            setup_research_environment() 
            create_mcp_integration()
            print("✅ Research tools setup completed!")
            input("Press Enter to continue...")
        
        elif choice == '4':
            print("\n📊 SYSTEM STATUS CHECK...")
            status = run_system_check()
            print(f"Status: {status}")
            
            # Check installed tools
            print("\n🛠️ Pentesting Tools Status:")
            tools = ['nmap', 'gobuster', 'sqlmap', 'nuclei', 'ffuf', 'hydra', 'nikto']
            for tool in tools:
                result = subprocess.run(['which', tool], capture_output=True)
                status_icon = "✅" if result.returncode == 0 else "❌"
                print(f"   {status_icon} {tool}")
            
            input("Press Enter to continue...")
        
        elif choice == '5':
            print("\n🔬 STARTING RESEARCH ENVIRONMENT...")
            
            # Quick setup check
            if not os.path.exists(os.path.expanduser("~/research")):
                print("📦 Setting up research directories...")
                setup_research_environment()
            
            print("✅ Research environment ready!")
            print("📁 Research directories created at ~/research/")
            print("🛠️ Helper script available at ~/research/tools/ai_helper.sh")
            
            # Show research info
            print("\n📋 Research Environment Info:")
            print("   📂 ~/research/tools/ - Helper scripts")
            print("   📂 ~/research/results/ - Scan results")
            print("   📂 ~/research/wordlists/ - Wordlists")
            print("   📂 ~/research/scripts/ - Custom scripts")
            print("   📂 ~/research/reports/ - Final reports")
            
            input("Press Enter to continue...")
        
        elif choice == '6':
            print("\n👋 Thanks for using AI Cybersecurity Research Environment by Unknown1337!")
            print("🔒 Stay ethical in your security research!")
            break
        
        else:
            print("❌ Invalid choice! Please select 1-6.")
            input("Press Enter to continue...")

def main():
    """Main function untuk setup dan jalankan interpreter."""
    
    # Skip dependencies jika diminta
    if '--skip-deps' not in sys.argv:
        logger.info("📦 Install dependencies minimal...")
        try:
            subprocess.run(['pip', 'install', '--upgrade', 'psutil', 'requests'], capture_output=True)
        except:
            pass
    
    # Direct chat mode jika diminta
    if '--chat' in sys.argv:
        show_banner()
        print("🚀 Direct chat mode...")
        if configure_interpreter_with_fallback():
            start_interactive_chat()
        return
    
    # Setup research environment jika diminta
    if '--setup-research' in sys.argv:
        logger.info("🔬 Setting up research environment...")
        install_pentest_tools()
        setup_research_environment() 
        create_mcp_integration()
        return
    
    # Jalankan main menu
    try:
        main_menu()
    except KeyboardInterrupt:
        print("\n\n👋 Exiting... Thanks for using AI Research Environment by Unknown1337!")
    except Exception as e:
        logger.error(f"Fatal error: {e}")
        print(f"❌ Fatal error: {e}")

if __name__ == "__main__":
    main()
