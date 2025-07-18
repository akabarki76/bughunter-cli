import os
import importlib
import pkgutil
import shutil
import subprocess
import platform
import click

PLUGIN_REGISTRY = {}

def register_plugin(name):
    """A decorator to register a new plugin."""
    def decorator(cls):
        PLUGIN_REGISTRY[name] = cls
        return cls
    return decorator

class Plugin:
    """Base class for all plugins."""
    dependencies = []

    def __init__(self):
        self._check_dependencies()

    def _check_dependencies(self):
        """Checks if all required dependencies for the plugin are installed."""
        missing_deps = [dep for dep in self.dependencies if not shutil.which(dep)]
        if missing_deps:
            if click.confirm(f"Plugin '{self.__class__.__name__}' requires the following missing dependencies: {', '.join(missing_deps)}. Do you want to attempt to install them now?"):
                self._install_dependencies(missing_deps)
            else:
                raise click.ClickException(f"Missing dependencies: {', '.join(missing_deps)}")

    def _install_dependencies(self, deps):
        """Attempts to install missing dependencies based on the OS."""
        system = platform.system()
        if system == "Linux":
            # Attempt to use apt, yum, or pacman
            if shutil.which("apt-get"):
                cmd = ["sudo", "apt-get", "install", "-y"] + deps
            elif shutil.which("yum"):
                cmd = ["sudo", "yum", "install", "-y"] + deps
            elif shutil.which("pacman"):
                cmd = ["sudo", "pacman", "-S", "--noconfirm"] + deps
            else:
                raise click.ClickException("Could not find a supported package manager (apt, yum, pacman). Please install dependencies manually.")
        elif system == "Darwin": # macOS
            if shutil.which("brew"):
                cmd = ["brew", "install"] + deps
            else:
                raise click.ClickException("Homebrew not found. Please install it or install dependencies manually.")
        else:
            raise click.ClickException(f"Unsupported OS: {system}. Please install dependencies manually.")

        try:
            subprocess.run(cmd, check=True)
            click.echo("Dependencies installed successfully.")
        except subprocess.CalledProcessError as e:
            raise click.ClickException(f"Failed to install dependencies: {e}")
        except FileNotFoundError:
            raise click.ClickException(f"Could not execute installation command. Is sudo installed and configured?")


    def execute(self, **kwargs):
        """Executes the plugin's main functionality."""
        raise NotImplementedError

def load_plugins():
    """Dynamically loads all plugins from the 'plugins' directory."""
    plugins_dir = os.path.join(os.path.dirname(__file__), 'plugins')
    for _, name, _ in pkgutil.iter_modules([plugins_dir]):
        importlib.import_module(f'src.plugins.{name}')

def get_plugin(name):
    """Retrieves a plugin from the registry."""
    if name not in PLUGIN_REGISTRY:
        raise click.ClickException(f"Plugin '{name}' not found.")
    return PLUGIN_REGISTRY[name]()
