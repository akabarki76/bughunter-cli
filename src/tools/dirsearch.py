from src.utils.tool_registration import register_tool, BaseTool
import subprocess

@register_tool("dirsearch")
class DirsearchTool(BaseTool):
    name = "dirsearch"

    def is_installed(self):
        return subprocess.run(["which", "dirsearch"], capture_output=True).returncode == 0

    def run(self, target, output_file=None, **kwargs):
        cmd = ["dirsearch", "-u", target, "--json-report", "/dev/stdout"]
        result = subprocess.run(cmd, capture_output=True, text=True)
        
        if output_file:
            with open(output_file, "w") as f:
                f.write(result.stdout)
        return result.stdout
