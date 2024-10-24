import random

def seed_database():
    # Import app and db here to avoid circular import issues
    from app import app, db
    from models import Story, Bug, Epic

    # Push the app context so we can interact with the database
    with app.app_context():
        # Clear existing data
        db.drop_all()
        db.create_all()

        # Create Epics
        epics = [
            Epic(title="Widget Factory", description="Develop a microservice-based system for automated widget production"),
            Epic(title="User Authentication", description="Implement and improve a scalable, secure user authentication system"),
            Epic(title="Reporting Dashboard", description="Design and build a dynamic dashboard for data reporting and visualization")
        ]
        db.session.add_all(epics)
        db.session.commit()

        # Create realistic stories
        stories = [
            {
                "title": "Integrate payment gateway with microservice architecture",
                "description": "Connect the payment processing system with the widget factory microservices using REST APIs.",
                "epic": epics[0]
            },
            {
                "title": "Implement OAuth2 for third-party login",
                "description": "Add OAuth2.0 integration to allow users to log in using Google and GitHub credentials.",
                "epic": epics[1]
            },
            {
                "title": "Create filter and sorting functionality for reports",
                "description": "Add options for users to filter and sort reports by date, type, and status.",
                "epic": epics[2]
            },
            {
                "title": "Refactor user session management",
                "description": "Improve performance by refactoring the session management system to use Redis.",
                "epic": epics[1]
            }
        ]

        # Create realistic bugs
        bugs = [
            {
                "title": "Widget production line crashes under load",
                "description": "The system crashes when processing more than 1000 widgets simultaneously. Investigate memory leaks.",
                "epic": epics[0]
            },
            {
                "title": "OAuth callback URL misconfigured",
                "description": "OAuth2 callback fails due to incorrect URL routing configuration in production.",
                "epic": epics[1]
            },
            {
                "title": "Dashboard charts not rendering on Safari",
                "description": "Charts fail to load in the Safari browser due to compatibility issues with the charting library.",
                "epic": epics[2]
            },
            {
                "title": "Session timeout not handled gracefully",
                "description": "Users are not redirected to the login page after session expiration, causing application errors.",
                "epic": epics[1]
            }
        ]

        # Add stories and bugs to the database
        for story_data in stories:
            story = Story(
                title=story_data["title"],
                description=story_data["description"],
                status=random.choice(['Open', 'In Progress', 'Closed']),
                epic=story_data["epic"]
            )
            db.session.add(story)

        for bug_data in bugs:
            bug = Bug(
                title=bug_data["title"],
                description=bug_data["description"],
                status=random.choice(['Open', 'In Progress', 'Closed']),
                epic=bug_data["epic"]
            )
            db.session.add(bug)

        db.session.commit()  # Commit the created stories and bugs
        print("Database seeded successfully!")

if __name__ == "__main__":
    seed_database()
