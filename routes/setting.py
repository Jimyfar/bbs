import os
import uuid

from flask import (
    render_template,
    request,
    redirect,
    url_for,
    Blueprint,
)
from werkzeug.datastructures import FileStorage

import config
from models.user import User
from routes import current_user


from utils import log

main = Blueprint('setting', __name__)


@main.route('/')
def index():
    print('running setting route')
    u = current_user()
    if u is None:
        return redirect(url_for('.index'))
    else:
        return render_template(
            'setting.html',
            user=u,
            alert_error=None,
            alert_success=None,
        )


@main.route('/update_username_and_signature', methods=['POST'])
def update_username_and_signature():
    username = request.form.get('username', '')
    signature = request.form.get('signature', '')
    u = current_user()

    if signature == '':
        # 签名为空时使用默认签名
        signature = config.default_signature
    if not User.validate_name(username):
        username = u.username
    User.update(u.id, username=username, signature=signature)
    return redirect(url_for(".index"))


@main.route('/update_password', methods=['POST'])
def update_password():
    old_password = request.form.get('old_password', '')
    new_password = request.form.get('new_password', '')
    u = current_user()
    form = dict(
        username=u.username,
        password=old_password,
        )
    # 用验证登录的方法判断用户原密码是否正确
    if User.validate_login(form) is not None and User.validate_password(new_password):
        User.update(u.id, password=User.salted_password(new_password))
        return render_template(
            'setting.html',
            user=u,
            alert_error=None,
            alert_success='修改密码成功',
        )
    else:
        return render_template(
            'setting.html',
            user=u,
            alert_error="修改密码失败",
            alert_success=None,
        )


@main.route('/image/add', methods=['POST'])
def avatar_add():
    file: FileStorage = request.files['avatar']
    # file = request.files['avatar']
    # filename = file.filename
    # ../../root/.ssh/authorized_keys
    # images/../../root/.ssh/authorized_keys
    # filename = secure_filename(file.filename)
    suffix = file.filename.split('.')[-1]
    # filename = '{}.{}'.format(str(uuid.uuid4()), suffix)
    filename = str(uuid.uuid4())
    path = os.path.join('images', filename)
    file.save(path)

    u = current_user()
    User.update(u.id, image='/images/{}'.format(filename))

    return redirect(url_for('setting.index'))

