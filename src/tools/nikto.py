from src.utils.tool_registration import register_tool, BaseTool
import subprocess

@register_tool("nikto")
class NiktoTool(BaseTool):
    name = "nikto"

    

    def run(self, target, output_file=None, **kwargs):
        cmd = ["nikto", "-h", target]
        result = subprocess.run(cmd, capture_output=True, text=True)
        
        if output_file:
            with open(output_file, "w") as f:
                f.write(result.stdout)
        return result.stdout
