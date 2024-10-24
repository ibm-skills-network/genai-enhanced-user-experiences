from app import db
from sqlalchemy.orm import relationship, backref, Mapped
from sqlalchemy.dialects.postgresql import JSON
from sqlalchemy import event
from datetime import datetime
from embeddings import get_embeddings

# Mixin for timestamp fields
class TimestampMixin(object):
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

# The main Issue model, which other models (Story, Bug, Epic) inherit from
class Issue(TimestampMixin, db.Model):
    __tablename__ = 'issues'
    id = db.Column(db.Integer, primary_key=True)
    type = db.Column(db.String(50))  # Polymorphic identity for subclasses
    title = db.Column(db.String(100), nullable=False)
    description = db.Column(db.Text)
    status = db.Column(db.String(20), default='Open')
    epic_id = db.Column(db.Integer, db.ForeignKey('issues.id', ondelete='SET NULL'))  # Self-referential FK for epics

    # Self-referential relationship for an epic and its child issues (stories, bugs, etc.)
    children = relationship("Issue", backref=backref('epic', remote_side=[id]))

    # Relationships to Diff (for changes tracked in issues)
    diffs = relationship("Diff", back_populates="issue", cascade="all, delete-orphan")

    # JSON columns for embeddings (optional)
    embedding = db.Column(JSON)

    # Setup for polymorphic inheritance for different issue types
    __mapper_args__ = {
        'polymorphic_identity': 'issue',
        'polymorphic_on': type
    }

# Subclasses for different issue types
class Story(Issue):
    __mapper_args__ = {
        'polymorphic_identity': 'story',
    }

class Bug(Issue):
    __mapper_args__ = {
        'polymorphic_identity': 'bug',
    }

class Epic(Issue):
    __mapper_args__ = {
        'polymorphic_identity': 'epic',
    }

    @property
    def stories(self):
        """Get all stories associated with this epic."""
        return [child for child in self.children if child.type == 'story']

    @property
    def bugs(self):
        """Get all bugs associated with this epic."""
        return [child for child in self.children if child.type == 'bug']


# Diff model to track changes on issues
class Diff(db.Model):
    __tablename__ = 'diffs'
    id = db.Column(db.Integer, primary_key=True)
    issue_id = db.Column(db.Integer, db.ForeignKey('issues.id', ondelete='CASCADE'), nullable=False)
    field = db.Column(db.String(50), nullable=False)
    current_value = db.Column(db.Text)
    suggested_value = db.Column(db.Text)
    action = db.Column(db.String(20), nullable=False)

    # Relationship back to Issue
    issue: Mapped['Issue'] = relationship('Issue', back_populates='diffs')

@event.listens_for(Issue, 'before_insert', propagate=True)
def generate_embeddings_before_insert(mapper, connection, target):
    """Automatically generate embeddings before inserting a new issue."""
    target.embedding = get_embeddings(f"{target.title} {target.description}")
