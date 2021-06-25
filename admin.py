from app import get_current_user, app, redirect, render_template, request, url_for, db, get_current_teacher, or_, flash

from models import Teachers, Student, Groups


@app.route('/move_to_group/<check_id>', methods=["POST"])
def check3(check_id):
    completed = request.get_json()['completed']
    todo_id = Student.query.get(check_id)
    todo_id.for_moved = completed
    db.session.commit()


@app.route('/inside_of_group/<int:id>', methods=['POST', 'GET'])
def inside_of_group(id):
    user = get_current_user()
    try:
        if not user.xojakent_admin and not user.director and not user.gazalkent_admin and not user.chirchiq_admin:
            return redirect(url_for('nav'))
    except AttributeError:
        return redirect(url_for('nav'))
    group = Groups.query.filter_by(id=id).first()
    groups = Groups.query.order_by('id').all()
    experts = Teachers.query.filter_by(subject=group.subject).all()
    student = Student.query.filter(
        or_(Student.group1 == group.id, Student.group2 == group.id, Student.group3 == group.id)).all()

    return render_template('new/Inside of Group.html', group=group, user=user, teachers=experts, group_id=id,
                           student=student, groups=groups)


@app.route('/delete_group/<int:group_id>/<int:teacher_id>/<subject>')
def delete_group(group_id, teacher_id, subject):
    user = get_current_user()
    try:
        if not user.xojakent_admin and not user.director and not user.gazalkent_admin and not user.chirchiq_admin:
            return redirect(url_for('nav'))
    except AttributeError:
        return redirect(url_for('nav'))
    del_gr = Groups.query.filter_by(id=group_id).first()
    students = Student.query.filter(
        or_(Student.group1 == group_id, Student.group2 == group_id, Student.group3 == group_id)).all()
    for student in students:
        if student.group1 == group_id:
            if not student.subject_1:
                Student.query.filter_by(group1=group_id, id=student.id).update({'group1': student.group2,
                                                                                'group2': student.group3,
                                                                                'group3': None,
                                                                                'subject_1': subject})
                db.session.commit()
            if not student.subject_2:
                Student.query.filter_by(group1=group_id, id=student.id).update({'group1': student.group2,
                                                                                'group2': student.group3,
                                                                                'group3': None,
                                                                                'subject_2': subject})
                db.session.commit()
            if not student.subject_3:
                Student.query.filter_by(group1=group_id, id=student.id).update({'group1': student.group2,
                                                                                'group2': student.group3,
                                                                                'group3': None,
                                                                                'subject_3': subject})
                db.session.commit()

        if student.group2 == group_id:
            if not student.subject_1:
                Student.query.filter_by(group2=group_id, id=student.id).update({'group2': student.group3,
                                                                                'group3': None,
                                                                                'subject_1': subject})
                db.session.commit()
            if not student.subject_2:
                Student.query.filter_by(group2=group_id, id=student.id).update({'group2': student.group3,
                                                                                'group3': None,
                                                                                'subject_2': subject})
                db.session.commit()
            if not student.subject_3:
                Student.query.filter_by(group2=group_id, id=student.id).update({'group2': student.group3,
                                                                                'group3': None,
                                                                                'subject_3': subject})
                db.session.commit()
        if student.group3 == group_id:
            if not student.subject_1:
                Student.query.filter_by(group3=group_id, id=student.id).update({'group3': None,
                                                                                'subject_1': subject})
                db.session.commit()
            if not student.subject_2:
                Student.query.filter_by(group3=group_id, id=student.id).update({'group3': None,
                                                                                'subject_2': subject})
                db.session.commit()
            if not student.subject_3:
                Student.query.filter_by(group3=group_id, id=student.id).update({'group3': None,
                                                                                'subject_3': subject})
                db.session.commit()
    teacher = Teachers.query.filter_by(id=teacher_id).first()

    if teacher.group1 == group_id:
        Teachers.query.filter_by(id=teacher_id, group1=group_id).update({'group1': teacher.group2,
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
    elif teacher.group2 == group_id:
        Teachers.query.filter_by(id=teacher_id, group2=group_id).update({'group2': teacher.group3,
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
    elif teacher.group3 == group_id:
        Teachers.query.filter_by(id=teacher_id, group3=group_id).update({'group3': teacher.group4,
                                                                         'group4': teacher.group5,
                                                                         'group5': teacher.group6,
                                                                         'group6': teacher.group7,
                                                                         'group7': teacher.group8,
                                                                         'group8': teacher.group9,
                                                                         'group9': teacher.group10,
                                                                         'group10': None
                                                                         })
        db.session.commit()
    elif teacher.group4 == group_id:
        Teachers.query.filter_by(id=teacher_id, group4=group_id).update({'group4': teacher.group5,
                                                                         'group5': teacher.group6,
                                                                         'group6': teacher.group7,
                                                                         'group7': teacher.group8,
                                                                         'group8': teacher.group9,
                                                                         'group9': teacher.group10,
                                                                         'group10': None
                                                                         })
        db.session.commit()
    elif teacher.group5 == group_id:
        Teachers.query.filter_by(id=teacher_id, group5=group_id).update({'group5': teacher.group6,
                                                                         'group6': teacher.group7,
                                                                         'group7': teacher.group8,
                                                                         'group8': teacher.group9,
                                                                         'group9': teacher.group10,
                                                                         'group10': None
                                                                         })
        db.session.commit()

    elif teacher.group6 == group_id:
        Teachers.query.filter_by(id=teacher_id, group6=group_id).update({'group6': teacher.group7,
                                                                         'group7': teacher.group8,
                                                                         'group8': teacher.group9,
                                                                         'group9': teacher.group10,
                                                                         'group10': None
                                                                         })
        db.session.commit()
    elif teacher.group7 == group_id:
        Teachers.query.filter_by(id=teacher_id, group7=group_id).update({'group7': teacher.group8,
                                                                         'group8': teacher.group9,
                                                                         'group9': teacher.group10,
                                                                         'group10': None
                                                                         })
        db.session.commit()
    elif teacher.group8 == group_id:
        Teachers.query.filter_by(id=teacher_id, group8=group_id).update({'group8': teacher.group9,
                                                                         'group9': teacher.group10,
                                                                         'group10': None
                                                                         })
        db.session.commit()
    elif teacher.group9 == group_id:
        Teachers.query.filter_by(id=teacher_id, group9=group_id).update({'group9': teacher.group10,
                                                                         'group10': None
                                                                         })
        db.session.commit()
    elif teacher.group10 == group_id:
        Teachers.query.filter_by(id=teacher_id, group10=group_id).update({'group10': None
                                                                          })
        db.session.commit()
    del_gr.delete()
    flash('Группа успешно удалена')
    return redirect(url_for('new_home'))


@app.route('/add_teacher<group_id>', methods=["POST", "GET"])
def add_teacher(group_id):
    user = get_current_user()
    try:
        if not user.xojakent_admin and not user.director and not user.gazalkent_admin:
            return redirect(url_for('nav'))
    except AttributeError:
        return redirect(url_for('nav'))
    teacher_id = request.form.get('names')
    group = Groups.query.filter_by(id=group_id).first()
    query_teacher = Teachers.query.filter_by(id=teacher_id).first()

    if query_teacher.group1 is None and query_teacher.group2 is None and query_teacher.group3 is None and \
            query_teacher.group4 is None and query_teacher.group5 is None and \
            query_teacher.group6 is None and query_teacher.group7 is None and \
            query_teacher.group8 is None and query_teacher.group9 is None and query_teacher.group10 is None:
        Teachers.query.filter_by(id=teacher_id).update({'group1': group.id})
        db.session.commit()
        Groups.query.filter_by(id=group_id).update(
            {'teacher_1': query_teacher.id, 'teacher_name': query_teacher.name,
             'teacher_surname': query_teacher.surname})
        db.session.commit()

    elif query_teacher.group1 is not None and query_teacher.group2 is None and query_teacher.group3 is None \
            and query_teacher.group4 is None and query_teacher.group5 is None and \
            query_teacher.group6 is None and query_teacher.group7 is None and \
            query_teacher.group8 is None and query_teacher.group9 is None and query_teacher.group10 is None:
        if query_teacher.group1 == group.id:
            return 'Bu grda ustoz uje bor'
        else:
            Teachers.query.filter_by(id=teacher_id).update({'group2': group.id})
            db.session.commit()
            Groups.query.filter_by(id=group_id).update(
                {'teacher_1': query_teacher.id, 'teacher_name': query_teacher.name,
                 'teacher_surname': query_teacher.surname})
            db.session.commit()

    elif query_teacher.group1 is not None and query_teacher.group2 is not None and query_teacher.group3 is None \
            and query_teacher.group4 is None and query_teacher.group5 is None and \
            query_teacher.group6 is None and query_teacher.group7 is None and \
            query_teacher.group8 is None and query_teacher.group9 is None and query_teacher.group10 is None:
        if query_teacher.group1 == group.id:
            return 'Bu grda ustoz uje bor'
        elif query_teacher.group2 == group.id:
            return 'Bu grda ustoz uje bor'

        else:
            Teachers.query.filter_by(id=teacher_id).update({'group3': group.id})
            db.session.commit()
            Groups.query.filter_by(id=group_id).update(
                {'teacher_1': query_teacher.id, 'teacher_name': query_teacher.name,
                 'teacher_surname': query_teacher.surname})
            db.session.commit()


    elif query_teacher.group1 is not None and query_teacher.group2 is not None and query_teacher.group3 is not None \
            and query_teacher.group4 is None and query_teacher.group5 is None and \
            query_teacher.group6 is None and query_teacher.group7 is None and \
            query_teacher.group8 is None and query_teacher.group9 is None and query_teacher.group10 is None:
        if query_teacher.group1 == group.id:
            return 'Bu grda ustoz uje bor'
        elif query_teacher.group2 == group.id:
            return 'Bu grda ustoz uje bor'
        elif query_teacher.group3 == group.id:
            return 'Bu grda ustoz uje bor'
        else:
            Teachers.query.filter_by(id=teacher_id).update({'group4': group.id})
            db.session.commit()
            Groups.query.filter_by(id=group_id).update(
                {'teacher_1': query_teacher.id, 'teacher_name': query_teacher.name,
                 'teacher_surname': query_teacher.surname})
            db.session.commit()

    elif query_teacher.group1 is not None and query_teacher.group2 is not None and query_teacher.group3 is not None \
            and query_teacher.group4 is not None and query_teacher.group5 is None and \
            query_teacher.group6 is None and query_teacher.group7 is None and \
            query_teacher.group8 is None and query_teacher.group9 is None and query_teacher.group10 is None:
        if query_teacher.group1 == group.id:
            return 'Bu grda ustoz uje bor'
        elif query_teacher.group2 == group.id:
            return 'Bu grda ustoz uje bor'
        elif query_teacher.group3 == group.id:
            return 'Bu grda ustoz uje bor'
        elif query_teacher.group4 == group.id:
            return 'Bu grda ustoz uje bor'
        else:
            Teachers.query.filter_by(id=teacher_id).update({'group5': group.id})
            db.session.commit()
            Groups.query.filter_by(id=group_id).update(
                {'teacher_1': query_teacher.id, 'teacher_name': query_teacher.name,
                 'teacher_surname': query_teacher.surname})
            db.session.commit()

    elif query_teacher.group1 is not None and query_teacher.group2 is not None and query_teacher.group3 is not None \
            and query_teacher.group4 is not None and query_teacher.group5 is not None and \
            query_teacher.group6 is None and query_teacher.group7 is None and \
            query_teacher.group8 is None and query_teacher.group9 is None and query_teacher.group10 is None:
        if query_teacher.group1 == group.id:
            return 'Bu grda ustoz uje bor'
        elif query_teacher.group2 == group.id:
            return 'Bu grda ustoz uje bor'
        elif query_teacher.group3 == group.id:
            return 'Bu grda ustoz uje bor'
        elif query_teacher.group4 == group.id:
            return 'Bu grda ustoz uje bor'
        elif query_teacher.group5 == group.id:
            return 'Bu grda ustoz uje bor'
        else:
            Teachers.query.filter_by(id=teacher_id).update({'group6': group.id})
            db.session.commit()
            Groups.query.filter_by(id=group_id).update(
                {'teacher_1': query_teacher.id, 'teacher_name': query_teacher.name,
                 'teacher_surname': query_teacher.surname})
            db.session.commit()

    elif query_teacher.group1 is not None and query_teacher.group2 is not None and query_teacher.group3 is not None \
            and query_teacher.group4 is not None and query_teacher.group5 is not None and \
            query_teacher.group6 is not None and query_teacher.group7 is None and \
            query_teacher.group8 is None and query_teacher.group9 is None and query_teacher.group10 is None:
        if query_teacher.group1 == group.id:
            return 'Bu grda ustoz uje bor'
        elif query_teacher.group2 == group.id:
            return 'Bu grda ustoz uje bor'
        elif query_teacher.group3 == group.id:
            return 'Bu grda ustoz uje bor'
        elif query_teacher.group4 == group.id:
            return 'Bu grda ustoz uje bor'
        elif query_teacher.group5 == group.id:
            return 'Bu grda ustoz uje bor'
        elif query_teacher.group6 == group.id:
            return 'Bu grda ustoz uje bor'
        else:
            Teachers.query.filter_by(id=teacher_id).update({'group7': group.id})
            db.session.commit()
            Groups.query.filter_by(id=group_id).update(
                {'teacher_1': query_teacher.id, 'teacher_name': query_teacher.name,
                 'teacher_surname': query_teacher.surname})
            db.session.commit()

    elif query_teacher.group1 is not None and query_teacher.group2 is not None and query_teacher.group3 is not None \
            and query_teacher.group4 is not None and query_teacher.group5 is not None and \
            query_teacher.group6 is not None and query_teacher.group7 is not None and \
            query_teacher.group8 is None and query_teacher.group9 is None and query_teacher.group10 is None:
        if query_teacher.group1 == group.id:
            return 'Bu grda ustoz uje bor'
        elif query_teacher.group2 == group.id:
            return 'Bu grda ustoz uje bor'
        elif query_teacher.group3 == group.id:
            return 'Bu grda ustoz uje bor'
        elif query_teacher.group4 == group.id:
            return 'Bu grda ustoz uje bor'
        elif query_teacher.group5 == group.id:
            return 'Bu grda ustoz uje bor'
        elif query_teacher.group6 == group.id:
            return 'Bu grda ustoz uje bor'
        elif query_teacher.group7 == group.id:
            return 'Bu grda ustoz uje bor'
        else:
            Teachers.query.filter_by(id=teacher_id).update({'group8': group.id})
            db.session.commit()
            Groups.query.filter_by(id=group_id).update(
                {'teacher_1': query_teacher.id, 'teacher_name': query_teacher.name,
                 'teacher_surname': query_teacher.surname})
            db.session.commit()

    elif query_teacher.group1 is not None and query_teacher.group2 is not None and query_teacher.group3 is not None \
            and query_teacher.group4 is not None and query_teacher.group5 is not None and \
            query_teacher.group6 is not None and query_teacher.group7 is not None and \
            query_teacher.group8 is not None and query_teacher.group9 is None and query_teacher.group10 is None:
        if query_teacher.group1 == group.id:
            return 'Bu grda ustoz uje bor'
        elif query_teacher.group2 == group.id:
            return 'Bu grda ustoz uje bor'
        elif query_teacher.group3 == group.id:
            return 'Bu grda ustoz uje bor'
        elif query_teacher.group4 == group.id:
            return 'Bu grda ustoz uje bor'
        elif query_teacher.group5 == group.id:
            return 'Bu grda ustoz uje bor'
        elif query_teacher.group6 == group.id:
            return 'Bu grda ustoz uje bor'
        elif query_teacher.group7 == group.id:
            return 'Bu grda ustoz uje bor'
        elif query_teacher.group8 == group.id:
            return 'Bu grda ustoz uje bor'
        else:
            Teachers.query.filter_by(id=teacher_id).update({'group9': group.id})
            db.session.commit()
            Groups.query.filter_by(id=group_id).update(
                {'teacher_1': query_teacher.id, 'teacher_name': query_teacher.name,
                 'teacher_surname': query_teacher.surname})
            db.session.commit()

    elif query_teacher.group1 is not None and query_teacher.group2 is not None and query_teacher.group3 is not None \
            and query_teacher.group4 is not None and query_teacher.group5 is not None and \
            query_teacher.group6 is not None and query_teacher.group7 is not None and \
            query_teacher.group8 is not None and query_teacher.group9 is not None and query_teacher.group10 is None:
        if query_teacher.group1 == group.id:
            return 'Bu grda ustoz uje bor'
        elif query_teacher.group2 == group.id:
            return 'Bu grda ustoz uje bor'
        elif query_teacher.group3 == group.id:
            return 'Bu grda ustoz uje bor'
        elif query_teacher.group4 == group.id:
            return 'Bu grda ustoz uje bor'
        elif query_teacher.group5 == group.id:
            return 'Bu grda ustoz uje bor'
        elif query_teacher.group6 == group.id:
            return 'Bu grda ustoz uje bor'
        elif query_teacher.group7 == group.id:
            return 'Bu grda ustoz uje bor'
        elif query_teacher.group8 == group.id:
            return 'Bu grda ustoz uje bor'
        elif query_teacher.group9 == group.id:
            return 'Bu grda ustoz uje bor'
        else:
            Teachers.query.filter_by(id=teacher_id).update({'group10': group.id})
            db.session.commit()
            Groups.query.filter_by(id=group_id).update(
                {'teacher_1': query_teacher.id, 'teacher_name': query_teacher.name,
                 'teacher_surname': query_teacher.surname})
            db.session.commit()
    flash('Учитель добавлен успешно')
    return redirect(url_for('inside_of_group', id=group_id))
