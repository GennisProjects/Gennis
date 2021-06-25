from app import app, get_current_teacher, get_current_user, render_template, redirect, url_for, request, or_, db, \
    PhotoForm, flash
from models import Teachers, Groups, Student, Attendance, All_Charity_Sums, Teacher_cash
from datetime import datetime, timedelta, date
from jinja2 import UndefinedError


@app.route('/my_group1')
def my_group1():
    user = get_current_user()
    teacher = get_current_teacher()
    form = PhotoForm(meta={'csrf': False})
    try:
        if not teacher:
            return redirect(url_for('nav'))
    except AttributeError:
        return redirect(url_for('nav'))
    teach = Teachers.query.filter_by(id=teacher.id).first()
    group1 = Groups.query.filter_by(id=teach.group1).first()
    group2 = Groups.query.filter_by(id=teach.group2).first()
    group3 = Groups.query.filter_by(id=teach.group3).first()
    group4 = Groups.query.filter_by(id=teach.group4).first()
    group5 = Groups.query.filter_by(id=teach.group5).first()
    group6 = Groups.query.filter_by(id=teach.group6).first()
    group7 = Groups.query.filter_by(id=teach.group7).first()
    group8 = Groups.query.filter_by(id=teach.group8).first()
    group9 = Groups.query.filter_by(id=teach.group9).first()
    group10 = Groups.query.filter_by(id=teach.group10).first()
    return render_template('new_continue/my groups.html', teacher=teacher, user=user, form=form, group1=group1,
                           group2=group2, group3=group3, group4=group4, group5=group5, group6=group6, group7=group7,
                           group8=group8, group9=group9, group10=group10)


@app.route('/teacher_inside_group/<int:group_id>')
def teacher_inside_group(group_id):
    user = get_current_user()
    teacher = get_current_teacher()
    try:
        if not teacher:
            return redirect(url_for('nav'))
    except AttributeError:
        return redirect(url_for('nav'))
    group = Groups.query.filter_by(id=group_id).first()
    students = Student.query.filter(or_(Student.group1 == group_id, Student.group2 == group_id,
                                        Student.group3 == group_id)).order_by('id').all()
    return render_template('new_continue/teacher_inside_group.html', user=user, teacher=teacher, group=group,
                           students=students)


@app.route('/give_score/<int:group_id>')
def give_score(group_id):
    user = get_current_user()
    teacher = get_current_teacher()
    today = datetime.today()
    hour = datetime.strftime(today, "%Y/%m/%d/%H")
    hour2 = datetime.strptime(hour, "%Y/%m/%d/%H")

    try:
        if not teacher:
            return redirect(url_for('nav'))
    except AttributeError:
        return redirect(url_for('nav'))
    group = Groups.query.filter_by(id=group_id).first()
    students = Student.query.filter(or_(Student.group1 == group_id, Student.group2 == group_id,
                                        Student.group3 == group_id)).order_by('id').all()
    return render_template('new_continue/give_score.html', user=user, teacher=teacher, students=students, hour2=hour2,
                           group=group)


@app.route('/giving_score/<int:student_id>/<int:group_id>', methods=["POST", "GET"])
def giving_score(student_id, group_id):
    user = get_current_user()
    teacher = get_current_teacher()
    today = datetime.today()
    hour = datetime.strftime(today, "%Y/%m/%d/%H")
    hour2 = datetime.strptime(hour, "%Y/%m/%d/%H")
    ball_time = hour2 + timedelta(hours=1)
    try:
        if not teacher:
            return redirect(url_for('nav'))
    except AttributeError:
        return redirect(url_for('nav'))
    if request.method == 'POST':
        student = Student.query.filter_by(id=student_id).first()
        group = Groups.query.filter(
            or_(Groups.id == student.group1, Groups.id == student.group2, Groups.id == student.group3)).first()
        query_teacher = Teachers.query.filter_by(id=group.teacher_1).first()
        sum = group.cost / 13 + student.charity
        for_teacher = sum / 2
        if query_teacher.salary is None:
            salary = for_teacher
        else:
            salary = query_teacher.salary + for_teacher
        if student.money is None:
            for_student_money = -sum
        else:
            for_student_money = student.money - sum
        get_date = datetime.now()
        if teacher.subject == 'Ingliz tili' or teacher.subject == 'Rus tili' or teacher.subject == "Ingliz tili+mental arifmetika" or teacher.subject == "Rus tili+mental arifmetika":
            get_homework = int(request.form.get('homework'))
            get_dictonary = int(request.form.get('dictionary'))
            get_class_activity = int(request.form.get('active'))
            plus1 = get_homework + get_dictonary + get_class_activity
            boluv2 = plus1 / 3
            add = Attendance(group_id=group_id, student_id=student_id, teacher_id=teacher.id, lugat=get_dictonary,
                             darsga_tayyorgarligi=get_homework, darsda_qatnashishi=get_class_activity,
                             ortacha_baho=boluv2, present=get_date, fan=group.subject, apset=None,
                             student_name=student.name, student_surname=student.surname,
                             student_username=student.username)
            db.session.add(add)
            db.session.commit()

        elif teacher.subject == 'Matematika' or teacher.subject == 'Tarix' or teacher.subject == 'Fizika' or \
                teacher.subject == 'Ona tili va Adabiyot' or teacher.subject == 'Biologiya' or\
                teacher.subject == 'Avto Maktab' or teacher.subject == 'Web Dasturchilik' or \
                teacher.subject == "Mental arifmetika":
            get_homework2 = int(request.form.get('homework'))
            get_class_activity2 = int(request.form.get('active'))
            plus3 = get_homework2 + get_class_activity2
            boluv3 = plus3 / 2
            add2 = Attendance(group_id=group_id, student_id=student_id, teacher_id=teacher.id,
                              darsga_tayyorgarligi=get_homework2, fan=group.subject, apset=None,
                              darsda_qatnashishi=get_class_activity2, ortacha_baho=boluv3, lugat=0, present=get_date,
                              student_name=student.name, student_surname=student.surname,
                              student_username=student.username)
            db.session.add(add2)
            db.session.commit()

        Student.query.filter_by(id=student_id).update({'money': for_student_money, 'ball_time': ball_time})
        if group.location == 1:
            salary = query_teacher.salary + for_teacher
            Teachers.query.filter_by(id=group.teacher_1).update({'salary': salary})
            db.session.commit()
        if group.location == 2:
            salary = query_teacher.salary_for_gazalkent + for_teacher
            Teachers.query.filter_by(id=group.teacher_1).update({'salary_for_gazalkent': salary})
            db.session.commit()
        if group.location == 3:
            salary = query_teacher.salary_for_chirchiq + for_teacher
            Teachers.query.filter_by(id=group.teacher_1).update({'salary_for_chirchiq': salary})
            db.session.commit()
        db.session.commit()
        if student.locations == 1:
            query_charity = All_Charity_Sums.query.filter_by(id=1).first()
            plus_charity = query_charity.bank_charity + student.charity
            All_Charity_Sums.query.filter_by(id=1).update({'bank_charity': plus_charity})
            db.session.commit()
        elif student.locations == 2:
            query_charity2 = All_Charity_Sums.query.filter_by(id=2).first()
            plus_charity2 = query_charity2.bank_charity + student.charity
            All_Charity_Sums.query.filter_by(id=2).update({'bank_charity': plus_charity2})
            db.session.commit()
        elif student.locations == 3:
            query_charity3 = All_Charity_Sums.query.filter_by(id=3).first()
            plus_charity3 = query_charity3.bank_charity + student.charity
            All_Charity_Sums.query.filter_by(id=3).update({'bank_charity': plus_charity3})
            db.session.commit()
        flash('Студент набрал баллы')
        return redirect(url_for('give_score', group_id=group_id))


@app.route('/make_absent/<int:student_id>/<int:group_id>')
def make_absent(student_id, group_id):
    user = get_current_user()
    teacher = get_current_teacher()
    today = datetime.today()
    hour = datetime.strftime(today, "%Y/%m/%d/%H")
    hour2 = datetime.strptime(hour, "%Y/%m/%d/%H")
    add2 = hour2 + timedelta(hours=1)
    try:
        if not teacher:
            return redirect(url_for('nav'))
    except AttributeError:
        return redirect(url_for('nav'))

    student = Student.query.filter_by(id=student_id).first()
    group = Groups.query.filter(or_(Groups.id == student.group1, Groups.id == student.group2,
                                    Groups.id == student.group3)).first()
    query_teacher = Teachers.query.filter_by(id=group.teacher_1).first()
    avarege_money = group.cost / 13
    for_teacher = avarege_money / 2
    for_student = student.money - avarege_money + student.charity
    get_date = datetime.now()
    Student.query.filter_by(id=student_id).update({'money': for_student, 'ball_time': add2})
    if group.location == 1:
        salary = query_teacher.salary + for_teacher
        Teachers.query.filter_by(id=group.teacher_1).update({'salary': salary})
        db.session.commit()
    if group.location == 2:
        salary = query_teacher.salary_for_gazalkent + for_teacher
        Teachers.query.filter_by(id=group.teacher_1).update({'salary_for_gazalkent': salary})
        db.session.commit()
    if group.location == 3:
        salary = query_teacher.salary_for_chirchiq + for_teacher
        Teachers.query.filter_by(id=group.teacher_1).update({'salary_for_chirchiq': salary})
        db.session.commit()
    add = Attendance(group_id=group_id, student_id=student_id, teacher_id=teacher.id, present=None, apset=get_date,
                     student_name=student.name, student_surname=student.surname, student_username=student.username)
    db.session.add(add)
    db.session.commit()
    if student.locations == 1:
        query_charity = All_Charity_Sums.query.filter_by(id=1).first()
        plus_charity = query_charity.bank_charity + student.charity
        All_Charity_Sums.query.filter_by(id=1).update({'bank_charity': plus_charity})
        db.session.commit()
    elif student.locations == 2:
        query_charity2 = All_Charity_Sums.query.filter_by(id=2).first()
        plus_charity2 = query_charity2.bank_charity + student.charity
        All_Charity_Sums.query.filter_by(id=2).update({'bank_charity': plus_charity2})
        db.session.commit()
    elif student.locations == 3:
        query_charity3 = All_Charity_Sums.query.filter_by(id=2).first()
        plus_charity3 = query_charity3.bank_charity + student.charity
        All_Charity_Sums.query.filter_by(id=3).update({'bank_charity': plus_charity3})
        db.session.commit()
    flash('Студент отмечен как отсутствующий')
    return redirect(url_for('give_score', group_id=group_id))


@app.route('/check1/<check_id>', methods=["POST"])
def check2(check_id):
    completed = request.get_json()['completed']
    todo_id = Student.query.get(check_id)
    todo_id.attendance = completed
    db.session.commit()
    return redirect(url_for('my_group1'))


@app.route('/see_att/<id>')
def see_att(id):
    user = get_current_user()
    teacher = get_current_teacher()
    try:
        if not teacher and not user:
            return redirect(url_for('nav'))
    except AttributeError:
        return redirect(url_for('nav'))
    attendance_present = Attendance.query.filter_by(group_id=id,
                                                    apset=None).order_by(Attendance.id.desc()).limit(30)

    attendance_absent = Attendance.query.filter_by(group_id=id,
                                                   present=None).order_by(Attendance.id.desc()).limit(30)
    return render_template('new_continue/student_att.html', user=user, teacher=teacher, id=id,
                           attendance_absent=attendance_absent, attendance_present=attendance_present)


@app.route('/student_profile_for_teacher/<int:student_id>/<int:group_id>')
def student_profile_for_teacher(student_id, group_id):
    user = get_current_user()
    teacher = get_current_teacher()
    try:
        if not teacher and not user:
            return redirect(url_for('nav'))
    except AttributeError:
        return redirect(url_for('nav'))

    student = Student.query.filter_by(id=student_id).first()
    attendance_present = Attendance.query.filter_by(student_id=student_id,group_id=group_id,
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

    attendance_absent = Attendance.query.filter_by(student_id=student_id,group_id=group_id,
                                                   present=None).order_by(Attendance.id.desc()).limit(30)

    return render_template('new_continue/student_profile_for_teacher.html', user=user, student=student,
                           student_id=student_id, teacher=teacher,attendance_present=attendance_present,
                           attendance_absent=attendance_absent,group_id=group_id,total=total)


@app.route('/see_salary/<salary>')
def see_salary(salary):
    user = get_current_user()
    teacher = get_current_teacher()
    try:
        if not teacher:
            return redirect(url_for('nav'))
    except AttributeError:
        return redirect(url_for('nav'))

    list_salary = Teacher_cash.query.filter_by(teacher_id=teacher.id,locations=salary).all()
    return render_template('new_continue/teacher_salary_list.html',user=user,teacher=teacher,list_salary=list_salary)


