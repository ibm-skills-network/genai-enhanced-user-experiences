from flask import render_template, request, jsonify, flash, redirect, url_for
from app import app, db
from models import Issue, Story, Bug, Epic
from wizard import extract_json_from_response, get_llm_suggestions, apply_changes  # Import wizard helpers
from search import simple_search, semantic_search

# Redirect root path `/` to `/issues`
@app.route('/')
def root():
    return redirect(url_for('index_issues'))

# GET /issues - List all issues (index action)
@app.route('/issues', methods=['GET'])
def index_issues():
    search_query = request.args.get('query')
    if search_query:
        issues = simple_search(search_query)

        # TODO: try using semantic search instead
        # issues = semantic_search(search_query)
    else:
        issues = Issue.query.all()
    return render_template('issues/index.html', issues=issues, search_query=search_query)

# GET /issues/new - Form to create a new issue (new action)
@app.route('/issues/new', methods=['GET'])
def new_issue():
    epics = Epic.query.all()
    return render_template('issues/create.html', epics=epics)

# POST /issues - Create a new issue (create action)
@app.route('/issues', methods=['POST'])
def create_issue():
    issue_type = request.form.get('issue_type')
    title = request.form.get('title')
    description = request.form.get('description')
    epic_id = request.form.get('epic_id')

    new_issue = create_issue_object(issue_type, title, description, epic_id)
    if new_issue:
        db.session.add(new_issue)
        db.session.commit()
        flash(f"New {issue_type} created successfully!", "success")
        return redirect(url_for('index_issues'))
    else:
        flash("Failed to create new issue. Invalid issue type.", "error")
        return redirect(url_for('new_issue'))

# GET /issues/<int:id> - Show a specific issue (show action)
@app.route('/issues/<int:id>', methods=['GET'])
def show_issue(id):
    issue = Issue.query.get_or_404(id)
    return render_template('issues/show.html', issue=issue)

# GET /issues/<int:id>/edit - Form to edit an existing issue (edit action)
@app.route('/issues/<int:id>/edit', methods=['GET'])
def edit_issue(id):
    issue = Issue.query.get_or_404(id)
    epics = Epic.query.all()
    return render_template('issues/edit.html', issue=issue, epics=epics)

# PATCH/PUT /issues/<int:id> - Update an existing issue (update action)
@app.route('/issues/<int:id>', methods=['PATCH', 'PUT'])
def update_issue(id):
    issue = Issue.query.get_or_404(id)
    update_issue_fields(issue, request.form)
    db.session.commit()
    flash("Issue updated successfully!", "success")
    return redirect(url_for('show_issue', id=issue.id))

# DELETE /issues/<int:id> - Delete an issue
@app.route('/issues/<int:id>', methods=['DELETE', 'POST'])
def delete_issue(id):
    issue = Issue.query.get_or_404(id)
    db.session.delete(issue)
    db.session.commit()
    if request.method == 'DELETE':
        return jsonify({"message": "Issue deleted successfully"}), 200
    flash("Issue deleted", "success")
    return redirect(url_for('index_issues'))

# Wizard Routes (using functions from wizard.py)
@app.route('/wizard_prompt', methods=['GET', 'POST'])
def wizard_prompt():
    return render_template('wizard_prompt.html')

@app.route('/wizard', methods=['GET'])
def wizard():
    action = request.args.get('action')
    if action:
        return render_template('wizard.html', prompt=action)
    else:
        return render_template('wizard.html', error="Failed to get suggestions from the LLM", prompt=action)

@app.route('/wizard_suggestions', methods=['GET'])
def wizard_suggestions():
    action = request.args.get('action')
    if action:
        diffs = get_llm_suggestions(action)
        if diffs:
            for diff in diffs:
                issue = Issue.query.get(diff['id'])
                diff['title'] = issue.title if issue else 'Unknown Issue'
            return jsonify({"diffs": diffs})
        else:
            return jsonify({"error": "Failed to get suggestions from the LLM"}), 500
    return jsonify({"error": "No prompt provided."}), 400

@app.route('/wizard/apply', methods=['POST'])
def apply_wizard_changes():
    form_data = request.json.get('form_data')
    return apply_changes(form_data)


# Helper methods
def create_issue_object(issue_type, title, description, epic_id=None):
    if issue_type == 'story':
        return Story(title=title, description=description, epic_id=epic_id)
    elif issue_type == 'bug':
        return Bug(title=title, description=description, epic_id=epic_id)
    elif issue_type == 'epic':
        return Epic(title=title, description=description)
    return None

def update_issue_fields(issue, form_data):
    for field, value in form_data.items():
        if field != 'issue_id' and hasattr(issue, field):
            setattr(issue, field, value)

# Error handling
@app.errorhandler(405)
def method_not_allowed(e):
    return jsonify(error=str(e)), 405
