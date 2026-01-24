import os
import platform
import subprocess
import urllib.request
import tarfile
import zipfile

# Cores para o terminal
BLUE = "\033[94m"
GREEN = "\033[92m"
YELLOW = "\033[93m"
RED = "\033[91m"
BOLD = "\033[1m"
RESET = "\033[0m"

# Sua lógica original de caminhos
user_docs = os.path.join(os.path.expanduser('~'), "Documents")
work_dir = os.path.join(user_docs, "Wandi Studio", "Engine", "arduino")

def setup_arduino_cli():
    # Criando o ambiente de trabalho
    if not os.path.exists(work_dir):
        print(f"{BLUE}Criando diretorio de trabalho em: {work_dir}{RESET}")
        os.makedirs(work_dir, exist_ok=True)
    
    system = platform.system().lower()
    print(f"{BLUE}Sistema detectado: {system.capitalize()}. Iniciando configuracao...{RESET}")

    # Definição de URLs e Binários
    if system == "windows":
        url = "https://downloads.arduino.cc/arduino-cli/arduino-cli_latest_Windows_64bit.zip"
        archive_path = os.path.join(work_dir, "cli.zip")
        exe_name = "arduino-cli.exe"
    else:
        url = f"https://downloads.arduino.cc/arduino-cli/arduino-cli_latest_{system.capitalize()}_64bit.tar.gz"
        archive_path = os.path.join(work_dir, "cli.tar.gz")
        exe_name = "arduino-cli"

    exe_path = os.path.join(work_dir, exe_name)
    config_file = os.path.join(work_dir, "arduino-cli.yaml")

    # 1. Download do Binário
    if not os.path.exists(exe_path):
        print(f"{YELLOW}Baixando Arduino CLI oficial...{RESET}")
        urllib.request.urlretrieve(url, archive_path)
        
        print(f"{YELLOW}Extraindo arquivos do motor...{RESET}")
        if archive_path.endswith(".zip"):
            with zipfile.ZipFile(archive_path, 'r') as zip_ref:
                zip_ref.extractall(work_dir)
        else:
            with tarfile.open(archive_path, 'r:gz') as tar_ref:
                tar_ref.extractall(work_dir)
        os.remove(archive_path)
        print(f"{GREEN}Motor instalado com sucesso.{RESET}")

    # Função para execução com output colorido original do arduino-cli
    def run_cli_visible(args):
        # O comando transporta as cores originais do arduino-cli para o seu terminal
        cmd = [exe_path] + args + ["--config-file", config_file]
        return subprocess.run(cmd, cwd=work_dir)

    print(f"\n{BOLD}--- CONFIGURACAO DO AMBIENTE WANDI STUDIO ---{RESET}\n")
    
    # Inicializar configuração local
    if not os.path.exists(config_file):
        print(f"{BLUE}Gerando arquivo de configuracao local...{RESET}")
        run_cli_visible(["config", "init", "--overwrite"])

    # 2. Sincronização
    print(f"\n{YELLOW}Atualizando indice de pacotes...{RESET}")
    run_cli_visible(["core", "update-index"])

    # 3. Instalação de Placas (AVR)
    print(f"\n{YELLOW}Instalando plataforma Arduino AVR (Uno, Nano, Mega)...{RESET}")
    run_cli_visible(["core", "install", "arduino:avr"])

    # 4. Instalação de Bibliotecas solicitadas
    libs = [
        "Servo", "Stepper", "LiquidCrystal", 
        "Adafruit Unified Sensor", "DHT sensor library"
    ]
    
    print(f"\n{BLUE}Instalando bibliotecas do projeto...{RESET}")
    for lib in libs:
        print(f"\n{BOLD}Processando: {lib}{RESET}")
        run_cli_visible(["lib", "install", lib])

    print(f"\n{GREEN}{BOLD}" + "="*50)
    print("PROCEDIMENTO CONCLUIDO COM SUCESSO")
    print(f"Ambiente pronto em: {work_dir}")
    print("="*50 + f"{RESET}")

if __name__ == "__main__":
    try:
        # Habilita cores no terminal Windows caso necessário
        if platform.system().lower() == "windows":
            os.system('color') 
            
        setup_arduino_cli()
    except Exception as e:
        print(f"\n{RED}Erro durante a execucao: {e}{RESET}")