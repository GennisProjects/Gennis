from app import app,get_current_user,get_current_teacher,or_,redirect,render_template,request,url_for,db, PhotoForm,\
    images, flash, generate_password_hash
from models import Student,Groups, Teachers, Deleted_students, Shartnoma
from datetime import datetime, date, timedelta


@app.route('/manage/<int:id>', methods=['POST', 'GET'])
def manage(id):
    user = get_current_user()
    try:
        if not user.gazalkent_admin and not user.director and not user.xojakent_admin:
            return redirect(url_for('nav'))
    except AttributeError:
        return redirect(url_for('nav'))
    teacher = get_current_teacher()
    groups = Groups.query.filter_by(id=id).all()
    experts = Teachers.query.filter_by(teacher=True).all()
    for group in groups:
        student = Student.query.filter(or_(Student.group1 == group.id,Student.group2 == group.id,Student.group3==group.id))
        if user.xojakent_admin or user.director:
            return render_template('Groups/manage_group.html', students=student, groups=groups, user=user,
                                   teachers=experts, gr_id=id)
        elif user.gazalkent_admin or user.director:
            return render_template('Groups/manage_group.html', students=student, groups=groups, user=user,
                                   teachers=experts, gr_id=id)
    return render_template('Groups/manage_group.html', groups=groups, user=user, teachers=experts, gr_id=id)


@app.route('/show_group/<int:group_id>', methods=['POST', 'GET'])
def show_group(group_id):
    user = get_current_user()
    try:
        if not user.gazalkent_admin and not user.director and not user.xojakent_admin:
            return redirect(url_for('nav'))
    except AttributeError:
        return redirect(url_for('nav'))
    gr_id = Groups.query.filter_by(id=group_id).first()
    query_groups = Groups.query.filter_by(location=gr_id.location).all()
    query_students = Student.query.filter_by(for_moved=True).first()
    return render_template('new/Show_group.html', groups=query_groups, old_id=group_id, students=query_students,
                           user=user)


@app.route('/check_moved/<check_id>', methods=["POST"])
def check_moved(check_id):
    completed = request.get_json()['completed']
    todo_id = Student.query.get(check_id)
    todo_id.for_moved = completed
    db.session.commit()
    return redirect(url_for('manage'))


@app.route('/move_to_group/<int:old_id>/<int:group_id>')
def move_to_group(old_id,group_id):
    user = get_current_user()
    try:
        if not user.gazalkent_admin and not user.director and not user.xojakent_admin:
            return redirect(url_for('nav'))
    except AttributeError:
        return redirect(url_for('nav'))
    query = Student.query.filter_by(for_moved=True).first()
    query_group = Groups.query.filter_by(id=group_id).all()
    old_group = Groups.query.filter_by(id=old_id).first()
    for i in query_group:
        if query.group1 == old_group.id:
            Student.query.filter_by(for_moved=True).update({'group1': i.id, 'for_moved': False})
            db.session.commit()

        elif query.group2 == old_group.id:
            if query.group1 == i.id:
                return 'Bu gruppa band'
            else:
                Student.query.filter_by(for_moved=True).update({'group2': i.id, 'for_moved': False})
                db.session.commit()

        elif query.group3 == old_group.id:
            if query.group1 == i.id:
                return 'Bu gruppa band'
            elif query.group2 == i.id:
                return 'Bu gruppa band'
            else:
                Student.query.filter_by(for_moved=True).update({'group3': i.id, 'for_moved': False})
                db.session.commit()
    flash('Студент успешно переехал')
    return redirect(url_for('inside_of_group', id=old_id))


@app.route('/rename_group<int:id>', methods=["POST"])
def rename_group(id):
    user = get_current_user()
    try:
        if not user.gazalkent_admin and not user.director and not user.xojakent_admin:
            return redirect(url_for('nav'))
    except AttributeError:
        return redirect(url_for('nav'))
    name = request.form.get('name').upper()
    Groups.query.filter_by(id=id).update({'name': name})
    db.session.commit()
    flash('Название группы успешно изменено')
    return redirect(url_for('inside_of_group', id=id))


@app.route('/deleted_students<int:id>',methods=["POST","GET"])
def deleted_students(id):
    user = get_current_user()
    try:
        if not user.gazalkent_admin and not user.director and not user.xojakent_admin:
            return redirect(url_for('nav'))
    except AttributeError:
        return redirect(url_for('nav'))
    reason = request.form.get('reason')
    query_student = Student.query.filter_by(id=id).first()
    add = Deleted_students(reason=reason,student_name=query_student.name,
                           student_id=query_student.id,student_phone=query_student.phone,
                           student_surname=query_student.surname)
    db.session.add(add)
    db.session.commit()
    query_student.delete()
    flash('Студент успешно удален')
    return redirect(url_for('new_home'))


@app.route('/change_info_student/<int:student_id>',methods=["POST"])
def change_student_info(student_id):
    user = get_current_user()
    try:
        if not user.xojakent_admin and not user.director and not user.gazalkent_admin and not user.chirchiq_admin:
            return redirect(url_for('new_home'))
    except AttributeError:
        return redirect(url_for('new_home'))
    name = request.form.get('name').upper()
    surname = request.form.get('surname').upper()
    phone = request.form.get('phone')
    parent_phone = request.form.get('parent_phone')
    subject_1 = request.form.get('subject_1')
    subject_2 = request.form.get('subject_2')
    subject_3 = request.form.get('subject_3')
    if subject_1 == "Birinchi Fan":
        subject_1 = None
    if subject_2 == "Ikkinchi Fan":
        subject_2 = None
    if subject_3 == 'Uchinchi Fan':
        subject_3 = None
    Student.query.filter_by(id=student_id).update({'name': name, "surname": surname, "phone": phone,
                                                   "parent_phone": parent_phone,'subject_1':subject_1,
                                                   'subject_2':subject_2,'subject_3':subject_3})
    db.session.commit()
    flash('Данные успешно изменены')
    return redirect(url_for('student_info',student_id=student_id))


@app.route('/change_info_student2/<int:student_id>',methods=["POST"])
def change_student_info2(student_id):
    user = get_current_user()
    try:
        if not user.xojakent_admin and not user.director and not user.gazalkent_admin and not user.chirchiq_admin:
            return redirect(url_for('new_home'))
    except AttributeError:
        return redirect(url_for('new_home'))
    name = request.form.get('name').upper()
    surname = request.form.get('surname').upper()
    phone = request.form.get('phone')
    parent_phone = request.form.get('parent_phone')
    subject_1 = request.form.get('subject_1')
    subject_2 = request.form.get('subject_2')
    subject_3 = request.form.get('subject_3')
    if subject_1 == "Birinchi Fan":
        subject_1 = None
    if subject_2 == "Ikkinchi Fan":
        subject_2 = None
    if subject_3 == 'Uchinchi Fan':
        subject_3 = None
    Student.query.filter_by(id=student_id).update({'name': name, "surname": surname, "phone": phone,
                                                   "parent_phone": parent_phone,'subject_1':subject_1,
                                                   'subject_2':subject_2,'subject_3':subject_3})
    db.session.commit()
    flash('Данные успешно изменены')
    return redirect(url_for('student_profile2',student_id=student_id))


@app.route('/change_password_student/<int:student_id>',methods=['POST'])
def change_password_student(student_id):
    user = get_current_user()
    try:
        if not user.xojakent_admin and not user.director and not user.gazalkent_admin and not user.chirchiq_admin:
            return redirect(url_for('new_home'))
    except AttributeError:
        return redirect(url_for('new_home'))
    password = request.form.get('password')
    hash = generate_password_hash(password, method='sha256')
    Student.query.filter_by(id=student_id).update({"password":hash})
    db.session.commit()
    flash('Пароль успешно изменен')
    return redirect(url_for('student_info',student_id=student_id))


@app.route('/shartnoma/<int:student_id>')
def shartnoma(student_id):
    user = get_current_user()
    try:
        if not user.xojakent_admin and not user.director and not user.gazalkent_admin and not user.chirchiq_admin:
            return redirect(url_for('new_home'))
    except AttributeError:
        return redirect(url_for('new_home'))
    user = get_current_user()
    year = datetime.today().year
    student = Student.query.filter_by(id=student_id).first()
    group1 = Groups.query.filter_by(id=student.group1).first()
    group2 = Groups.query.filter_by(id=student.group2).first()
    group3 = Groups.query.filter_by(id=student.group3).first()
    info_contract = Shartnoma.query.filter_by(student_id=student_id).all()
    list_info = list(map(Shartnoma.info, info_contract))
    info = {
        "data": list_info
    }
    if group1 and not group2 and not group3:
        sum1 = group1.cost
        return render_template('new_continue/Shartnoma.html', user=user, info=info, student=student,
                               group1=group1, sum1=sum1, student_id=student_id, year=year)
    elif group1 and group2 and not group3:
        sum2 = group1.cost + group2.cost
        return render_template('new_continue/Shartnoma.html', user=user, info=info, student=student,
                               group1=group1, group2=group2, sum2=sum2, student_id=student_id, year=year)
    elif group1 and group2 and group3:

        sum3 = group1.cost + group2.cost + group3.cost
        return render_template('new_continue/Shartnoma.html', user=user, info=info, student=student,
                               group1=group1, group2=group2, group3=group3, student_id=student_id, year=year,
                               sum3=sum3)


@app.route('/shartoma_fill1/<int:student_id>',methods=['POST'])
def shartnoma_fill1(student_id):
    user = get_current_user()
    try:
        if not user.xojakent_admin and not user.director and not user.gazalkent_admin and not user.chirchiq_admin:
            return redirect(url_for('new_home'))
    except AttributeError:
        return redirect(url_for('new_home'))
    ot = request.form.get('ot')
    do = request.form.get('do')
    converted_ot = datetime.strptime(ot, "%Y-%m-%d")
    converted_do = datetime.strptime(do, "%Y-%m-%d")
    converted1 = datetime.strftime(converted_ot,"%Y-%m-%d")
    converted2 = datetime.strftime(converted_do, "%Y-%m-%d")
    student = Shartnoma.query.filter_by(student_id=student_id).first()
    if student:
        Shartnoma.query.filter_by(student_id=student_id).update({
            'ot': converted1,
            'do': converted2
        })
        db.session.commit()
    else:
        shartnoma_new = Shartnoma(ot=converted1,do=converted2,student_id=student_id)
        shartnoma_new.insert()
    return redirect(url_for('shartnoma',student_id=student_id))


@app.route('/upload_contract/<int:student_id>',methods=['POST'])
def upload_contract(student_id):
    user = get_current_user()
    try:
        if not user.xojakent_admin and not user.director and not user.gazalkent_admin and not user.chirchiq_admin:
            return redirect(url_for('new_home'))
    except AttributeError:
        return redirect(url_for('new_home'))
    form = PhotoForm(meta={'csrf': False})
    if form.validate_on_submit():
        filename = images.save(form.image.data)
        image_url = images.url(filename)
        Student.query.filter_by(id=student_id).update({'contract_image': image_url})
        db.session.commit()
        print(image_url)
        flash('Фотография успешно загружена')
        return redirect(url_for('student_info',student_id=student_id))


@app.route('/teacher_profile/<int:id>')
def teacher_profile(id):
    user = get_current_user()
    try:
        if not user.xojakent_admin and not user.director and not user.gazalkent_admin and not user.chirchiq_admin:
            return redirect(url_for('nav'))
    except AttributeError:
        return redirect(url_for('nav'))
    teacher = Teachers.query.filter_by(id=id).first()
    group1 = Groups.query.filter_by(id=teacher.group1).first()
    group2 = Groups.query.filter_by(id=teacher.group2).first()
    group3 = Groups.query.filter_by(id=teacher.group3).first()
    group4 = Groups.query.filter_by(id=teacher.group4).first()
    group5 = Groups.query.filter_by(id=teacher.group5).first()
    group6 = Groups.query.filter_by(id=teacher.group6).first()
    group7 = Groups.query.filter_by(id=teacher.group7).first()
    group8 = Groups.query.filter_by(id=teacher.group8).first()
    group9 = Groups.query.filter_by(id=teacher.group9).first()
    group10 = Groups.query.filter_by(id=teacher.group10).first()

    return render_template('new_continue/teacher_information.html', user=user, teacher=teacher, group1=group1,
                           group2=group2,group3=group3,group4=group4,group5=group5,group6=group6,group7=group7,
                           group8=group8,group9=group9,group10=group10)


@app.route('/change_info_teacher/<int:teacher_id>',methods=["POST"])
def change_info_teacher(teacher_id):
    user = get_current_user()
    try:
        if not user.xojakent_admin and not user.director and not user.gazalkent_admin and not user.chirchiq_admin:
            return redirect(url_for('new_home'))
    except AttributeError:
        return redirect(url_for('new_home'))
    name = request.form.get('name').upper()
    surname = request.form.get('surname').upper()
    phone = request.form.get('phone')

    Teachers.query.filter_by(id=teacher_id).update({'name': name, "surname": surname, "phone": phone})
    db.session.commit()
    flash('Данные успешно изменены')
    return redirect(url_for('teacher_profile', id=teacher_id))


@app.route('/change_password_teacher/<teacher_id>', methods=['POST'])
def change_password_teacher(teacher_id):
    user = get_current_user()
    try:
        if not user.xojakent_admin and not user.director and not user.gazalkent_admin and not user.chirchiq_admin:
            return redirect(url_for('new_home'))
    except AttributeError:
        return redirect(url_for('new_home'))
    password = request.form.get('password')
    hash = generate_password_hash(password, method='sha256')
    Teachers.query.filter_by(id=teacher_id).update({"password":hash})
    db.session.commit()
    flash('Пароль успешно изменен')
    return redirect(url_for('teacher_profile', id=teacher_id))

