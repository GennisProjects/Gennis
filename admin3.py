from app import request, redirect, url_for, app, get_current_user, render_template, get_current_teacher, db, abort, or_, \
    and_, PhotoForm, flash
from models import Student, Teachers, Groups, Shartnoma
from werkzeug.security import generate_password_hash
from datetime import datetime, date, timedelta


@app.route('/all_students')
def all_students():
    user = get_current_user()
    form = PhotoForm(meta={'csrf': False})
    try:
        if not user.xojakent_admin and not user.gazalkent_admin and not user.chirchiq_admin and not user.director:
            return redirect(url_for('nav'))
    except AttributeError:
        return redirect(url_for('nav'))
    if user.xojakent_admin:
        Student.query.filter_by(locations=1).update({'for_group': False, 'for_moved': False})
        db.session.commit()
    elif user.xojakent_admin:
        Student.query.filter_by(locations=2).update({'for_group': False, 'for_moved': False})
        db.session.commit()
    elif user.chirchiq_admin:
        Student.query.filter_by(locations=3).update({'for_group': False, 'for_moved': False})
        db.session.commit()

    students = Student.query.filter_by(director=False, xojakent_admin=False, gazalkent_admin=False,
                                       chirchiq_admin=False).order_by('id').all()
    teachers = Teachers.query.order_by('id').all()
    groups = Groups.query.order_by('id').all()
    return render_template('Admin templates/xojakent/List students xojakent.html', user=user, students=students, form=form, teachers=teachers,
                           groups=groups)


@app.route('/search_age_all', methods=['POST'])
def search_age_all():
    user = get_current_user()
    try:
        if not user.xojakent_admin and not user.director and not user.gazalkent_admin and not user.director:
            return redirect(url_for('nav'))
    except AttributeError:
        return redirect(url_for('nav'))
    age = int(request.form.get('age'))
    age_student = int(request.form.get('age_student'))
    subject = request.form.get('subject')
    location = int(request.form.get('location'))
    print(subject)
    subject_1 = Student.query.filter(and_(Student.age >= age, Student.age <= age_student, Student.subject_1 == subject,
                                          Student.locations == location)).order_by(Student.id).all()
    subject_2 = Student.query.filter_by(age=age, subject_2=subject, locations=location).order_by(Student.id).all()
    subject_3 = Student.query.filter_by(age=age, subject_3=subject, locations=location).order_by(Student.id).all()

    return render_template('base template/student_by_age.html', user=user, students=subject_1, students2=subject_2,
                           students3=subject_3, search=age, search2=age_student, subject=request.form.get('subject'))


@app.route('/studying_students')
def studying_students():
    user = get_current_user()
    form = PhotoForm(meta={'csrf': False})
    try:
        if not user.xojakent_admin and not user.director and not user.gazalkent_admin and not user \
                and not user.chirchiq_admin:
            return redirect(url_for('nav'))
    except AttributeError:
        return redirect(url_for('nav'))

    students1 = Student.query.filter(Student.locations == 1, Student.xojakent_admin == False,
                                     Student.chirchiq_admin == False, Student.gazalkent_admin == False,
                                     Student.director == False).order_by('id').all()
    students2 = Student.query.filter(Student.locations == 2, Student.xojakent_admin == False,
                                     Student.chirchiq_admin == False, Student.gazalkent_admin == False,
                                     Student.director == False).order_by('id').all()
    students3 = Student.query.filter(Student.locations == 3, Student.xojakent_admin == False,
                                     Student.chirchiq_admin == False, Student.gazalkent_admin == False,
                                     Student.director == False).order_by('id').all()
    group_1_xojakent = []
    group_2_xojakent = []
    group_3_xojakent = []
    for student1 in students1:
        group1_xojakent = Groups.query.filter_by(id=student1.group1).first()
        group2_xojakent = Groups.query.filter_by(id=student1.group2).first()
        group3_xojakent = Groups.query.filter_by(id=student1.group3).first()
        group_1_xojakent.append(group1_xojakent)
        group_2_xojakent.append(group2_xojakent)
        group_3_xojakent.append(group3_xojakent)
    group_1_gazalkent = []
    group_2_gazalkent = []
    group_3_gazalkent = []
    for student2 in students2:
        group1_gazalkent = Groups.query.filter_by(id=student2.group1).first()
        group2_gazalkent = Groups.query.filter_by(id=student2.group2).first()
        group3_gazalkent = Groups.query.filter_by(id=student2.group3).first()
        group_1_gazalkent.append(group1_gazalkent)
        group_2_gazalkent.append(group2_gazalkent)
        group_3_gazalkent.append(group3_gazalkent)
    group_1_chirchiq = []
    group_2_chirchiq = []
    group_3_chirchiq = []
    for student3 in students3:
        group1_chirchiq = Groups.query.filter_by(id=student3.group1).first()
        group2_chirchiq = Groups.query.filter_by(id=student3.group2).first()
        group3_chirchiq = Groups.query.filter_by(id=student3.group3).first()
        group_1_chirchiq.append(group1_chirchiq)
        group_2_chirchiq.append(group2_chirchiq)
        group_3_chirchiq.append(group3_chirchiq)
    return render_template('Admin templates/xojakent/studying students xojakent.html', group_info1=group_1_xojakent, group_info2=group_2_xojakent,
                           group_info3=group_3_xojakent, group_info4=group_1_gazalkent, group_info5=group_2_gazalkent,
                           group_info6=group_3_gazalkent, group_info7=group_1_chirchiq, form=form, user=user,
                           group_info8=group_2_chirchiq, group_info9=group_3_chirchiq, students1=students1,
                           students2=students2, students3=students3)


@app.route('/register_teacher', methods=['POST', 'GET'])
def register_teacher():
    user = get_current_user()
    try:
        if not user.xojakent_admin and not user.chirchiq_admin and not user.gazalkent_admin and not user.director:
            return redirect(url_for('nav'))
    except AttributeError:
        return redirect(url_for('nav'))
    teacher = get_current_teacher()
    all_usernames = Student.query.order_by('id').all()
    all_usernames2 = Teachers.query.order_by('id').all()
    if request.method == 'POST':
        teacher_name = request.form.get('name').upper()
        teacher_surname = request.form.get('surname').upper()
        teacher_location = request.form.get('location2')
        teacher_username = request.form.get('username').upper()
        confirm_password = request.form.get('con_password')
        teacher_phone = request.form.get('phone')
        otasining_ismi = request.form.get('father_name')
        birth_day = int(request.form.get('birth_day'))
        birth_month = int(request.form.get('birth_month'))
        birth_year = int(request.form.get('birth_year'))
        teacher_subject = request.form.get('subject_1')
        a = datetime.today().year
        age = a - birth_year
        hash = generate_password_hash(confirm_password, method='sha256')
        if teacher_location == "xojakent":
            teacher_location = 1
        elif teacher_location == "gazalkent":
            teacher_location = 2
        elif teacher_location == "chirchiq":
            teacher_location = 3

        # print(teacher_username)
        # print(teacher_name)
        # print(teacher_surname)
        # print(teacher_phone)
        # print(teacher_subject)
        # print(teacher_location)
        # print(birth_year)
        # print(birth_month)
        # print(birth_day)
        # print(otasining_ismi)
        add = Teachers(name=teacher_name,
                       surname=teacher_surname,
                       age=age,
                       locations=teacher_location,
                       username=teacher_username,
                       password=hash,
                       subject=teacher_subject,
                       phone=teacher_phone,
                       teacher=True,
                       otasining_ismi=otasining_ismi,
                       salary=0,
                       salary_for_gazalkent=0,
                       salary_for_chirchiq=0,
                       day_born=birth_day,
                       month_born=birth_month,
                       year_born=birth_year
                       )
        add.add_teacher()
        flash("Вы успешно зарегистрировали учителя")
        return redirect(url_for('new_home'))
    return render_template('new/register_teacher.html', user=user, teacher=teacher, usernames=all_usernames,
                           usernames2=all_usernames2)


@app.route('/groups')
def dir_groups():
    form = PhotoForm(meta={'csrf': False})
    user = get_current_user()
    try:
        if not user.xojakent_admin and not user.director and not user.gazalkent_admin and not user.chirchiq_admin:
            return redirect(url_for('nav'))
    except AttributeError:
        return redirect(url_for('nav'))
    groups_xoj = Groups.query.filter_by(location=1).order_by('id').all()
    groups_without_teacher = Groups.query.filter_by(location=1, teacher_1=0).all()
    groups_gaz = Groups.query.filter_by(location=2).order_by('id').all()
    groups_without_teacher2 = Groups.query.filter_by(location=2, teacher_1=0).all()
    groups_chir = Groups.query.filter_by(location=3).order_by('id').all()
    groups_without_teacher3 = Groups.query.filter_by(location=3, teacher_1=0).all()
    return render_template('new/groups.html', user=user, groups_gaz=groups_gaz, groups_xoj=groups_xoj,
                           groups_without_teacher2=groups_without_teacher2, groups_chir=groups_chir, form=form,
                           groups_without_teacher=groups_without_teacher,
                           groups_without_teacher3=groups_without_teacher3)


@app.route('/group_name', methods=['POST'])
def group_search_name():
    user = get_current_user()
    try:
        if not user.xojakent_admin and not user.director and not user.gazalkent_admin and not user.director:
            return redirect(url_for('nav'))
    except AttributeError:
        return redirect(url_for('nav'))
    group_name = Groups.query.filter(Groups.name.ilike("%" + request.form.get('group_name').upper() + "%"),
                                     Groups.location == 1)
    find_name = list(map(Groups.info, group_name))
    result_name = {
        "data": find_name,
        "count": len(find_name)
    }
    return render_template('new_continue/search_by_name_xoj.html', user=user, result_name=result_name,
                           search=request.form.get('group_name').upper())


@app.route('/group_search_teacher', methods=['POST'])
def group_search_teacher():
    user = get_current_user()
    try:
        if not user.xojakent_admin and not user.director and not user.gazalkent_admin and not user.director:
            return redirect(url_for('nav'))
    except AttributeError:
        return redirect(url_for('nav'))
    teacher_name = Groups.query.filter(Groups.teacher_name.ilike("%" + request.form.get('group_teacher').upper() + "%"),
                                       Groups.location == 1)
    find_name = list(map(Groups.info, teacher_name))
    result_name = {
        "data": find_name,
        "count": len(find_name)
    }
    return render_template('new_continue/teacher_search_xoj.html', user=user, result_name=result_name,
                           search=request.form.get('group_teacher').upper())


@app.route('/group_search_subject', methods=['POST'])
def group_search_subject():
    user = get_current_user()
    try:
        if not user.xojakent_admin and not user.director and not user.gazalkent_admin and not user.director:
            return redirect(url_for('nav'))
    except AttributeError:
        return redirect(url_for('nav'))
    subject_name = Groups.query.filter(Groups.subject.ilike("%" + request.form.get('group_subject') + "%"),
                                       Groups.location == 1)
    find_name = list(map(Groups.info, subject_name))
    result_name = {
        "data": find_name,
        "count": len(find_name)
    }
    return render_template('new_continue/subject_xoj.html', user=user, result_name=result_name,
                           search=request.form.get('group_subject'))


@app.route('/group_name2', methods=['POST'])
def group_search_name2():
    user = get_current_user()
    try:
        if not user.xojakent_admin and not user.director and not user.gazalkent_admin and not user.director:
            return redirect(url_for('nav'))
    except AttributeError:
        return redirect(url_for('nav'))
    teacher_name = Groups.query.filter(Groups.name.ilike("%" + request.form.get('group_name').upper() + "%"),
                                       Groups.location == 2)
    find_name = list(map(Groups.info, teacher_name))
    result_name = {
        "data": find_name,
        "count": len(find_name)
    }
    return render_template('new_continue/seach_by_name_gaz.html', user=user, result_name=result_name,
                           search=request.form.get('group_name').upper())


@app.route('/group_search_teacher2', methods=['POST'])
def group_search_teacher2():
    user = get_current_user()
    try:
        if not user.xojakent_admin and not user.director and not user.gazalkent_admin and not user.director:
            return redirect(url_for('nav'))
    except AttributeError:
        return redirect(url_for('nav'))
    teacher_name = Groups.query.filter(Groups.teacher_name.ilike("%" + request.form.get('group_teacher').upper() + "%"),
                                       Groups.location == 2)
    find_name = list(map(Groups.info, teacher_name))
    result_name = {
        "data": find_name,
        "count": len(find_name)
    }
    return render_template('new_continue/teacher_search_gaz.html', user=user, result_name=result_name,
                           search=request.form.get('group_teacher').upper())


@app.route('/group_search_by_subject2', methods=['POST'])
def group_search_by_subject2():
    user = get_current_user()
    try:
        if not user.xojakent_admin and not user.director and not user.gazalkent_admin and not user.director:
            return redirect(url_for('nav'))
    except AttributeError:
        return redirect(url_for('nav'))
    teacher_name = Groups.query.filter(Groups.subject.ilike("%" + request.form.get('group_subject') + "%"),
                                       Groups.location == 2)
    find_name = list(map(Groups.info, teacher_name))
    result_name = {
        "data": find_name,
        "count": len(find_name)
    }
    return render_template('new_continue/subject_gaz.html', user=user, result_name=result_name,
                           search=request.form.get('group_subject'))


@app.route('/group_search_name3', methods=['POST'])
def group_search_name3():
    user = get_current_user()
    try:
        if not user.xojakent_admin and not user.chirchiq_admin and not user.gazalkent_admin and not user.director:
            return redirect(url_for('nav'))
    except AttributeError:
        return redirect(url_for('nav'))
    teacher_name = Groups.query.filter(Groups.name.ilike("%" + request.form.get('group_name').upper() + "%"),
                                       Groups.location == 3)
    find_name = list(map(Groups.info, teacher_name))
    result_name = {
        "data": find_name,
        "count": len(find_name)
    }
    return render_template('new_continue/search_by_name_chir.html', user=user, result_name=result_name,
                           search=request.form.get('group_name').upper())


@app.route('/group_name_teacher3', methods=['POST'])
def group_search_teacher3():
    user = get_current_user()
    try:
        if not user.xojakent_admin and not user.director and not user.gazalkent_admin and not user.director:
            return redirect(url_for('nav'))
    except AttributeError:
        return redirect(url_for('nav'))
    teacher_name = Groups.query.filter(Groups.teacher_name.ilike("%" + request.form.get('group_teacher').upper() + "%"),
                                       Groups.location == 3)
    find_name = list(map(Groups.info, teacher_name))
    result_name = {
        "data": find_name,
        "count": len(find_name)
    }
    return render_template('new_continue/teacher_search_chir.html', user=user, result_name=result_name,
                           search=request.form.get('group_teacher').upper())


@app.route('/group_search_subject3', methods=['POST'])
def group_search_subject3():
    user = get_current_user()
    try:
        if not user.xojakent_admin and not user.chirchiq_admin and not user.gazalkent_admin and not user.director:
            return redirect(url_for('nav'))
    except AttributeError:
        return redirect(url_for('nav'))
    teacher_name = Groups.query.filter(Groups.subject.ilike("%" + request.form.get('group_subject') + "%"),
                                       Groups.location == 3)
    find_name = list(map(Groups.info, teacher_name))
    result_name = {
        "data": find_name,
        "count": len(find_name)
    }
    return render_template('new_continue/subject_chir.html', user=user, result_name=result_name,
                           search=request.form.get('group_subject'))


@app.route('/prepare_add_group', methods=['POST'])
def prepare_add_group():
    user = get_current_user()
    try:
        if not user.xojakent_admin and not user.chirchiq_admin and not user.gazalkent_admin:
            return redirect(url_for('nav'))
    except AttributeError:
        return redirect(url_for('nav'))
    group_id = request.form.get('group_id')
    return redirect(url_for('add_group', group_id=group_id))


@app.route('/join_group/<int:group_id>', methods=['POST', 'GET'])
def add_group(group_id):
    user = get_current_user()
    try:
        if not user.xojakent_admin and not user.chirchiq_admin and not user.gazalkent_admin:
            return redirect(url_for('nav'))
    except AttributeError:
        return redirect(url_for('nav'))
    if request.method == 'POST':

        students = Student.query.filter_by(for_group=True, locations=user.locations).all()
        group = Groups.query.filter_by(id=group_id).first()
        for student in students:
            if student.group1 == None and student.group2 == None and student.group3 == None:
                if group.subject == student.subject_1:
                    Student.query.filter(Student.id == student.id, Student.for_group == True, Student.group1 == None,
                                         Student.group2 == None,
                                         Student.group3 == None).update(
                        {'group1': group.id, 'for_group': False, 'subject_1': None})
                    db.session.commit()
                    db.session.rollback()
                if group.subject == student.subject_2:
                    Student.query.filter(Student.id == student.id, Student.for_group == True, Student.group1 == None,
                                         Student.group2 == None,
                                         Student.group3 == None).update(
                        {'group1': group.id, 'for_group': False, 'subject_2': None})
                    db.session.commit()
                    db.session.rollback()
                if group.subject == student.subject_3:
                    Student.query.filter(Student.id == student.id, Student.for_group == True, Student.group1 == None,
                                         Student.group2 == None,
                                         Student.group3 == None).update(
                        {'group1': group.id, 'for_group': False, 'subject_3': None})
                    db.session.commit()
                    db.session.rollback()
            if student.group1 != None and student.group2 == None and student.group3 == None:
                if group.subject == student.subject_1:
                    Student.query.filter(Student.id == student.id, Student.for_group == True, Student.group1 != None,
                                         Student.group2 == None,
                                         Student.group3 == None).update(
                        {'group2': group.id, 'for_group': False, 'subject_1': None})
                    db.session.commit()
                    db.session.rollback()
                if group.subject == student.subject_2:
                    Student.query.filter(Student.id == student.id, Student.for_group == True, Student.group1 != None,
                                         Student.group2 == None,
                                         Student.group3 == None).update(
                        {'group2': group.id, 'for_group': False, 'subject_2': None})
                    db.session.commit()
                    db.session.rollback()
                if group.subject == student.subject_3:
                    Student.query.filter(Student.id == student.id, Student.for_group == True, Student.group1 != None,
                                         Student.group2 == None,
                                         Student.group3 == None).update(
                        {'group2': group.id, 'for_group': False, 'subject_3': None})
                    db.session.commit()
                    db.session.rollback()
            elif student.group1 != None and student.group2 != None and student.group3 == None:
                if group.subject == student.subject_1:
                    Student.query.filter(Student.id == student.id, Student.for_group == True, Student.group1 != None,
                                         Student.group2 != None,
                                         Student.group3 == None).update(
                        {'group3': group.id, 'for_group': False, 'subject_1': None})
                    db.session.commit()
                    db.session.rollback()
                if group.subject == student.subject_2:
                    Student.query.filter(Student.id == student.id, Student.for_group == True, Student.group1 != None,
                                         Student.group2 != None,
                                         Student.group3 == None).update(
                        {'group3': group.id, 'for_group': False, 'subject_2': None})
                    db.session.commit()
                    db.session.rollback()
                if group.subject == student.subject_3:
                    Student.query.filter(Student.id == student.id, Student.for_group == True, Student.group1 != None,
                                         Student.group2 != None,
                                         Student.group3 == None).update(
                        {'group3': group.id, 'for_group': False, 'subject_3': None})
                    db.session.commit()
                    db.session.rollback()
        flash('Студент успешно добавлен')
        return redirect(url_for('new_home'))
    group = Groups.query.filter_by(id=group_id).first()
    students = Student.query.filter(or_(Student.subject_1 == group.subject, Student.subject_2 == group.subject,
                                        Student.subject_3 == group.subject)).all()
    student = Student.query.filter(or_(Student.subject_1 == group.subject, Student.subject_2 == group.subject,
                                       Student.subject_3 == group.subject)).first()
    return render_template('new/add_group.html', user=user, students=students, group_id=group_id, group=group,
                           student=student)


@app.route('/teachers2/<int:id>/<int:group_id>')
def teacher2(id, group_id):
    user = get_current_user()
    try:
        if not user:
            return redirect(url_for('nav'))
    except AttributeError:
        return redirect(url_for('nav'))
    teacher = Teachers.query.filter_by(id=id)
    return render_template('base template/teachers2.html', user=user, teacher=teacher, id=id, group_id=group_id)


@app.route('/student_profile2/<int:student_id>')
def student_profile2(student_id):
    form = PhotoForm(meta={'csrf': False})
    user = get_current_user()
    teacher = get_current_teacher()
    try:
        if not user.xojakent_admin and not user.director and not user.gazalkent_admin and not user.chirchiq_admin:
            return redirect(url_for('nav'))
    except AttributeError:
        return redirect(url_for('nav'))

    student = Student.query.filter_by(id=student_id).first()
    return render_template('new_continue/student_profile2.html', user=user, student=student, form=form, student_id=student_id,
                           teacher=teacher)
