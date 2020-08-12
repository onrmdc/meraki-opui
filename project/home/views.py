from project import db
from project.models import User, Template, Network, Device
from flask import render_template, Blueprint, request
from flask_login import login_required, current_user
from project.home.forms import NetworkDeviceForm
from project.home.functions import get_templates

# home blueprint definition
home_blueprint = Blueprint('home', __name__, template_folder='templates')


@home_blueprint.route('/', methods=['GET', 'POST'])
@login_required
def home():
    error = None
    templates_are_not_new = False
    templates_names = []
    print(current_user.id)

    if templates_are_not_new:
        Template.query.delete()  # delete existing templates in db
        templates = get_templates()  # return dictionary
        for template in templates.items():
            db_row = Template(*template)
            db.session.add(db_row)
        db.session.commit()
        templates_names = templates.keys()

    else:
        templates_db = Template.query.all()
        for template in templates_db:
            templates_names.append(template.name)

    form = NetworkDeviceForm(request.form)
    form.net_template.choices = list(templates_names)
    if request.method == 'POST':
        device_serials_list = form.serial_nos.data.strip().upper().replace(" ","").split("\r\n")
        if form.new_or_existing.data == 'existing':
            pass
        else:
            if form.net_type.data == 'firewall':
                pass
            else:
                net_name = form.net_name.data
                net_type = form.net_type.data
                user_id = current_user.id
                network = Network(net_name, net_type, user_id)
                db.session.add(network)
                db.session.commit()
                network = Network.query.filter_by(name=net_name).first()
                for device_serial in device_serials_list:
                    dev_name = device_serial.replace("-", "")
                    dev_serial = device_serial
                    network_id = network.id
                    device = Device(dev_name, dev_serial, network_id)
                    db.session.add(device)
                db.session.commit()

    return render_template('home.html', form=form, error=error)


@home_blueprint.route('/welcome')
def welcome():
    return render_template('welcome.html')  # render a template

