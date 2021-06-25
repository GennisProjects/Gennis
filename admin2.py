from app import app, get_current_user, or_, db, url_for, redirect, render_template, request, flash
from models import Student, Groups, Teachers


@app.route('/delete_teacher1/<int:id><int:gr>')
def delete_teacher1(id, gr):
    user = get_current_user()
    try:
        if not user.xojakent_admin and not user.director and not user.gazalkent_admin and not user.chirchiq_admin:
            return redirect(url_for('nav'))
    except AttributeError:
        return redirect(url_for('nav'))
    teacher = Teachers.query.filter_by(id=gr).all()
    if teacher.group1 == id:
        Teachers.query.filter_by(id=gr, group1=id).update({'group1': teacher.group2,
                                                           'group2': teacher.group3,
                                                           'group3': teacher.group4,
                                                           'group4': teacher.group5,
                                                           'group5': teacher.group6,
                                                           'group6': teacher.group7,
                                                           'group7': teacher.group8,
                                                           'group8': teacher.group9,
                                                           'group9': teacher.group10,
                                                           'group10': None})
        db.session.commit()
    elif teacher.group2 == id:
        Teachers.query.filter_by(id=gr, group2=id).update({'group2': teacher.group3,
                                                           'group3': teacher.group4,
                                                           'group4': teacher.group5,
                                                           'group5': teacher.group6,
                                                           'group6': teacher.group7,
                                                           'group7': teacher.group8,
                                                           'group8': teacher.group9,
                                                           'group9': teacher.group10,
                                                           'group10': None
                                                           })
        db.session.commit()
    elif teacher.group3 == id:
        Teachers.query.filter_by(id=gr, group3=id).update({'group3': teacher.group4,
                                                           'group4': teacher.group5,
                                                           'group5': teacher.group6,
                                                           'group6': teacher.group7,
                                                           'group7': teacher.group8,
                                                           'group8': teacher.group9,
                                                           'group9': teacher.group10,
                                                           'group10': None
                                                           })
        db.session.commit()
    elif teacher.group4 == id:
        Teachers.query.filter_by(id=gr, group4=id).update({'group4': teacher.group5,
                                                           'group5': teacher.group6,
                                                           'group6': teacher.group7,
                                                           'group7': teacher.group8,
                                                           'group8': teacher.group9,
                                                           'group9': teacher.group10,
                                                           'group10': None
                                                           })
        db.session.commit()
    elif teacher.group5 == id:
        Teachers.query.filter_by(id=gr, group5=id).update({'group5': teacher.group6,
                                                           'group6': teacher.group7,
                                                           'group7': teacher.group8,
                                                           'group8': teacher.group9,
                                                           'group9': teacher.group10,
                                                           'group10': None
                                                           })
        db.session.commit()


    elif teacher.group6 == id:
        Teachers.query.filter_by(id=gr, group6=id).update({'group6': teacher.group7,
                                                           'group7': teacher.group8,
                                                           'group8': teacher.group9,
                                                           'group9': teacher.group10,
                                                           'group10': None
                                                           })
        db.session.commit()
    elif teacher.group7 == id:
        Teachers.query.filter_by(id=gr, group7=id).update({'group7': teacher.group8,
                                                           'group8': teacher.group9,
                                                           'group9': teacher.group10,
                                                           'group10': None
                                                           })
        db.session.commit()
    elif teacher.group8 == id:
        Teachers.query.filter_by(id=gr, group8=id).update({'group8': teacher.group9,
                                                           'group9': teacher.group10,
                                                           'group10': None
                                                           })
        db.session.commit()
    elif teacher.group9 == id:
        Teachers.query.filter_by(id=gr, group9=id).update({'group9': teacher.group10,
                                                           'group10': None
                                                           })
        db.session.commit()
    elif teacher.group10 == id:
        Teachers.query.filter_by(id=gr, group10=id).update({'group10': None
                                                            })
        db.session.commit()

    Groups.query.filter_by(teacher_1=gr, id=id).update({'teacher_1': 0, 'teacher_name': '', 'teacher_surname': ''})
    db.session.commit()
    flash('Учитель успешно удален из группы')
    return redirect(url_for('inside_of_group', id=id))


@app.route('/delete_student_q/<int:id>/<int:gr_id>', methods=['GET'])
def delete_student(id, gr_id):
    user = get_current_user()
    try:
        if not user.xojakent_admin and not user.director and not user.gazalkent_admin and not user.chirchiq_admin:
            return redirect(url_for('nav'))
    except AttributeError:
        return redirect(url_for('nav'))
    students = Student.query.filter(or_(Student.group1 == gr_id, Student.group2 == gr_id, Student.group3 == gr_id)).all()
    group = Groups.query.filter_by(id=gr_id).first()
    for student in students:
        if student.group1 == gr_id:
            if student.subject_1 == None:
                Student.query.filter_by(group1=gr_id, id=id).update({'group1': student.group2,
                                                                     'group2': student.group3,
                                                                     'group3': None,
                                                                     'subject_1': group.subject})
                db.session.commit()
            if student.subject_2 == None:
                Student.query.filter_by(group1=gr_id, id=id).update({'group1': student.group2,
                                                                     'group2': student.group3,
                                                                     'group3': None,
                                                                     'subject_2': group.subject})
                db.session.commit()
            if student.subject_3 == None:
                Student.query.filter_by(group1=gr_id, id=id).update({'group1': student.group2,
                                                                     'group2': student.group3,
                                                                     'group3': None,
                                                                     'subject_3': group.subject})
                db.session.commit()

        if student.group2 == gr_id:
            if student.subject_1 == None:
                Student.query.filter_by(group2=gr_id, id=id).update({'group2': student.group3,
                                                                     'group3': None,
                                                                     'subject_1': group.subject})
                db.session.commit()
            if student.subject_2 == None:
                Student.query.filter_by(group2=gr_id, id=id).update({'group2': student.group3,
                                                                     'group3': None,
                                                                     'subject_2': group.subject})
                db.session.commit()
            if student.subject_3 == None:
                Student.query.filter_by(group2=gr_id, id=id).update({'group2': student.group3,
                                                                     'group3': None,
                                                                     'subject_3': group.subject})
                db.session.commit()
        if student.group3 == gr_id:
            if student.subject_1 == None:
                Student.query.filter_by(group3=gr_id, id=id).update({'group3': None,
                                                                     'subject_1': group.subject})
                db.session.commit()
            if student.subject_2 == None:
                Student.query.filter_by(group3=gr_id, id=id).update({'group3': None,
                                                                     'subject_2': group.subject})
                db.session.commit()
            if student.subject_3 == None:
                Student.query.filter_by(group3=gr_id, id=id).update({'group3': None,
                                                                     'subject_3': group.subject})
                db.session.commit()
    flash('Студент успешно удален из группы')
    return redirect(url_for('inside_of_group', id=gr_id))


@app.route('/prepare_to_create', methods=['POST'])
def prepare_to_create():
    user = get_current_user()
    try:
        if not user.xojakent_admin and not user.gazalkent_admin and not user.chirchiq_admin:
            return redirect(url_for('nav'))
    except AttributeError:
        return redirect(url_for('nav'))
    group_name = request.form.get('group_name').upper()
    pick_teacher = int(request.form.get('pick_teacher'))
    type_of_course = request.form.get('type_of_course')
    price = int(request.form.get('price'))
    teacher = Teachers.query.filter_by(id=pick_teacher).first()
    return redirect(url_for('create_group', pick_teacher=pick_teacher, group_name=group_name,
                            type_of_course=type_of_course, price=price))


@app.route('/create_group/<int:pick_teacher>/<group_name>/<type_of_course>/<int:price>', methods=['POST', 'GET'])
def create_group(pick_teacher, group_name, type_of_course, price):
    user = get_current_user()
    try:
        if not user.xojakent_admin and not user.gazalkent_admin and not user.chirchiq_admin:
            return redirect(url_for('nav'))
    except AttributeError:
        return redirect(url_for('nav'))
    if request.method == 'POST':
        teacher = Teachers.query.filter_by(id=pick_teacher).first()

        add = Groups(name=group_name, teacher_1=teacher.id, location=user.locations, subject=teacher.subject,
                     cost=price,
                     teacher_name=teacher.name, teacher_surname=teacher.surname,
                     type_of_course=type_of_course)
        db.session.add(add)
        db.session.commit()
        group = Groups.query.filter_by(name=group_name).first()
        query_teacher = Teachers.query.filter_by(id=pick_teacher).first()

        if query_teacher.group1 == None and query_teacher.group2 == None and query_teacher.group3 == None and \
                query_teacher.group4 == None and query_teacher.group5 == None and \
                query_teacher.group6 == None and query_teacher.group7 == None and \
                query_teacher.group8 == None and query_teacher.group9 == None and query_teacher.group10 is None:
            Teachers.query.filter_by(id=pick_teacher).update({'group1': group.id})
            db.session.commit()

        elif query_teacher.group1 != None and query_teacher.group2 == None and query_teacher.group3 == None \
                and query_teacher.group4 == None and query_teacher.group5 == None and \
                query_teacher.group6 == None and query_teacher.group7 == None and \
                query_teacher.group8 == None and query_teacher.group9 == None and query_teacher.group10 == None:

            Teachers.query.filter_by(id=pick_teacher).update({'group2': group.id})
            db.session.commit()

        elif query_teacher.group1 != None and query_teacher.group2 != None and query_teacher.group3 == None \
                and query_teacher.group4 == None and query_teacher.group5 == None and \
                query_teacher.group6 == None and query_teacher.group7 == None and \
                query_teacher.group8 == None and query_teacher.group9 == None and query_teacher.group10 == None:

            Teachers.query.filter_by(id=pick_teacher).update({'group3': group.id})
            db.session.commit()

        elif query_teacher.group1 != None and query_teacher.group2 != None and query_teacher.group3 != None \
                and query_teacher.group4 == None and query_teacher.group5 == None and \
                query_teacher.group6 == None and query_teacher.group7 == None and \
                query_teacher.group8 == None and query_teacher.group9 == None and query_teacher.group10 == None:

            Teachers.query.filter_by(id=pick_teacher).update({'group4': group.id})
            db.session.commit()

        elif query_teacher.group1 != None and query_teacher.group2 != None and query_teacher.group3 != None \
                and query_teacher.group4 !=  None and query_teacher.group5 == None and \
                query_teacher.group6 == None and query_teacher.group7 == None and \
                query_teacher.group8 == None and query_teacher.group9 == None and query_teacher.group10 == None:

            Teachers.query.filter_by(id=pick_teacher).update({'group5': group.id})
            db.session.commit()

        elif query_teacher.group1 != None and query_teacher.group2 != None and query_teacher.group3 != None \
                and query_teacher.group4 != None and query_teacher.group5 != None and \
                query_teacher.group6 == None and query_teacher.group7 == None and \
                query_teacher.group8 == None and query_teacher.group9 == None and query_teacher.group10 == None:

            Teachers.query.filter_by(id=pick_teacher).update({'group6': group.id})
            db.session.commit()

        elif query_teacher.group1 != None and query_teacher.group2 != None and query_teacher.group3 != None \
                and query_teacher.group4 != None and query_teacher.group5 != None and \
                query_teacher.group6 != None and query_teacher.group7 == None and \
                query_teacher.group8 == None and query_teacher.group9 == None and query_teacher.group10 == None:

            Teachers.query.filter_by(id=pick_teacher).update({'group7': group.id})
            db.session.commit()

        elif query_teacher.group1 != None and query_teacher.group2 != None and query_teacher.group3 != None \
                and query_teacher.group4 != None and query_teacher.group5 != None and \
                query_teacher.group6 != None and query_teacher.group7 != None and \
                query_teacher.group8 == None and query_teacher.group9 == None and query_teacher.group10 == None:

            Teachers.query.filter_by(id=pick_teacher).update({'group8': group.id})
            db.session.commit()

        elif query_teacher.group1 != None and query_teacher.group2 != None and query_teacher.group3 != None \
                and query_teacher.group4 != None and query_teacher.group5 != None and \
                query_teacher.group6 != None and query_teacher.group7 != None and \
                query_teacher.group8 != None and query_teacher.group9 == None and query_teacher.group10 == None:
            Teachers.query.filter_by(id=pick_teacher).update({'group9': group.id})
            db.session.commit()

        if query_teacher.group1 != None and query_teacher.group2 != None and query_teacher.group3 != None \
                and query_teacher.group4 != None and query_teacher.group5 != None and \
                query_teacher.group6 != None and query_teacher.group7 != None and \
                query_teacher.group8 != None and query_teacher.group9 != None and query_teacher.group10 == None:
            Teachers.query.filter_by(id=pick_teacher).update({'group10': group.id})
            db.session.commit()

        query = Student.query.filter_by(for_group=True,locations=user.locations).all()
        for student in query:
            if student.group1 == None and student.group2 == None and student.group3 == None:
                if add.subject == student.subject_1:
                    Student.query.filter(Student.id==student.id, Student.for_group == True, Student.group1 == None, Student.group2 == None,
                                         Student.group3 == None).update(
                        {'group1': add.id, 'for_group': False, 'subject_1': None})
                    db.session.commit()
                    db.session.rollback()
                if add.subject == student.subject_2:
                    Student.query.filter(Student.id==student.id,Student.for_group == True, Student.group1 == None, Student.group2 == None,
                                         Student.group3 == None).update(
                        {'group1': add.id, 'for_group': False, 'subject_2': None})
                    db.session.commit()
                    db.session.rollback()
                if add.subject == student.subject_3:
                    Student.query.filter(Student.id==student.id,Student.for_group == True, Student.group1 == None, Student.group2 == None,
                                         Student.group3 == None).update(
                        {'group1': add.id, 'for_group': False, 'subject_3': None})
                    db.session.commit()
                    db.session.rollback()
            if student.group1 != None and student.group2 == None and student.group3 == None:
                if add.subject == student.subject_1:
                    Student.query.filter(Student.id==student.id,Student.for_group == True, Student.group1 != None,
                                         Student.group2 == None,
                                         Student.group3 == None).update(
                        {'group2': add.id, 'for_group': False, 'subject_1': None})
                    db.session.commit()
                    db.session.rollback()
                if add.subject == student.subject_2:
                    Student.query.filter(Student.id==student.id,Student.for_group == True, Student.group1 != None,
                                         Student.group2 == None,
                                         Student.group3 == None).update(
                        {'group2': add.id, 'for_group': False, 'subject_2': None})
                    db.session.commit()
                    db.session.rollback()
                if add.subject == student.subject_3:
                    Student.query.filter(Student.id==student.id,Student.for_group == True, Student.group1 != None,
                                         Student.group2 == None,
                                         Student.group3 == None).update(
                        {'group2': add.id, 'for_group': False, 'subject_3': None})
                    db.session.commit()
                    db.session.rollback()
            elif student.group1 != None and student.group2 != None and student.group3 == None:
                if add.subject == student.subject_1:
                    Student.query.filter(Student.id==student.id,Student.for_group == True, Student.group1 !=  None,
                                         Student.group2 != None,
                                         Student.group3 == None).update(
                        {'group3': add.id, 'for_group': False, 'subject_1': None})
                    db.session.commit()
                    db.session.rollback()
                if add.subject == student.subject_2:
                    Student.query.filter(Student.id==student.id,Student.for_group == True, Student.group1 != None,
                                         Student.group2 != None,
                                         Student.group3 == None).update(
                        {'group3': add.id, 'for_group': False, 'subject_2': None})
                    db.session.commit()
                    db.session.rollback()
                if add.subject == student.subject_3:
                    Student.query.filter(Student.id==student.id,Student.for_group == True, Student.group1 != None,
                                         Student.group2 != None,
                                         Student.group3 == None).update(
                        {'group3': add.id, 'for_group': False, 'subject_3': None})
                    db.session.commit()
                    db.session.rollback()

        db.session.commit()
        flash('Вы успешно создали группу')
        return redirect(url_for('new_home'))
    teachers = Teachers.query.filter_by(id=pick_teacher).first()
    students = Student.query.filter(or_(Student.subject_1 == teachers.subject, Student.subject_2 == teachers.subject,
                                        Student.subject_3 == teachers.subject)).order_by('id').all()
    student = Student.query.filter(or_(Student.subject_1 == teachers.subject, Student.subject_2 == teachers.subject,
                                       Student.subject_3 == teachers.subject)).first()
    return render_template('new/create_group.html', user=user, teachers=teachers, students=students, student=student,
                           pick_teacher=pick_teacher, group_name=group_name, type_of_course=type_of_course, price=price)


@app.route('/chosen_student/<int:check_id>', methods=["POST"])
def check1(check_id):
    completed = request.get_json()['completed']
    Student.query.filter_by(id=check_id).update({'for_group': completed})
    db.session.commit()
    return "Yes"
