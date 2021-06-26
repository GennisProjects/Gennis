from app import app, render_template, redirect, request, url_for, \
    session, get_current_user, db, get_current_teacher, PhotoForm, images, flash
from models import Student, Teachers, Locations, Coments, Home, All_Charity_Sums, Shartnoma, Groups
from werkzeug.security import generate_password_hash, check_password_hash
from datetime import datetime, date, timedelta

today = date.today()
two_days = today + timedelta(days=2)


@app.route('/new_home')
def new_home():
    form = PhotoForm(meta={'csrf': False})
    user = get_current_user()
    teacher = get_current_teacher()
    try:
        if not user and not teacher:
            return redirect(url_for('nav'))
    except AttributeError:
        return redirect(url_for('nav'))

    if user and not user.director and not user.xojakent_admin and not user.chirchiq_admin and not user.gazalkent_admin:
        return redirect(url_for('find_group'))

    if not teacher and user.director and user.xojakent_admin and user.chirchiq_admin and user.gazalkent_admin:
        return redirect(url_for('all_students'))

    if teacher:
        return redirect(url_for('my_group1'))

    subject_1 = Groups.query.filter_by(id=user.group1).first()
    subject_2 = Groups.query.filter_by(id=user.group2).first()
    subject_3 = Groups.query.filter_by(id=user.group3).first()
    return render_template('new/new_home.html', user=user, form=form,
                           subject_1=subject_1, subject_2=subject_2, subject_3=subject_3)


@app.route('/')
def nav():
    return render_template('index.html')


@app.route('/register', methods=['POST', 'GET'])
def register():
    user = get_current_user()
    now = datetime.now()
    all_usernames = Student.query.order_by('id').all()
    all_usernames2 = Teachers.query.order_by('id').all()
    if request.method == 'POST':
        name = request.form.get('name').upper()
        surname = request.form.get('surname').upper()
        location = request.form.get('location2')
        username = request.form.get('username').upper()
        password = request.form.get('con_password')
        phone = request.form.get('phone')
        parent_phone = request.form.get('parent_phone')
        otasining_ismi = request.form.get('father_name').upper()
        subject_1 = request.form.get('subject_1')
        subject_2 = request.form.get('subject_2')
        subject_3 = request.form.get('subject_3')
        comment = request.form.get('comment')
        birth_year = int(request.form.get('birth_year'))
        birth_month = int(request.form.get('birth_month'))
        birth_day = int(request.form.get('birth_day'))
        a = datetime.today().year
        hash = generate_password_hash(password, method='sha256')
        age = a-birth_year
        username_check = Student.query.filter_by(username=username).all()
        for user_check in username_check:
            if user_check.username == username:
                flash('Это имя пользователя уже занято')
                return redirect(url_for('login'))


        # location1 = Locations(id=1,loc='xojakent')
        # location2 = Locations(id=2,loc='gazalkent')
        # location3 = Locations(id=3,loc='chirchiq')
        # db.session.add(location1)
        # db.session.add(location2)
        # db.session.add(location3)
        # db.session.commit()
        # print(name)
        # print(surname)
        # print(username)

        # print(location)
        # print(password)
        # print(phone)
        # print(parent_phone)
        # print(otasining_ismi)
        # print(subject_1)
        # print(subject_2)
        # print(subject_3)
        # print(birth_year)
        # print(birth_month)
        # print(birth_day)
        if location == "xojakent":
            location = 1
        elif location == "gazalkent":
            location = 2
        elif location == 'chirchiq':
            location = 3

        add = Student(name=name,
                      surname=surname,
                      age=age,
                      locations=location,
                      username=username,
                      password=hash,
                      year_born=birth_year,
                      born_day=birth_day,
                      born_month=birth_month,
                      subject_1=subject_1,
                      subject_2=subject_2,
                      subject_3=subject_3,
                      phone=phone,
                      director=False,
                      xojakent_admin=False,
                      gazalkent_admin=False,
                      chirchiq_admin=False,
                      for_group=False,
                      parent_phone=parent_phone,
                      charity=0,
                      money=0,
                      otasining_ismi=otasining_ismi,
                      join_data=now,
                      methodist=False,
                      comment=comment
                      )
        db.session.add(add)
        db.session.commit()
        if add.id == 2:
            add1 = All_Charity_Sums(id=1, bank_charity=0)
            add2 = All_Charity_Sums(id=2, bank_charity=0)
            db.session.add(add1)
            db.session.add(add2)
            db.session.commit()
        if not user:
            flash('Вы успешно зарегистрировались' + " " + name)
            return redirect(url_for('login'))
        if user:
            flash("Вы успешно зарегистрировали студента")
            return redirect(url_for('new_home'))
    return render_template('new/register_student.html', user=user, usernames=all_usernames,
                           all_usernames2=all_usernames2 )


today = datetime.today()
hour = datetime.strftime(today, "%Y/%m/%d")
hour3 = datetime.strptime(hour, "%Y/%m/%d")


@app.route('/login', methods=['POST', 'GET'])
def login():
    if request.method == 'POST':
        username = request.form.get('username').upper()
        password = request.form.get('password')
        username_sign = Student.query.filter_by(username=username).first()
        teacher_username = Teachers.query.filter_by(username=username).first()
        if username_sign and check_password_hash(username_sign.password, password):
            session['user'] = username_sign.username
            user = get_current_user()
            age = Student.query.filter_by(id=user.id).first()
            if age.year_born:
                a = datetime.today().year
                result = a - age.year_born
                Student.query.filter_by(id=user.id).update({'age': result})
                db.session.commit()
            flash(f"Добро пожаловать {user.name}")
            return redirect(url_for('new_home'))
        elif teacher_username and check_password_hash(teacher_username.password, password):
            session['teacher'] = teacher_username.username
            a = datetime.today().year
            teacher = get_current_teacher()
            age2 = Teachers.query.filter_by(id=teacher.id).first()
            if age2.year_born:
                result2 = a - age2.year_born
                Teachers.query.filter_by(id=teacher.id).update({'age': result2})
                db.session.commit()
            flash(f"Добро пожаловать {teacher.name}")
            return redirect(url_for('new_home'))
        else:
            flash('Имя пользователя или пароль неверны')
            return redirect(url_for('login'))
    return render_template('new/login.html')


@app.route('/change_infos_user', methods=['GET', 'POST'])
def change_infos_user():
    user = get_current_user()
    teacher = get_current_teacher()
    all_usernames = Student.query.order_by('id').all()
    all_usernames2 = Teachers.query.order_by('id').all()
    try:
        if not user and not teacher:
            return redirect(url_for('nav'))
    except AttributeError:
        return redirect(url_for('nav'))
    if request.method == "POST":
        password = request.form.get('password')
        print(password)
        if user:
            if check_password_hash(user.password,password):
                return redirect(url_for('change_infos_user'))
            else:
                return f"Password is incorrect {password}"
        elif teacher:
            if check_password_hash(teacher.password,password):
                return redirect(url_for('change_infos_user'))
            else:
                return f"Password is incorrect {password}"
    return render_template('new/profile_change.html',user=user,teacher=teacher,all_usernames=all_usernames,
                           all_usernames2=all_usernames2)


@app.route('/logout')
def log_out():
    user = get_current_user()
    session.pop('user', None)
    session.pop('teacher', None)
    return redirect(url_for('nav'))


@app.route('/comment_teacher/<int:teacher_id>/<int:group_id>', methods=["POST"])
def get_comment_teacher(teacher_id, group_id):
    user = get_current_user()
    try:
        if not user:
            return redirect(url_for('home'))
    except AttributeError:
        return redirect(url_for('home'))
    get_coment = request.form.get('coment')
    student = Student.query.filter_by(id=user.id).first()
    if get_coment == '':
        return 'You did not write coment'
    add = Coments(user_id=user.id, teacher_id=teacher_id, comment=get_coment)
    db.session.add(add)
    db.session.commit()
    return redirect(url_for('find_group'))


@app.route('/coment<int:id>')
def comment(id):
    user = get_current_user()
    try:
        if not user:
            return redirect(url_for('home'))
    except AttributeError:
        return redirect(url_for('home'))
    return render_template('base template/Comment_education.html', location=id, user=user)




