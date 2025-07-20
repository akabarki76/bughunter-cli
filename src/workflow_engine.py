import click
from src.tool_manager import get_plugin, load_plugins

def execute_workflow(workflow: list, initial_context: dict = None) -> dict:
    """Orchestrates plugin execution with dependency management and context passing.

    Args:
        workflow: A list of dictionaries, where each dictionary represents a step
                  and contains 'plugin' (str) and 'config' (dict, optional).
        initial_context: An optional dictionary to start the workflow context.

    Returns:
        The final context dictionary after all workflow steps have been executed.
    """
    load_plugins() # Ensure all plugins are loaded
    context = initial_context if initial_context is not None else {}

    click.echo("[*] Starting workflow execution...")

    for i, step in enumerate(workflow):
        plugin_name = step.get("plugin")
        plugin_config = step.get("config", {})

        if not plugin_name:
            click.echo(f"Error: Workflow step {i+1} is missing 'plugin' name.", err=True)
            continue

        click.echo(f"[*] Executing step {i+1}: Plugin '{plugin_name}'...")
        try:
            plugin_instance = get_plugin(plugin_name)
            # Pass the current context and step-specific config to the plugin's execute method
            # The plugin's execute method is responsible for merging/using this config
            # and updating the context.
            context = plugin_instance.execute(context=context, **plugin_config)
            click.echo(f"[+] Step {i+1} ('{plugin_name}') completed successfully.")
        except Exception as e:
            click.echo(f"Error executing plugin '{plugin_name}' in step {i+1}: {e}", err=True)
            # Depending on desired behavior, you might want to break here or continue
            # For now, we'll continue to allow other steps to potentially run.
            continue

    click.echo("[*] Workflow execution finished.")
    return context
