from flask_wtf import FlaskForm
from wtforms import SubmitField, StringField, IntegerField, SelectField, \
    DateField, validators, ValidationError

from .models import Position


class PositionForm(FlaskForm):
    name = StringField(label='Position name', validators=[validators.DataRequired()])
    department = StringField(label='Position department')
    wage = IntegerField(label='Position wage', validators=[validators.DataRequired()])
    submit = SubmitField(label='Save position')

    def validate_wage(self, wage):
        if wage.data < 0:
            raise ValidationError('Wage cannot be < 0')


class EmployeeForm(FlaskForm):
    name = StringField(label='Employee name')
    birth_date = DateField(label='birth date')
    position_id = SelectField(label='Position')
    submit = SubmitField(label='Save employee')

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        result = []
        for position in Position.query.all():
            result.append((position.id, position.name))
        self.position_id.choices = result
