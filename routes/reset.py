from flask import (
    render_template,
    request,
    redirect,
    url_for,
    Blueprint,
)
import uuid
import config
from models.message import send_mail
from models.user import User
from utils import log

main = Blueprint('reset', __name__)


@main.route('/send', methods=['POST'])
def send():
    form = request.form.to_dict()

    current_user = User.one(email=form['email'])
    if current_user is None:
        return redirect(url_for('index.index'))

    token = new_reset_token(current_user.id)
    content = '重置密码地址 {}://{}:{}{}?token={}'.format(
        config.protocol,
        config.host,
        config.port,
        url_for('.view'),
        token
    )
    log('重置密码地址', content)
    send_mail('重置密码', config.admin_mail, current_user.email, content)
    return redirect(url_for('index.index'))


@main.route('/view')
def view():
    log('token', request.args.get('token'), reset_tokens)
    token = request.args.get('token', '')
    if len(token) > 0:
        return render_template('reset/view.html', token=token)
    else:
        return redirect(url_for('index.index'))


@main.route('/index')
def index():
    return render_template('reset/index.html')


@main.route("/update",methods=['POST'])
def update():
    form = request.form.to_dict()
    password = form.get('password', '')
    token = form.get('token', '')
    id = reset_tokens.get(token, None)
    log('token and id', token, id, reset_tokens)
    if id is None:
        return redirect(url_for('index.index'))
    if User.validate_password(password):
        reset_tokens.pop(token)
        User.update(id, password=User.salted_password(password))
    return redirect(url_for('index.index'))


reset_tokens = dict()


def new_reset_token(user_id):
    token = str(uuid.uuid4())
    reset_tokens[token] = user_id
    return token
