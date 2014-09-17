__author__ = 'Beryl'
from flask_wtf import Form
from wtforms import TextField,DateField, IntegerField, SelectField
from wtforms.validators import DataRequired

class AddTaskForm(Form):
    task_id = ImportError('Priority')
    name = TextField('Task Name',validators=[DataRequired()])
    due_date = DateField('Date Due (mm/dd/yyyy)', validators=[DateRequired()], format='%m/%d/%Y')
    priority = SelectField(  'Priority', validators=[DataRequired()], choices=[('1', '1'), ('2', '2'), ('3', '3'), ('4', '4'), ('5',
'5'), ('6', '6'), ('7', '7'), ('8', '8'), ('9', '9'), ('10', '10') ] )
status = IntegerField('Status')