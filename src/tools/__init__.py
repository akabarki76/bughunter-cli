from .nmap import NmapTool
from .nikto import NiktoTool
from .dirsearch import DirsearchTool
from .sqlmap import SqlmapTool
from .waybackurls import WaybackurlsTool
from .nuclei import NucleiTool
from .forecast import ForecastTool
from .config import ConfigTool
from .map import MapTool

TOOL_REGISTRY = {
    "nmap": NmapTool,
    "nikto": NiktoTool,
    "dirsearch": DirsearchTool,
    "sqlmap": SqlmapTool,
    "waybackurls": WaybackurlsTool,
    "nuclei": NucleiTool,
    "forecast": ForecastTool,
    "config": ConfigTool,
    "map": MapTool,
}