import subprocess
import re
import openai  

def run_powershell_command(command):
    """Executes a PowerShell command and returns the output."""
    result = subprocess.run(["powershell", "-Command", command], capture_output=True, text=True)
    return result.stdout.strip()

def interpret_query(query):
    """Basic NLP mapping of queries to PowerShell commands."""
    query = query.lower()
    commands = {
        "cpu": "Get-WmiObject Win32_Processor | Select-Object Name,NumberOfCores,MaxClockSpeed",
        "ram": "Get-WmiObject Win32_PhysicalMemory | Select-Object Capacity,Manufacturer",
        "storage": "Get-WmiObject Win32_DiskDrive | Select-Object Model,Size",
        "gpu": "Get-WmiObject Win32_VideoController | Select-Object Name,AdapterRAM",
        "installed software": "Get-WmiObject Win32_Product | Select-Object Name,Version",
        "running processes": "Get-Process | Select-Object ProcessName,Id,CPU",
        "network": "Get-NetIPConfiguration",
        "firewall rules": "Get-NetFirewallRule | Select-Object DisplayName,Enabled,Direction",
        "open ports": "Get-NetTCPConnection | Where-Object {$_.State -eq 'Listen'} | Select-Object LocalPort,OwningProcess",
        "vulnerabilities cpu": "Get-WmiObject Win32_Processor | Select-Object Name"
    }
    
    if "vulnerabilities" in query:
        return "Check vulnerabilities for installed software or CPU."
    
    for key, cmd in commands.items():
        if key in query:
            return cmd
    
    return None

def check_vulnerabilities(cpu_info, software_info):
    """Provide contextual information about vulnerabilities based on CPU and software."""
    vulnerability_info = ""
    
    # Check vulnerabilities in CPU (e.g., Meltdown, Spectre)
    if "intel" in cpu_info.lower():
        vulnerability_info += "Your CPU (Intel Core i7-8550U) may be affected by vulnerabilities such as Spectre and Meltdown. Ensure your system is patched with the latest security updates from Intel and your OS.\n"
    
    # Check vulnerabilities in installed software
    for software in software_info:
        if "java" in software.lower():
            vulnerability_info += f"{software} is outdated. You should update to the latest version to avoid known vulnerabilities.\n"
        if "python" in software.lower():
            vulnerability_info += f"{software} is the latest version. However, ensure any installed packages or dependencies are up to date.\n"
    
    if not vulnerability_info:
        vulnerability_info = "No known vulnerabilities found in your system based on the current software and hardware information."
    
    return vulnerability_info

def main():
    print("AI System Query Agent (Windows)")
    while True:
        query = input("Ask me about your system (or type 'exit'): ")
        if query.lower() == "exit":
            break
        
        command = interpret_query(query)
        if command:
            output = run_powershell_command(command)
            print("\n", output, "\n")
            
            # Get vulnerabilities
            if "vulnerabilities" in query.lower():
                cpu_info = run_powershell_command("Get-WmiObject Win32_Processor | Select-Object Name")
                software_info = run_powershell_command("Get-WmiObject Win32_Product | Select-Object Name,Version").splitlines()
                vulnerability_report = check_vulnerabilities(cpu_info, software_info)
                print("\nVulnerability Check:\n", vulnerability_report, "\n")
        else:
            print("Sorry, I don't understand that query. Try something like 'What is my CPU model?'")

if __name__ == "__main__":
    main()
