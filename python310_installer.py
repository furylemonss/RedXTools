import subprocess
import sys
import os
import urllib.request
import time
import modules.rpc_manager as rpc_manager
rpc_manager.set_details("Downloading Python 3.10")

os.system("cls")

def ensure_package(pkg):
    try:
        __import__(pkg)
    except:
        subprocess.check_call([sys.executable, "-m", "pip", "install", pkg])

ensure_package("colorama")
ensure_package("tqdm")

from colorama import Fore, Style, init
from tqdm import tqdm

init(autoreset=True)

PY310_URL = "https://www.python.org/ftp/python/3.10.0/python-3.10.0-amd64.exe"
PY310_INSTALLER = "python-3.10.0-amd64.exe"
VENV_PATH = ".venv"
REQUIREMENTS_FILE = "requirements.txt"


def run(cmd):
    subprocess.check_call(cmd, shell=True)


def python310_exists():
    try:
        subprocess.check_output("py -3.10 --version", shell=True)
        return True
    except:
        return False


def ask_confirmation():
    while True:
        answer = input(
            Fore.YELLOW
            + "Python 3.10 is required. Do you approve installation? (Y/N): "
        ).strip().lower()
        if answer == "y":
            return True
        if answer == "n":
            return False


def download_with_progress(url, filename):
    response = urllib.request.urlopen(url)
    total = int(response.getheader("Content-Length"))
    with open(filename, "wb") as file, tqdm(
        desc=Fore.CYAN + "Downloading Python 3.10",
        total=total,
        unit="B",
        unit_scale=True,
        unit_divisor=1024,
    ) as bar:
        while True:
            chunk = response.read(1024)
            if not chunk:
                break
            file.write(chunk)
            bar.update(len(chunk))


def install_python310():
    if not os.path.exists(PY310_INSTALLER):
        print(Fore.CYAN + "Downloading installer...")
        download_with_progress(PY310_URL, PY310_INSTALLER)

    print(Fore.GREEN + "Installing Python 3.10 silently...")
    run(f"{PY310_INSTALLER} /quiet InstallAllUsers=1 PrependPath=1 Include_pip=1")
    time.sleep(8)


def ensure_venv():
    if not os.path.isdir(VENV_PATH):
        print(Fore.CYAN + "Creating virtual environment...")
        run("py -3.10 -m venv " + VENV_PATH)
    else:
        print(Fore.GREEN + ".venv already exists, using existing environment.")

    return os.path.join(VENV_PATH, "Scripts", "python.exe")


def get_installed_packages(python_path):
    try:
        output = subprocess.check_output(
            f'"{python_path}" -m pip list --format=freeze',
            shell=True
        ).decode()

        installed = set()
        for line in output.splitlines():
            if "==" in line:
                name = line.split("==")[0].lower()
                installed.add(name)
        return installed
    except Exception as e:
        print(Fore.YELLOW + f"Warning: Could not check installed packages: {str(e)}")
        return set()


def get_required_packages():
    required = []
    if not os.path.exists(REQUIREMENTS_FILE):
        print(Fore.YELLOW + f"Warning: {REQUIREMENTS_FILE} not found, using default packages")
        return ['colorama', 'tqdm', 'requests', 'pywebview', 'pillow']
    try:
        with open(REQUIREMENTS_FILE, "r", encoding="utf-8") as f:
            for line in f:
                line = line.strip()
                if line and not line.startswith('#'):
                    pkg_name = line.split('==')[0].split('>=')[0].split('<=')[0].split('<')[0].split('>')[0].strip()
                    if pkg_name:
                        required.append(pkg_name.lower())
            os.system("python -3.10 -m pip install pywebview")
        return required
    except Exception as e:
        print(Fore.RED + f"Error reading requirements.txt: {str(e)}")
        return []


def ensure_requirements(python_path):
    print(Fore.CYAN + "Checking and installing required packages...")

    installed = get_installed_packages(python_path)
    required = get_required_packages()

    if not required:
        print(Fore.YELLOW + "No packages to install.")
        return

    missing = []
    for pkg in required:
        if pkg not in installed:
            missing.append(pkg)

    if not missing:
        print(Fore.GREEN + "All requirements already satisfied.")
        return

    print(Fore.YELLOW + f"Installing {len(missing)} missing package(s):")
    for pkg in missing:
        print(Fore.CYAN + f"  → Installing {pkg}...")
        try:
            subprocess.check_call(
                f'"{python_path}" -m pip install {pkg} --quiet',
                shell=True
            )
            print(Fore.GREEN + f"  ✓ {pkg} installed successfully")
        except Exception as e:
            print(Fore.RED + f"  ✗ Failed to install {pkg}: {str(e)}")

    print(Fore.GREEN + "\nPackage installation completed!")


print(Style.BRIGHT + Fore.MAGENTA + "\n=== Environment Setup for Valorant Checker ===\n")


def ensure_environment():
    try:
        if not python310_exists():
            if not ask_confirmation():
                print(Fore.RED + "Operation cancelled. Python 3.10 is required.")
                return False
            install_python310()
            
            if not python310_exists():
                print(Fore.RED + "Python 3.10 installation failed or not detected.")
                return False

        python_path = ensure_venv()
        
        ensure_requirements(python_path)
        
        print(Fore.GREEN + "\n✓ Environment setup complete!")
        print(Fore.GREEN + "✓ Ready to run Valorant Checker")
        return True
        
    except Exception as e:
        print(Fore.RED + f"\n✗ Error during setup: {str(e)}")
        import traceback
        traceback.print_exc()
        return False


if __name__ == "__main__":
    success = ensure_environment()
    if success:
        print(Fore.GREEN + "\nSetup completed successfully!")
    else:
        print(Fore.RED + "\nSetup failed!")
    input("\nPress Enter to exit...")