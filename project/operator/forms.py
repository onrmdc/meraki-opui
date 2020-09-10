from flask_wtf import FlaskForm
from wtforms import StringField, SelectField, TextAreaField, SelectMultipleField
from wtforms.validators import DataRequired, Length
from flask_login import current_user
from project.models import Network


class NewNetworkForm(FlaskForm):
    net_name = StringField('Network Name: ', validators=[Length(max=64)])
    net_template = SelectField('Template: ', choices=[])
    net_type = SelectField('Network Type: ', choices=["appliance", "switch", "wireless"])
    new_or_existing = SelectField("New", choices=[("new", "New Network"), ("existing", "Existing Network")], )
    net_tag_mselect = SelectMultipleField("Select Tags:", validators=[DataRequired()])

    def set_choices(self):
        tag_list = []
        for group in current_user.groups:
            tag_list.extend(group.tags)
        self.net_tag_mselect.choices = [(tag.id, tag.name) for tag in tag_list]


class AddDevicesForm(FlaskForm):
    serial_nos = TextAreaField('Serial Numbers, one per line: ', validators=[DataRequired(), Length(max=2000)])
    registered_nets = SelectField('Network: ', choices=[])

    def set_choices(self):
        user_networks = Network.query.filter_by(user_id=current_user.id)
        self.registered_nets.choices = [(network.id, network.name) for network in user_networks]
        user_groups = current_user.groups
        for user_group in user_groups:
            if user_group.networks:
                group_networks = user_group.networks
                self.registered_nets.choices.extend([(network.id, network.name) for network in group_networks])