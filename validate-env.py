#!/usr/bin/env python3
"""
AITuneCreator Environment Validator
Checks if the environment is properly configured for running the application
"""

import os
import sys
from pathlib import Path
from dotenv import load_dotenv

# Colors for output
class Colors:
    HEADER = '\033[95m'
    BLUE = '\033[94m'
    CYAN = '\033[96m'
    GREEN = '\033[92m'
    YELLOW = '\033[93m'
    RED = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'

def print_header(text):
    print(f"\n{Colors.BOLD}{Colors.BLUE}==== {text} ===={Colors.ENDC}")

def print_success(text):
    print(f"{Colors.GREEN}✓{Colors.ENDC} {text}")

def print_warning(text):
    print(f"{Colors.YELLOW}⚠{Colors.ENDC} {text}")

def print_error(text):
    print(f"{Colors.RED}✗{Colors.ENDC} {text}")

def print_info(text):
    print(f"{Colors.CYAN}ℹ{Colors.ENDC} {text}")

def check_python_version():
    """Check if Python version is 3.11 or higher"""
    print_header("Python Version Check")

    version_info = sys.version_info
    version_str = f"{version_info.major}.{version_info.minor}.{version_info.micro}"

    if version_info.major >= 3 and version_info.minor >= 11:
        print_success(f"Python {version_str} (OK)")
        return True
    else:
        print_warning(f"Python {version_str} found, but 3.11+ recommended")
        return True  # Still allow, but warn

def check_virtual_environment():
    """Check if running in a virtual environment"""
    print_header("Virtual Environment Check")

    in_venv = hasattr(sys, 'real_prefix') or (
        hasattr(sys, 'base_prefix') and sys.base_prefix != sys.prefix
    )

    if in_venv:
        print_success(f"Running in virtual environment: {sys.prefix}")
        return True
    else:
        print_warning("Not running in a virtual environment (recommended: activate venv)")
        return False

def check_dependencies():
    """Check if all required dependencies are installed"""
    print_header("Dependencies Check")

    required = {
        'streamlit': 'Streamlit Web Framework',
        'langchain': 'LangChain LLM Orchestration',
        'langchain_groq': 'Groq LangChain Integration',
        'music21': 'Music Theory Library',
        'synthesizer': 'Audio Synthesis',
        'scipy': 'Scientific Computing',
        'dotenv': 'Environment Variable Loading'
    }

    all_ok = True
    for package, description in required.items():
        try:
            __import__(package)
            print_success(f"{package:<20} - {description}")
        except ImportError:
            print_error(f"{package:<20} - {description} (NOT INSTALLED)")
            all_ok = False

    return all_ok

def check_environment_files():
    """Check if environment files exist and are configured"""
    print_header("Environment Files Check")

    env_type = os.getenv('ENV', 'not set')
    print_info(f"Current ENV variable: {Colors.CYAN}{env_type}{Colors.ENDC}")

    if env_type == 'not set':
        print_warning("ENV variable not set. Using default: 'dev'")

    # Check for environment files
    env_files = {
        '.env.dev': 'Development (local)',
        '.env.test': 'Testing',
        '.env.prod': 'Production'
    }

    found_any = False
    for filename, description in env_files.items():
        if os.path.exists(filename):
            print_success(f"{filename:<15} exists ({description})")
            found_any = True
        else:
            print_warning(f"{filename:<15} missing ({description})")

    if not found_any:
        print_error("No environment files found (.env.dev, .env.test, .env.prod)")
        return False

    return True

def check_groq_api_key():
    """Check if GROQ_API_KEY is configured"""
    print_header("Groq API Key Check")

    # Determine which env file to check
    env_type = os.getenv('ENV', 'dev')
    env_file = f'.env.{env_type}'

    if not os.path.exists(env_file):
        print_warning(f"Environment file {env_file} not found")
        return False

    # Load environment from file
    load_dotenv(env_file)

    api_key = os.getenv('GROQ_API_KEY')

    if api_key:
        # Show masked version
        masked = api_key[:10] + '*' * (len(api_key) - 15) + api_key[-5:] if len(api_key) > 20 else '*' * len(api_key)
        print_success(f"GROQ_API_KEY is set in {env_file}")
        print_info(f"Key preview: {Colors.CYAN}{masked}{Colors.ENDC}")
        return True
    else:
        print_error(f"GROQ_API_KEY is not set in {env_file}")
        print_info(f"Add your Groq API key to {env_file}")
        print_info(f"Get one from: https://console.groq.com")
        return False

def check_app_structure():
    """Check if application files exist"""
    print_header("Application Structure Check")

    files_to_check = {
        'app.py': 'Main Streamlit app',
        'app/__init__.py': 'App package init',
        'app/main.py': 'MusicLLM class',
        'app/utils.py': 'Utility functions',
        'requirements.txt': 'Dependencies list',
        'setup.py': 'Package setup',
        '.env.example': 'Environment template'
    }

    all_ok = True
    for filename, description in files_to_check.items():
        if os.path.exists(filename):
            print_success(f"{filename:<20} - {description}")
        else:
            print_error(f"{filename:<20} - {description} (MISSING)")
            all_ok = False

    return all_ok

def check_llm_initialization():
    """Try to initialize the MusicLLM class"""
    print_header("LLM Initialization Check")

    # Load environment first
    env_type = os.getenv('ENV', 'dev')
    env_file = f'.env.{env_type}'

    if os.path.exists(env_file):
        load_dotenv(env_file)

    try:
        from app.main import MusicLLM
        print_info("Attempting to initialize MusicLLM...")
        llm = MusicLLM()
        print_success("MusicLLM initialized successfully")
        return True
    except ImportError as e:
        print_error(f"Failed to import MusicLLM: {e}")
        return False
    except Exception as e:
        print_error(f"Failed to initialize MusicLLM: {e}")
        if "GROQ_API_KEY" in str(e):
            print_info("Make sure GROQ_API_KEY is set in your environment file")
        return False

def print_summary(results):
    """Print validation summary"""
    print_header("Validation Summary")

    total = len(results)
    passed = sum(1 for v in results.values() if v)

    if passed == total:
        print_success(f"All checks passed ({passed}/{total})")
        print("\nYou're ready to run the application!")
        return True
    else:
        print_warning(f"Some checks failed ({passed}/{total} passed)")
        print("\nPlease fix the issues above before running the application.")
        return False

def main():
    print(f"{Colors.BOLD}{Colors.BLUE}")
    print("╔════════════════════════════════════════╗")
    print("║   AITuneCreator Environment Validator  ║")
    print("╚════════════════════════════════════════╝")
    print(f"{Colors.ENDC}")

    results = {
        'Python Version': check_python_version(),
        'Virtual Environment': check_virtual_environment(),
        'Dependencies': check_dependencies(),
        'Environment Files': check_environment_files(),
        'API Configuration': check_groq_api_key(),
        'App Structure': check_app_structure(),
        'LLM Initialization': check_llm_initialization(),
    }

    success = print_summary(results)

    print(f"\n{Colors.CYAN}For detailed setup instructions, see DEVELOPER_GUIDE.md{Colors.ENDC}\n")

    sys.exit(0 if success else 1)

if __name__ == '__main__':
    main()
