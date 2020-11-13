from flask_wtf import FlaskForm
from wtforms import StringField
from wtforms.validators import URL


class WebsiteForm(FlaskForm):
    address = StringField('address', validators=[URL()])
