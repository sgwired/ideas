from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField
from wtforms.validators import DataRequired
from wtforms.ext.sqlalchemy.fields import QuerySelectField

from ..models import Idea


class IdeaForm(FlaskForm):
    """
    Form  to add or edit a idea
    """
    name = StringField('Name', validators=[DataRequired()])
    category = StringField('Category', validators=[DataRequired()])
    description = StringField('Description', validators=[DataRequired()])
    retailer = StringField('Other Retailers', validators=[DataRequired()])
    submit = SubmitField('Submit')
