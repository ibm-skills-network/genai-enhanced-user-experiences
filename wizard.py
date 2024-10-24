import json
import re
import logging
from flask import jsonify
from models import Issue
from generate import generate_text
from app import db

logger = logging.getLogger(__name__)

def extract_json_from_response(response_text):
    """
    Extracts the JSON content from a WatsonX response text by finding the first
    valid JSON-like structure.
    """
    match = re.search(r'(\[.*\])', response_text, re.DOTALL)
    if match:
        json_str = match.group(1)
        try:
            return json.loads(json_str)
        except json.JSONDecodeError as e:
            logger.error(f"Error parsing JSON: {e}")
            return None
    else:
        logger.info("No JSON found in the response")
        return None

def get_llm_suggestions(user_prompt):
    """Send the prompt to LLM and return suggested field changes across multiple issues in JSON format."""
    issues = Issue.query.all()
    issues_json = [
        {
            "id": issue.id,
            "title": issue.title,
            "description": issue.description,
            "status": issue.status,
            "type": issue.type
        }
        for issue in issues
    ]

    issues_json_str = json.dumps(issues_json, indent=4)

    llm_prompt = f"""
    TODO: write your prompt here
    """

    try:
        logger.info(f"LLM prompt: {llm_prompt}")
        response = generate_text(llm_prompt)
        logger.info(f"LLM response: {llm_prompt}")

        try:
            fields = json.loads(response)
            return fields
        except json.JSONDecodeError:
            logger.error(f"Failed to parse LLM response as JSON: {response}")
            return None

    except Exception as e:
        logger.error(f"Failed to get LLM suggestions: {e}")
        return None

def apply_changes(form_data):
    """Apply the accepted changes from the diff to the issue."""
    issue_id = form_data.get('issue_id')
    issue = Issue.query.get_or_404(issue_id)

    for field in form_data['fields']:
        setattr(issue, field['name'], field['proposed'])

    db.session.commit()
    return jsonify({"message": "Changes applied successfully!"})
