
try:
    import pip
except ImportError:
    os.system('sudo apt install python3-venv python3-pip')


def install(package):
    subprocess.check_call([sys.executable, "-m", "pip", "install", package])

try:
    import schedule
except ImportError:
    install("schedule")
    import schedule


def main_scheduler():
    pass
    
