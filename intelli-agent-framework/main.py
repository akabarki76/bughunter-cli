from __init__ import create_agent

if __name__ == "__main__":
    print("Starting Intelli-Agent Framework example...")

    # Example usage from the plan
    support_bot = create_agent("configs/customer_support.yaml")
    response = support_bot.handle_query("My order #1234 is late")
    print(f"Agent response: {response}")
