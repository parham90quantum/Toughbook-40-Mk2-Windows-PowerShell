import tkinter as tk
from tkinter import scrolledtext
import time
import ctypes

class FakePowerShell:
    def __init__(self, root):
        self.root = root
        myappid = 'Microsoft.Windows.PowerShell.1337'
        try:
            ctypes.windll.shell32.SetCurrentProcessExplicitAppUserModelID(myappid)
        except:
            pass
        self.root.title("Windows PowerShell")
        self.root.geometry("950x650")
        self.root.configure(bg="#012456")
        
        # سیستم فایل فیک!
        self.current_path = "C:\\Users\\Hacker"
        self.fake_filesystem = {
            "C:\\Users\\Hacker": {
                "type": "dir",
                "children": {
                    "Desktop": {"type": "dir", "children": {}},
                    "Documents": {"type": "dir", "children": {
                        "Mission Brief.txt": {"type": "file", "size": "1.2 KB"},
                        "Target List.xlsx": {"type": "file", "size": "4.5 KB"}
                    }},
                    "Downloads": {"type": "dir", "children": {}},
                    "Toughbook_Specs.pdf": {"type": "file", "size": "2.8 MB"},
                    ".secret": {"type": "dir", "children": {}}
                }
            },
            "C:\\Program Files": {
                "type": "dir",
                "children": {
                    "Toughbook Tools": {"type": "dir", "children": {}}
                }
            }
        }
        
        self.setup_ui()
        self.print_welcome()
        
    def setup_ui(self):
        # هدر با دکمه‌های کنترل
        header = tk.Frame(self.root, bg="#1e1e1e", height=30)
        header.pack(fill="x")
        
        # دکمه‌های ویندوز
        controls = tk.Frame(header, bg="#1e1e1e")
        controls.pack(side="left", padx=10)
        
        for color in ["#FF5F56", "#FFBD2E", "#27C93F"]:
            dot = tk.Canvas(controls, width=12, height=12, bg="#1e1e1e", highlightthickness=0)
            dot.pack(side="left", padx=2)
            dot.create_oval(2, 2, 10, 10, fill=color, outline="")
        
        # عنوان
        title = tk.Label(header, text="Windows PowerShell (Toughbook Emulator)", 
                        bg="#1e1e1e", fg="white", font=("Segoe UI", 10))
        title.pack(side="left", padx=10)
        
        # ترمینال
        terminal_frame = tk.Frame(self.root, bg="#012456")
        terminal_frame.pack(fill="both", expand=True, padx=10, pady=10)
        
        self.terminal = scrolledtext.ScrolledText(
            terminal_frame,
            bg="#0C0C0C",
            fg="#CCCCCC",
            insertbackground="white",
            font=("Consolas", 11),
            wrap="word",
            borderwidth=0,
            highlightthickness=0
        )
        self.terminal.pack(fill="both", expand=True)
        
        # تگ‌های رنگی
        self.terminal.tag_config("path", foreground="#FFFF00")
        self.terminal.tag_config("command", foreground="#FFFF00")
        self.terminal.tag_config("prompt", foreground="#FFB900")
        self.terminal.tag_config("output", foreground="#CCCCCC")
        self.terminal.tag_config("directory", foreground="#569CD6")
        self.terminal.tag_config("file", foreground="#4EC9B0")
        self.terminal.tag_config("error", foreground="#F48771")
        self.terminal.tag_config("property", foreground="#569CD6")
        self.terminal.tag_config("value", foreground="#4EC9B0")
        
        self.terminal.bind("<Key>", self.on_key)
        self.terminal.bind("<Return>", self.on_enter)
        self.current_line = ""
        self.command_history = []
        self.history_index = 0
        
    def print_welcome(self):
        welcome = [
            "Windows PowerShell",
            "Copyright (C) Microsoft Corporation. All rights reserved.",
            "",
            "Install the latest PowerShell for new features and improvements! https://aka.ms/PSWindows",
            "",
            "╔════════════════════════════════════════════════════════════╗",
            "║     TOUGHBOOK 40 MK2 - JOINT SPECIAL OPERATIONS COMMAND   ║",
            "║              Classified Workstation - Level 3             ║",
            "╚════════════════════════════════════════════════════════════╝",
            ""
        ]
        for line in welcome:
            self.terminal.insert("end", line + "\n", "output")
        
        self.print_prompt()
        
    def print_prompt(self):
        prompt_path = self.current_path.replace("C:\\Users\\", "C:\\Users\\")
        self.terminal.insert("end", f"PS {prompt_path}> ", "prompt")
        self.terminal.see("end")
        self.current_line = ""
        
    def on_key(self, event):
        if event.char and event.char.isprintable():
            self.terminal.insert("end", event.char, "command")
            self.current_line += event.char
            return "break"
        elif event.keysym == "BackSpace":
            pos = self.terminal.index("end-1c")
            if self.terminal.get(pos + "-1c") != ">":
                self.terminal.delete("end-2c", "end-1c")
                self.current_line = self.current_line[:-1]
            return "break"
        elif event.keysym == "Up":
            # تاریخچه دستورات
            if self.command_history:
                # پاک کردن خط فعلی
                for _ in range(len(self.current_line)):
                    self.terminal.delete("end-2c", "end-1c")
                self.current_line = self.command_history[-1]
                self.terminal.insert("end", self.current_line, "command")
            return "break"
            
    def on_enter(self, event):
        self.terminal.insert("end", "\n", "output")
        command = self.current_line.strip()
        
        if command:
            self.command_history.append(command)
            self.history_index = len(self.command_history)
            
        self.execute_command(command)
        self.print_prompt()
        self.current_line = ""
        return "break"
    
    def execute_command(self, command):
        if not command:
            return
            
        parts = command.lower().split()
        cmd = parts[0]
        args = parts[1:] if len(parts) > 1 else []
        
        # =============== دستورات پوورشل ===============
        if cmd == "get-computerinfo":
            self.show_toughbook_info()
            
        elif cmd in ["cls", "clear"]:
            self.terminal.delete(1.0, "end")
            
        elif cmd in ["dir", "ls"]:
            self.list_directory()
            
        elif cmd == "cd":
            self.change_directory(args[0] if args else "")
            
        elif cmd == "pwd":
            self.terminal.insert("end", f"{self.current_path}\n", "path")
            
        elif cmd == "mkdir":
            if args:
                self.terminal.insert("end", f"Directory created: {self.current_path}\\{args[0]}\n", "value")
            else:
                self.terminal.insert("end", "mkdir : Missing argument\n", "error")
                
        elif cmd == "echo":
            text = " ".join(args)
            self.terminal.insert("end", f"{text}\n", "output")
            
        elif cmd == "hostname":
            self.terminal.insert("end", "TOUGHBOOK-40-MK2\n", "value")
            
        elif cmd == "whoami":
            self.terminal.insert("end", "hacker\\jsoc_operator\n", "value")
            
        elif cmd == "ipconfig":
            self.show_fake_ipconfig()
            
        elif cmd == "systeminfo":
            self.show_systeminfo()
            
        elif cmd == "exit":
            self.terminal.insert("end", "Goodbye!\n", "output")
            self.root.after(1000, self.root.destroy)
            
        elif cmd == "help":
            self.show_help()
            
        else:
            # ارور حرفه‌ای برای دستورات ناشناخته
            self.terminal.insert("end", f"{cmd} : The term '{cmd}' is not recognized as the name of a cmdlet, function, script file, or operable program.\n", "error")
            self.terminal.insert("end", "Check the spelling of the name, or if a path was included, verify that the path is correct and try again.\n", "error")
    
    def list_directory(self):
        """لیست فایل‌ها و پوشه‌های فیک"""
        self.terminal.insert("end", "\n    Directory: ", "property")
        self.terminal.insert("end", f"{self.current_path}\n\n", "path")
        
        # پوشه والد
        if self.current_path != "C:\\":
            self.terminal.insert("end", "d-----", "directory")
            self.terminal.insert("end", "  ", "output")
            self.terminal.insert("end", "..\n", "directory")
        
        # فایل‌های فیک
        fake_files = [
            ("Desktop", "dir", "d-----"),
            ("Documents", "dir", "d-----"),
            ("Downloads", "dir", "d-----"),
            ("Toughbook_Specs.pdf", "file", "-a----"),
            (".secret", "dir", "d--h--"),
            ("Mission Planner.exe", "file", "-a----"),
            ("Satellite Link.ps1", "file", "-a----"),
        ]
        
        for name, ftype, attrs in fake_files:
            self.terminal.insert("end", f"{attrs}", "property")
            self.terminal.insert("end", "  ", "output")
            if ftype == "dir":
                self.terminal.insert("end", f"{name}/\n", "directory")
            else:
                self.terminal.insert("end", f"{name}\n", "file")
    
    def change_directory(self, path):
        if not path or path == "~":
            self.current_path = "C:\\Users\\Hacker"
        elif path == "..":
            if "\\" in self.current_path:
                self.current_path = "\\".join(self.current_path.split("\\")[:-1])
        elif path == "\\" or path == "/":
            self.current_path = "C:\\"
        else:
            # شبیه‌سازی تغییر دایرکتوری
            self.current_path = f"C:\\Users\\Hacker\\{path}"
    
    def show_toughbook_info(self):
        """اطلاعات حماسی Toughbook 40 Mk2"""
        info = [
            "",
            "ComputerName           : TOUGHBOOK-40-MK2",
            "WindowsVersion         : Windows 11 Pro for Workstations (24H2)",
            "OSArchitecture         : 64-bit",
            "Processor              : Intel Core Ultra 7 165H (16 Cores, 22 Threads)",
            "  Base Speed          : 3.8 GHz",
            "  Max Speed           : 5.0 GHz",
            "  Cache               : 24 MB Intel Smart Cache",
            "Memory                 : 64 GB DDR5-5600 (4x16GB, Dual Channel)",
            "Graphics               : Intel Arc Graphics (8GB shared)",
            "Storage                : 2 TB NVMe SSD Opal 2.0 Self-Encrypting",
            "Battery                : 2x Hot-swap 68Wh (41 hours runtime)",
            "Durability            : MIL-STD-810H, MIL-STD-461F, IP66",
            "Operating Temp        : -29°C to +63°C (-20°F to +145°F)",
            "Shock Resistance      : 180 cm drop (6 feet) - 26 drops",
            "Vibration             : Vehicle mounted, 5-500Hz, 3.04 Grms",
            "Altitude              : 15,000 ft operating, 40,000 ft non-operating",
            "Water/Dust            : IP66 (dust tight, powerful water jets)",
            "",
            "[HARDWARE SECURITY]",
            "TPM                    : 2.0 (dedicated chip)",
            "Secure Boot           : Enabled",
            "BitLocker             : AES-256, Fully encrypted",
            "SmartCard Reader      : Integrated",
            "Fingerprint Sensor    : Capacitive touch",
            "IR Camera             : Windows Hello",
            "",
            "[COMMUNICATIONS]",
            "Wireless              : Intel Wi-Fi 6E AX211, Bluetooth 5.3",
            "Cellular              : 5G NR Sub-6, 4G LTE Advanced Pro",
            "GPS                   : GPS/GLONASS/BeiDou/Galileo",
            "Satellite             : Optional Iridium Certus",
            "",
            "[UNIQUE FEATURES]",
            "• Night Vision compatible display (dimmable to 0.1 nits)",
            "• 1200 nit sunlight-readable touchscreen",
            "• Gloved and wet finger support",
            "• Bridge battery system - zero downtime hot swap",
            "• XFillin noise-cancelling microphone array",
            "• Quad-rugged I/O doors",
            "",
            "PS C:\\Users\\hacker> $env:CLASSIFICATION",
            "TOP SECRET//SI/TK//NOFORN",
            ""
        ]
        
        # انیمیشن لودینگ
        self.terminal.insert("end", "\n[*] Fetching system information... ", "property")
        self.terminal.see("end")
        self.root.update()
        time.sleep(0.8)
        self.terminal.insert("end", "DONE\n\n", "value")
        
        for line in info:
            if ":" in line and not "//" in line:
                prop, val = line.split(":", 1)
                self.terminal.insert("end", f"{prop}:", "property")
                self.terminal.insert("end", f"{val}\n", "value")
            else:
                color = "property" if "[" in line or "•" in line else "output"
                self.terminal.insert("end", line + "\n", color)
    
    def show_fake_ipconfig(self):
        """IP کانفیگ فیک"""
        ips = [
            "Windows IP Configuration",
            "",
            "Ethernet adapter Ethernet0:",
            "   Connection-specific DNS Suffix  . : jsoc.mil",
            "   IPv4 Address. . . . . . . . . . . : 10.42.23.15",
            "   Subnet Mask . . . . . . . . . . . : 255.255.255.0",
            "   Default Gateway . . . . . . . . . : 10.42.23.1",
            "",
            "Wireless LAN adapter Wi-Fi:",
            "   Connection-specific DNS Suffix  . : jsoc.mil",
            "   IPv4 Address. . . . . . . . . . . : 172.16.88.103",
            "   Subnet Mask . . . . . . . . . . . : 255.255.0.0",
            "   Default Gateway . . . . . . . . . : 172.16.0.1",
            "",
            "Tunnel adapter SecureLink:",
            "   IPv4 Address. . . . . . . . . . . : 192.168.247.2",
            "   Subnet Mask . . . . . . . . . . . : 255.255.255.255",
            "   Description . . . . . . . . . . . : Fortinet VPN Tunnel"
        ]
        
        for line in ips:
            self.terminal.insert("end", line + "\n", "output")
    
    def show_systeminfo(self):
        """سیستم‌اینفوی خلاصه"""
        info = [
            "Host Name:                 TOUGHBOOK-40-MK2",
            "OS Name:                   Microsoft Windows 11 Pro for Workstations",
            "OS Version:                10.0.26080 N/A Build 26080",
            "OS Manufacturer:           Microsoft Corporation",
            "System Manufacturer:       Panasonic Corporation",
            "System Model:             Toughbook 40 Mk2 (CF-40MK2)",
            "System Type:              x64-based PC",
            "Processor(s):             1 Processor(s) Installed.",
            "                          [01]: Intel64 Family 6 Model 183 Stepping 1 GenuineIntel ~3800 Mhz",
            "BIOS Version:             American Megatrends Inc. 3.26, 2/14/2025",
            "Total Physical Memory:    65,536 MB",
            "Available Physical:       58,924 MB",
            "Virtual Memory:           Max Size: 75,000 MB",
            "Virtual Memory:           Available: 67,500 MB",
            "Page File:               pagefile.sys",
            "Domain:                  jsoc.mil",
            "Logon Server:           \\\\DC01",
            "Hotfix(s):              12 Hotfix(s) Installed.",
            "Network Card(s):         Intel Wi-Fi 6E AX211, Qualcomm Snapdragon X65 5G"
        ]
        
        for line in info:
            if ":" in line:
                prop, val = line.split(":", 1)
                self.terminal.insert("end", f"{prop}:", "property")
                self.terminal.insert("end", f"{val}\n", "value")
            else:
                self.terminal.insert("end", line + "\n", "output")
    
    def show_help(self):
        """کمک"""
        help_text = [
            "",
            "Common PowerShell Commands:",
            "  Get-ComputerInfo     Display Toughbook 40 Mk2 system specifications",
            "  cls, clear          Clear the console",
            "  dir, ls             List files and directories",
            "  cd <path>           Change directory",
            "  pwd                 Show current directory",
            "  mkdir <name>        Create a new directory",
            "  echo <text>         Display text",
            "  hostname            Show computer name",
            "  whoami              Show current user",
            "  ipconfig            Display network configuration",
            "  systeminfo          Show system summary",
            "  exit                Close PowerShell",
            "  help                Show this help message",
            ""
        ]
        
        for line in help_text:
            self.terminal.insert("end", line + "\n", "output")

if __name__ == "__main__":
    root = tk.Tk()
    app = FakePowerShell(root)
    root.mainloop()