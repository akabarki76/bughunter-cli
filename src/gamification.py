"""
Handles the gamification aspects of BugHunter CLI, such as awarding points
and granting achievements to users based on their contributions.
"""

# TODO: This should be connected to the application's database.
# For now, it's a mock object for demonstration purposes.
class MockDB:
    def execute(self, query, params):
        print(f"Executing query: {query} with params: {params}")

db = MockDB()

# TODO: This should be integrated with a real achievements system.
def grant_achievement(user_id, achievement_name):
    """Grants an achievement to a user."""
    print(f"User {user_id} has been granted the '{achievement_name}' achievement!")

# Mapping of finding severity to points awarded.
severity_to_points = {
    "critical": 100,
    "high": 50,
    "medium": 20,
    "low": 10,
    "info": 1,
}

def award_bug_hunter_points(user, finding):
    """
    Awards points to a user based on the severity of their finding and
    grants achievements based on their total points.

    Args:
        user: The user object (e.g., with an 'id' attribute).
        finding: The finding object (e.g., with a 'severity' attribute).
    """
    points = severity_to_points.get(finding.severity, 0)
    if points > 0:
        # Assuming the db object has a method to update user points.
        # This is a placeholder for the actual database logic.
        db.execute("UPDATE users SET points = points + ? WHERE id = ?", 
                  (points, user.id))
        print(f"Awarded {points} points to user {user.id} for a '{finding.severity}' finding.")

        # Placeholder for checking total points and granting achievements.
        # This would require fetching the user's new total points from the DB.
        # For demonstration, let's assume we have a way to check this.
        # if get_user_points(user.id) >= 1000:
        #     grant_achievement(user.id, "Elite Hunter")

# Example Usage (for demonstration purposes)
if __name__ == '__main__':
    class MockUser:
        def __init__(self, user_id):
            self.id = user_id

    class MockFinding:
        def __init__(self, severity):
            self.severity = severity

    # Create mock objects
    current_user = MockUser(user_id=123)
    critical_finding = MockFinding(severity="critical")
    
    # Award points
    award_bug_hunter_points(current_user, critical_finding)
