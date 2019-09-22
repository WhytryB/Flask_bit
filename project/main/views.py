#################
#### imports ####
#################

from flask import render_template, Blueprint
from flask_login import login_required


################
#### config ####
################

main_blueprint = Blueprint('main', __name__,)


################
#### routes ####
################

@main_blueprint.route('/sss')
@login_required
def home():
    return render_template('index.html')