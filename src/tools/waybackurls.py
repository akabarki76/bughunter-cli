# src/tools/waybackurls.py
from src.utils.tool_registration import register_tool, BaseTool
import subprocess

@register_tool("waybackurls")
class WaybackurlsTool(BaseTool):
    name = "waybackurls"
    
    def is_installed(self):
        return subprocess.run(["which", "waybackurls"], capture_output=True).returncode == 0

    def run(self, target, output_file=None, **kwargs):
        cmd = ["waybackurls", target]
        result = subprocess.run(cmd, capture_output=True, text=True)
        
        if output_file:
            with open(output_file, "w") as f:
                f.write(result.stdout)
        return result.stdout
