from app import redirect, render_template, url_for, get_current_user, app, or_, request, get_current_teacher, PhotoForm, \
    images, db, flash
from models import Student, Groups, Attendance, ReasonAbsentDays, Teachers, Coments
from jinja2 import UndefinedError
from datetime import datetime, date, timedelta

# baho qoyishga datetime
today = datetime.today()
hour = datetime.strftime(today, "%Y/%m/%d/%H")
hour2 = datetime.strptime(hour, "%Y/%m/%d/%H")
add = hour2 + timedelta(hours=1)


###################################


@app.route('/info')
def info():
    user = get_current_user()
    teacher = get_current_teacher()
    try:
        if not user and not teacher:
            return redirect(url_for('nav'))
    except AttributeError:
        return redirect(url_for('nav'))
    form = PhotoForm(meta={'csrf': False})
    return render_template('new_continue/student_profile.html', user=user, form=form, teacher=teacher)


@app.route('/fill_data_contract',methods=['POST'])
def fill_data_contract():
    user = get_current_user()
    try:
        if not user:
            return redirect(url_for('nav'))
    except AttributeError:
        return redirect(url_for('nav'))
    vakil_name = request.form.get('vakil_name')
    vakil_surname = request.form.get('vakil_surname')
    vakil_phone = request.form.get('vakil_phone')
    vakil_father = request.form.get('vakil_father')
    Student.query.filter_by(id=user.id).update({'vakilning_ismi': vakil_name, 'vakilning_familyasi': vakil_surname,
                                                'vakilning_telefon_raqami': vakil_phone,
                                                'vakilning_otchestvasi': vakil_father})
    db.session.commit()
    flash('Спасибо за ваши данные. Скоро вы получите свой контракт.')
    return redirect(url_for('find_group'))


@app.route('/group1', methods=['POST', 'GET'])
def find_group():
    user = get_current_user()
    try:
        if not user:
            return redirect(url_for('nav'))
    except AttributeError:
        return redirect(url_for('nav'))
    form = PhotoForm(meta={'csrf': False})
    group = Groups.query.filter_by(id=user.group1).first()
    group2 = Groups.query.filter_by(id=user.group2).first()
    group3 = Groups.query.filter_by(id=user.group3).first()
    return render_template('new_continue/student/student_group.html', user=user, group=group, group2=group2,
                           group3=group3, form=form)


@app.route('/student_inside_group/<int:group_id>')
def student_inside_group(group_id):
    user = get_current_user()
    teacher = get_current_teacher()
    try:
        if not user:
            return redirect(url_for('nav'))
    except AttributeError:
        return redirect(url_for('nav'))
    group = Groups.query.filter_by(id=group_id).first()
    students = Student.query.filter(or_(Student.group1 == group_id, Student.group2 == group_id,
                                        Student.group3 == group_id)).order_by('id').all()
    return render_template('new_continue/student/student_inside_group.html', user=user, teacher=teacher, group=group,
                           students=students)


@app.route('/student_attendance/<int:group_id>')
def student_attendance(group_id):
    user = get_current_user()
    try:
        if not user:
            return redirect(url_for('nav'))
    except AttributeError:
        return redirect(url_for('nav'))
    form = PhotoForm(meta={'csrf': False})
    student = Student.query.filter_by(id=user.id).first()
    attendance_present = Attendance.query.filter_by(student_id=user.id, group_id=group_id,
                                                    apset=None).order_by(Attendance.id.desc()).limit(30)
    num_lessons = []
    net_average = 0
    total = []

    for att in attendance_present:
        baho = att.ortacha_baho
        num_lessons.append(baho)
        net_average += baho
        a = net_average / len(num_lessons)
        b = a * 10
        c = round(b)
        total = c / 10

    attendance_absent = Attendance.query.filter_by(student_id=user.id, group_id=group_id,
                                                   present=None).order_by(Attendance.id.desc()).limit(30)

    return render_template('new_continue/student/student_attendance.html', user=user, student=student,
                           attendance_present=attendance_present, form=form,
                           attendance_absent=attendance_absent, group_id=group_id, total=total)


@app.route('/reason_day/<check_id>', methods=["POST"])
def make_reason_day(check_id):
    completed = request.get_json()['completed']
    todo_id = Attendance.query.get(check_id)
    todo_id.for_sabab = completed
    db.session.commit()
    return "yes"


@app.route('/apset_days<int:student_id><int:group_id>')
def apset_days(student_id, group_id):
    user = get_current_user()
    try:
        if not user:
            return redirect(url_for('nav'))
    except AttributeError:
        return redirect(url_for('nav'))
    apset_days = Attendance.query.filter_by(student_id=student_id, group_id=group_id).all()
    return render_template('student/apset_days.html', apset_days=apset_days, user=user)


@app.route('/save_reason/<int:student_id>/<int:group_id>', methods=["POST", "GET"])
def save_reason(student_id, group_id):
    user = get_current_user()
    try:
        if not user:
            return redirect(url_for('nav'))
    except AttributeError:
        return redirect(url_for('nav'))
    teacher = get_current_teacher()
    reason = request.form.get('reason')
    form = PhotoForm(meta={'csrf': False})
    student = Student.query.filter_by(id=student_id).first()
    get = Attendance.query.filter_by(for_sabab=True).first()
    if not get:
        flash('Дни не выбраны')
        return redirect(url_for('student_attendance',group_id=group_id))
    if form.validate_on_submit():
        filename = images.save(form.image.data)
        image_url = images.url(filename)
        reason_day = ReasonAbsentDays(student_id=user.id,
                                      img_due_days=image_url, reason_due=reason,
                                      date_abset=get.apset, group_id=get.group_id, student_locations=student.locations)
        db.session.add(reason_day)
        db.session.commit()
    flash('Запрос успешно отправлен')
    return redirect(url_for('student_attendance', group_id=group_id))


@app.route('/apset/<int:group_id>/<int:student_id>')
def apsets_for_groups(group_id, student_id):
    user = get_current_user()
    try:
        if not user:
            return redirect(url_for('nav'))
    except AttributeError:
        return redirect(url_for('nav'))
    attendance = Attendance.query.filter_by(group_id=group_id, student_id=student_id).order_by('id').all()
    return render_template('Teacher/Apset_for_my_attendance.html', user=user, attendance=attendance, group_id=group_id,
                           student_id=student_id)


@app.route('/lessons')
def lessons():
    user = get_current_user()
    try:
        if not user:
            return redirect(url_for('nav'))
    except AttributeError:
        return redirect(url_for('nav'))
    return render_template('subjects/student_lesson_page.html')


@app.route('/get_lesson/<lesson>')
def get_lesson(lesson):
    user = get_current_user()
    try:
        if not user:
            return redirect(url_for('nav'))
    except AttributeError:
        return redirect(url_for('nav'))
    if lesson == "ielts":
        return render_template('subjects/ielts_lessons.html')
    return "Hello"
