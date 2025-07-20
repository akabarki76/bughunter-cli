# src/tools/nmap.py
from src.utils.tool_registration import register_tool, BaseTool
import subprocess

@register_tool("nmap")
class NmapTool(BaseTool):
    name = "nmap"
    
    def is_installed(self):
        return subprocess.run(["which", "nmap"], capture_output=True).returncode == 0

    def run(self, target, output_file=None, ports="1-1000", **kwargs):
        cmd = ["nmap", "-sV", "-p", ports, target]
        result = subprocess.run(cmd, capture_output=True, text=True)
        
        if output_file:
            with open(output_file, "w") as f:
                f.write(result.stdout)
        return result.stdout
