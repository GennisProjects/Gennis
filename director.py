from app import get_current_user, render_template, redirect, url_for, db, app, request, or_, PhotoForm, flash
from models import Student, Teachers, Groups, Attendance, ReasonAbsentDays, due_days, All_Charity_Sums


@app.route('/delete_teacher/<teacher_id>')
def delete_teacher(teacher_id):
    user = get_current_user()
    try:
        if not user.director:
            return redirect(url_for('nav'))
    except AttributeError:
        return redirect(url_for('nav'))
    delete = Teachers.query.filter_by(id=teacher_id).first()
    delete.delete()
    flash('Учитель успешно удален')
    return redirect(url_for('new_home'))


@app.route('/teachers')
def teacher():
    user = get_current_user()
    form = PhotoForm(meta={'csrf': False})
    try:
        if not user.director and not user.gazalkent_admin and not user.xojakent_admin and not user.chirchiq_admin:
            return redirect(url_for('nav'))
    except AttributeError:
        return redirect(url_for('nav'))
    teachers = Teachers.query.order_by('id').all()
    return render_template('new_continue/teachers.html', user=user, teachers=teachers, form=form)


@app.route('/giving_charity/<id>', methods=['POST'])
def give_charity(id):
    user = get_current_user()
    try:
        if not user.director:
            return redirect(url_for('nav'))
    except AttributeError:
        return redirect(url_for('nav'))
    if request.method == "POST":
        charity = int(request.form.get('charity'))
        Student.query.filter_by(id=id).update({'charity': charity})
        db.session.commit()
        flash('Благотворительность прошла успешно')
        return redirect(url_for('student_info', student_id=id))


@app.route('/giving_charity2/<int:id>', methods=['POST'])
def give_charity2(id):
    user = get_current_user()
    try:
        if not user.director:
            return redirect(url_for('nav'))
    except AttributeError:
        return redirect(url_for('nav'))
    if request.method == "POST":
        charity = request.form.get('charity')
        Student.query.filter_by(id=id).update({'charity': charity})
        db.session.commit()
        return redirect(url_for('student_info', student_id=id))


@app.route('/all_user')
def admin_users():
    form = PhotoForm(meta={'csrf': False})
    user = get_current_user()
    try:
        if not user.director:
            return redirect(url_for('nav'))
    except AttributeError:
        return redirect(url_for('nav'))
    admins = Student.query.filter(or_(Student.xojakent_admin, Student.gazalkent_admin,
                                      Student.chirchiq_admin)).all()
    print(admins)
    return render_template('new_continue/admin user.html', admins=admins, user=user, form=form)


@app.route('/delete_user/<int:delete_id>')
def delete_user(delete_id):
    user = get_current_user()
    try:
        if not user.director:
            return redirect(url_for('nav'))
    except AttributeError:
        return redirect(url_for('nav'))
    delete = Student.query.filter_by(id=delete_id).first()
    delete.delete()
    return redirect(url_for('admin_users'))


@app.route('/make_admin_/<int:admin_id>', methods=['POST'])
def admin(admin_id):
    user = get_current_user()
    try:
        if not user.director:
            return redirect(url_for('nav'))
    except AttributeError:
        return redirect(url_for('nav'))
    location = request.form.get('location')
    if location == "Ходжикент":
        Student.query.filter_by(id=admin_id).update({'xojakent_admin': True})
        db.session.commit()
    if location == "Газалкент":
        Student.query.filter_by(id=admin_id).update({'gazalkent_admin': True})
        db.session.commit()
    if location == "Чирчик":
        Student.query.filter_by(id=admin_id).update({'chirchiq_admin': True})
        db.session.commit()
    flash(f'У вас новый администратор для {location}')
    return redirect(url_for('student_profile2', student_id=admin_id))


@app.route('/kick_admin/<int:admin_id>')
def admin_kick(admin_id):
    user = get_current_user()
    try:
        if not user.director:
            return redirect(url_for('nav'))
    except AttributeError:
        return redirect(url_for('nav'))
    admin_info = Student.query.filter_by(id=admin_id).first()
    if admin_info.xojakent_admin:
        Student.query.filter_by(id=admin_id).update({'xojakent_admin': False})
        db.session.commit()
    if admin_info.gazalkent_admin:
        Student.query.filter_by(id=admin_id).update({'gazalkent_admin': False})
        db.session.commit()
    if admin_info.chirchiq_admin:
        Student.query.filter_by(id=admin_id).update({'chirchiq_admin': False})
        db.session.commit()
    flash('Роль администратора удалена')
    return redirect(url_for('student_profile2', student_id=admin_id))


@app.route('/absent_days/<int:student_id>')
def absent(student_id):
    user = get_current_user()
    try:
        if not user.director:
            return redirect(url_for('nav'))
    except AttributeError:
        return redirect(url_for('nav'))
    attendance = Attendance.query.filter_by(student_id=student_id).all()
    student = Student.query.filter_by(id=student_id).first()
    group = Groups.query.filter(or_(Groups.id == student.group1, Groups.id == student.group2,
                                    Groups.id == student.group3))
    for i in group:
        teacher = i.teacher_1
        return render_template('base template/absent students1.html', teacher=teacher, group=group,
                               attendance=attendance,
                               student=student,
                               id=student_id)
    return render_template('base template/absent students1.html', user=user, attendance=attendance, id=student_id)


@app.route('/delete_days/<int:day_id><int:student_id>')
def delete_days(day_id, student_id):
    user = get_current_user()
    try:
        if not user.director:
            return redirect(url_for('nav'))
    except AttributeError:
        return redirect(url_for('nav'))
    delete = Attendance.query.filter(Attendance.id == day_id).first()
    delete.delete()
    query = Student.query.filter_by(id=student_id).first()
    group = Groups.query.filter(or_(Groups.id == query.group1, Groups.id == query.group2, Groups.id == query.group3))
    for i in group:
        query_teacher = Teachers.query.filter_by(id=i.teacher_1).first()
        slesh = i.cost / 13
        boluv = slesh / 2
        plus = query.money + slesh
        minus = query_teacher.salary - boluv
        Student.query.filter_by(id=student_id).update({'money': plus})
        Teachers.query.filter_by(id=i.teacher_1).update({'salary': minus})
        db.session.commit()
        qosh = query.charity
        total = All_Charity_Sums.bank_charity - qosh
        All_Charity_Sums.query.filter_by(id=1).update({'bank_charity': total})
        db.session.commit()

    return redirect(url_for('home'))


@app.route('/get_id/<check_id>', methods=["POST"])
def get_id(check_id):
    completed = request.get_json()['completed']
    todo_id = Attendance.query.get(check_id)
    todo_id.for_sabab = completed
    db.session.commit()
    return check_id


@app.route('/sababli_qilish')
def sababli_qilish():
    user = get_current_user()
    try:
        if not user.director:
            return redirect(url_for('nav'))
    except AttributeError:
        return redirect(url_for('nav'))
    form = PhotoForm(meta={'csrf': False})
    get_student = ReasonAbsentDays.query.order_by('student_id').all()
    for student in get_student:
        query_students = Student.query.filter_by(id=student.student_id).all()
        print(query_students)
        return render_template('new_continue/Sababli_qilish.html', user=user, query_students=query_students, form=form)
    return render_template('new_continue/Sababli_qilish.html', user=user, form=form)


@app.route('/show_due_days<int:student_id>')
def show_due_days(student_id):
    user = get_current_user()
    try:
        if not user.director:
            return redirect(url_for('nav'))
    except AttributeError:
        return redirect(url_for('nav'))
    attendance = Attendance.query.filter_by(student_id=student_id, for_sabab=True).all()
    reason_days = ReasonAbsentDays.query.filter_by(student_id=student_id).first()
    query = Attendance.query.filter_by(student_id=student_id, for_sabab=True).first()
    return render_template('new_continue/Show_due_days.html', user=user, reason_days=reason_days, query=query,
                           attendance=attendance)


@app.route('/commit/<int:student_id>/<int:id_reason>/<int:teacher_id>/<int:group_id>')
def commit_due(student_id, id_reason, teacher_id, group_id):
    user = get_current_user()
    try:
        if not user.director:
            return redirect(url_for('nav'))
    except AttributeError:
        return redirect(url_for('nav'))
    query = ReasonAbsentDays.query.filter_by(id=id_reason).first()

    add2 = due_days(group_id_student=query.group_id,
                    img_due_days=query.img_due_days, id_of_student=query.student_id,
                    date_of_absent=query.date_abset,
                    reason_due=query.reason_due)
    db.session.add(add2)

    student = Student.query.filter_by(id=student_id).first()
    group = Groups.query.filter_by(id=group_id).first()

    teacher = Teachers.query.filter_by(id=teacher_id).first()
    slesh = group.cost / 13 - student.charity
    for_teacher = slesh / 2
    plus = 0
    salary = 0
    if student.money >= 0:
        plus = student.money - slesh
    else:
        plus = student.money + slesh
    Student.query.filter_by(id=student_id).update({'money': plus})
    #teacher
    if group.location == 1:
        if salary >= 0:
            salary = teacher.salary - for_teacher
        else:
            salary = teacher.salary + for_teacher
        Teachers.query.filter_by(id=group.teacher_1).update({'salary': salary})
        db.session.commit()
    if group.location == 2:
        if salary >= 0:
            salary = teacher.salary - for_teacher
        else:
            salary = teacher.salary + for_teacher
        Teachers.query.filter_by(id=group.teacher_1).update({'salary_for_gazalkent': salary})
        db.session.commit()
    if group.location == 3:
        if salary >= 0:
            salary = teacher.salary - for_teacher
        else:
            salary = teacher.salary + for_teacher
        Teachers.query.filter_by(id=group.teacher_1).update({'salary_for_chirchiq': salary})
        db.session.commit()
    #Student
    if student.locations == 1:
        query_charity = All_Charity_Sums.query.filter_by(id=1).first()
        salary = query_charity.bank_charity - student.charity
        All_Charity_Sums.query.filter_by(id=1).update({'bank_charity': salary})
    elif student.locations == 2:
        query_charity2 = All_Charity_Sums.query.filter_by(id=2).first()
        minus2 = query_charity2.bank_charity - student.charity
        All_Charity_Sums.query.filter_by(id=2).update({'bank_charity': minus2})
    elif student.locations == 3:
        query_charity3 = All_Charity_Sums.query.filter_by(id=3).first()
        minus3 = query_charity3.bank_charity - student.charity
        All_Charity_Sums.query.filter_by(id=3).update({'bank_charity': minus3})
    Attendance.query.filter_by(student_id=student_id, for_sabab=True).delete()
    ReasonAbsentDays.query.filter_by(id=id_reason).delete()
    db.session.commit()
    flash('Операция прошла успешно')
    return redirect(url_for('sababli_qilish'))


@app.route('/refuse/<int:student_id>/<int:group_id>')
def refuse_due(student_id, group_id):
    user = get_current_user()
    try:
        if not user.director:
            return redirect(url_for('nav'))
    except AttributeError:
        return redirect(url_for('nav'))
    Attendance.query.filter_by(student_id=student_id, for_sabab=True, group_id=group_id).update({'for_sabab': False})
    db.session.commit()
    reason = ReasonAbsentDays.query.filter_by(student_id=student_id, group_id=group_id)
    for res in reason:
        db.session.delete(res)
        db.session.commit()
    flash('Операция успешно отменена')
    return redirect(url_for('sababli_qilish'))


@app.route('/users')
def users():
    user = get_current_user()
    form = PhotoForm(meta={'csrf': False})
    try:
        if user.username != "RIMEFARA" and not user.director:
            return redirect(url_for('nav'))
    except AttributeError:
        return redirect(url_for('nav'))
    all_users = Student.query.order_by('id').all()
    return render_template('all_users.html', user=user,all_users=all_users,form=form)


@app.route('/delete_users/<int:id>')
def delete_users(id):
    user = get_current_user()
    form = PhotoForm(meta={'csrf': False})
    try:
        if user.username != "RIMEFARA" and not user.director:
            return redirect(url_for('nav'))
    except AttributeError:
        return redirect(url_for('nav'))
    Student.query.filter_by(id=id).delete()
    db.session.commit()
    flash("User has successfully deleted")
    return redirect(url_for('users'))
