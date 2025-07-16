from src.tool_manager import Plugin, register_plugin
import subprocess

@register_plugin("nikto")
class NiktoTool(Plugin):
    dependencies = ["nikto"]
    
    def execute(self, target, output_file=None, **kwargs):
        cmd = ["nikto", "-h", target]
        result = subprocess.run(cmd, capture_output=True, text=True)
        
        if output_file:
            with open(output_file, "w") as f:
                f.write(result.stdout)
        return result.stdout
