from app import app, db
from models import Story, Bug, Epic
import logging

# Set up logging
logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)

# Import all routes
from routes import *

if __name__ == "__main__":
    with app.app_context():
        db.create_all()
        
        # Retrieve all issues and log them
        all_issues = Story.query.all() + Bug.query.all() + Epic.query.all()
        
        logger.debug("All issues retrieved from the database:")
        for issue in all_issues:
            logger.debug(f"ID: {issue.id}, Type: {issue.__class__.__name__}, Title: {issue.title}")
        
        # Check for duplicate IDs
        id_count = {}
        for issue in all_issues:
            if issue.id in id_count:
                id_count[issue.id].append(issue.__class__.__name__)
            else:
                id_count[issue.id] = [issue.__class__.__name__]
        
        duplicates = {id: types for id, types in id_count.items() if len(types) > 1}
        
        if duplicates:
            logger.warning("Duplicate IDs found:")
            for id, types in duplicates.items():
                logger.warning(f"ID {id} is used by: {', '.join(types)}")
        else:
            logger.info("No duplicate IDs found.")
    
    app.run(host="0.0.0.0", port=8080, debug=True)
