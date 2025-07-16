from src.tool_manager import Plugin, register_plugin
import subprocess

@register_plugin("dirsearch")
class DirsearchTool(Plugin):
    dependencies = ["dirsearch"]
    
    def execute(self, target, output_file=None, **kwargs):
        cmd = ["dirsearch", "-u", target, "--json-report", "/dev/stdout"]
        result = subprocess.run(cmd, capture_output=True, text=True)
        
        if output_file:
            with open(output_file, "w") as f:
                f.write(result.stdout)
        return result.stdout
