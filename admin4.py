from datetime import datetime
from app import app, render_template, redirect, request, url_for, get_current_user, db, PhotoForm,or_,flash
from models import Teachers, Student, Student_cash, Overhead, Capital_expenditure, Teacher_cash, Withdrawal, Groups, \
    All_Charity_Sums, Shartnoma

now = datetime.now()


@app.route('/calculate/<id>', methods=['POST'])
def calculate(id):
    user = get_current_user()
    try:
        if not user.gazalkent_admin and not user.chirchiq_admin and not user.xojakent_admin:
            return redirect(url_for('nav'))
    except AttributeError:
        return redirect(url_for('nav'))
    money = int(request.form.get('pay'))
    student = Student.query.filter_by(id=id).first()
    data = datetime.now()
    total = student.money + money
    Student.query.filter_by(id=id).update({"money": total})
    if user.xojakent_admin:
        add = Student_cash(student_id=id, debt=student.money, payment=money, result=total, payment_data=data,
                           username=student.username,
                           student_name=student.name, student_surname=student.surname, locations='xojakent')
        add.add()
    elif user.gazalkent_admin:
        add2 = Student_cash(student_id=id, debt=student.money, payment=money, result=total, payment_data=data,
                            username=student.username,
                            student_name=student.name, student_surname=student.surname, locations='gazalkent')
        add2.add()
    elif user.chirchiq_admin:
        add2 = Student_cash(student_id=id, debt=student.money, payment=money, result=total, payment_data=data,
                            username=student.username,
                            student_name=student.name, student_surname=student.surname, locations='chirchiq')
        add2.add()
    flash('Оплата прошла успешно')
    return redirect(url_for('student_info',student_id=id))


@app.route('/salary_give/<id>', methods=['POST'])
def salary_give(id):
    user = get_current_user()
    try:
        if not user.gazalkent_admin and not user.chirchiq_admin and not user.xojakent_admin:
            return redirect(url_for('nav'))
    except AttributeError:
        return redirect(url_for('nav'))
    salary = int(request.form.get('teacher_salary'))
    teacher = Teachers.query.filter_by(id=id).first()
    all = teacher.salary - salary
    if user.xojakent_admin:
        add = Teacher_cash(teacher_id=teacher.id, teacher_name=teacher.name, teacher_surname=teacher.surname,
                           username=teacher.username, payment=salary, payment_data=now, salary=teacher.salary,
                           result=all, locations='xojakent')
        db.session.add(add)
        db.session.commit()
        all = teacher.salary - salary
        Teachers.query.filter_by(id=id).update({'salary': all})
        db.session.commit()
    elif user.gazalkent_admin:
        add2 = Teacher_cash(teacher_id=teacher.id, teacher_name=teacher.name, teacher_surname=teacher.surname,
                            username=teacher.username, payment=salary, payment_data=now, salary=teacher.salary,
                            result=all, locations='gazalkent')
        db.session.add(add2)
        db.session.commit()
        all = teacher.salary_for_gazalkent - salary
        Teachers.query.filter_by(id=id).update({'salary_for_gazalkent': all})
        db.session.commit()
    elif user.chirchiq_admin:
        add3 = Teacher_cash(teacher_id=teacher.id, teacher_name=teacher.name, teacher_surname=teacher.surname,
                            username=teacher.username, payment=salary, payment_data=now, salary=teacher.salary,
                            result=all, locations='chirchiq')
        db.session.add(add3)
        db.session.commit()
        all = teacher.salary_for_chirchiq - salary
        Teachers.query.filter_by(id=id).update({'salary_for_chirchiq': all})
        db.session.commit()
    flash('Выдача зарплаты прошла успешно')
    return redirect(url_for('teacher_profile', id=id))


@app.route('/overhead', methods=['POST'])
def overhead():
    user = get_current_user()
    try:
        if not user.gazalkent_admin and not user.chirchiq_admin and not user.xojakent_admin:
            return redirect(url_for('nav'))
    except AttributeError:
        return redirect(url_for('nav'))
    if request.method == 'POST':
        reason = request.form.get('reason')
        amount = request.form.get('amount')
        sums = int(request.form.get('sum'))
        now = datetime.now()
        if user.xojakent_admin:
            save = Overhead(reason=reason, quantity=amount, sum=sums, payed_data=now, locations='xojakent')
            db.session.add(save)
            db.session.commit()
        if user.gazalkent_admin:
            save2 = Overhead(reason=reason, quantity=amount, sum=sums, payed_data=now, locations='gazalkent')
            db.session.add(save2)
            db.session.commit()
        if user.chirchiq_admin:
            save3 = Overhead(reason=reason, quantity=amount, sum=sums, payed_data=now, locations='chirchiq')
            db.session.add(save3)
            db.session.commit()
        flash('Данные успешно добавлены')
        return redirect(url_for('payment'))


@app.route('/capital', methods=['POST'])
def capital():
    user = get_current_user()
    try:
        if not user.gazalkent_admin and not user.chirchiq_admin and not user.xojakent_admin:
            return redirect(url_for('nav'))
    except AttributeError:
        return redirect(url_for('nav'))
    if request.method == 'POST':
        name_item = request.form.get('name_item')
        number_item = int(request.form.get('number_item'))
        sums = int(request.form.get('amount_item'))
        now = datetime.now()
        if user.xojakent_admin:
            save = Capital_expenditure(item=name_item, number_items=number_item, amount_item=sums,
                                       bought_data=now, locations='xojakent')
            db.session.add(save)
            db.session.commit()
        if user.gazalkent_admin:
            save2 = Capital_expenditure(item=name_item, number_items=number_item, amount_item=sums,
                                        bought_data=now, locations='gazalkent')
            db.session.add(save2)
            db.session.commit()
        if user.chirchiq_admin:
            save3 = Capital_expenditure(item=name_item, number_items=number_item, amount_item=sums,
                                        bought_data=now, locations='chirchiq')
            db.session.add(save3)
            db.session.commit()
        flash('Данные успешно добавлены')
        return redirect(url_for('payment'))


@app.route('/payment', methods=['POST', 'GET'])
def payment():
    user = get_current_user()
    try:
        if not user.gazalkent_admin and not user.director and not user.xojakent_admin and not user.chirchiq_admin:
            return redirect(url_for('nav'))
    except AttributeError:
        return redirect(url_for('nav'))
    form = PhotoForm(meta={'csrf': False})
    capital_xojakent = Capital_expenditure.query.filter_by(locations='xojakent')
    all_cap_xoj = 0
    for cap_xoj in capital_xojakent:
        all_cap_xoj += cap_xoj.amount_item
    capital_gazalkent = Capital_expenditure.query.filter_by(locations='gazalkent')
    all_cap_gaz = 0
    for cap_gaz in capital_gazalkent:
        all_cap_gaz += cap_gaz.amount_item
    capital_chirchiq = Capital_expenditure.query.filter_by(locations='chirchiq')
    all_cap_chirchiq = 0
    for cap_chir in capital_chirchiq:
        all_cap_chirchiq += cap_chir.amount_item

    overhead_xojakent = Overhead.query.filter_by(locations='xojakent')
    all_over_xoj = 0
    for over_xoj in overhead_xojakent:
        all_over_xoj += over_xoj.sum
    overhead_gazalkent = Overhead.query.filter_by(locations='gazalkent')
    all_over_gaz = 0
    for over_gaz in overhead_gazalkent:
        all_over_gaz += over_gaz.sum
    overhead_chirchiq = Overhead.query.filter_by(locations='chirchiq')
    all_over_chir = 0
    for over_chir in overhead_chirchiq:
        all_over_chir += over_chir.sum

    withdrawal_xojakent = Withdrawal.query.filter_by(locations='xojakent')
    all_with_xoj = 0
    for with_xoj in withdrawal_xojakent:
        all_with_xoj += with_xoj.amount
    withdrawal_gazalkent = Withdrawal.query.filter_by(locations='gazalkent')
    all_with_gaz = 0
    for with_gaz in withdrawal_gazalkent:
        all_with_gaz += with_gaz.amount
    withdrawal_chirchiq = Withdrawal.query.filter_by(locations='chirchiq')
    all_with_chir = 0
    for with_chir in withdrawal_chirchiq:
        all_with_chir += with_chir.amount

    student_debt_xojakent = Student.query.filter(Student.director == False, Student.locations == 1, Student.money <= 0,
                                                 Student.xojakent_admin == False, Student.gazalkent_admin == False)
    all_debt_xoj = 0
    for debt_xoj in student_debt_xojakent:
        all_debt_xoj += debt_xoj.money
    student_debt_gazalkent = Student.query.filter(Student.director == False, Student.locations == 2, Student.money <= 0,
                                                  Student.xojakent_admin == False, Student.gazalkent_admin == False)
    all_debt_gaz = 0
    for debt_gaz in student_debt_gazalkent:
        all_debt_gaz += debt_gaz.money
    student_debt_chirchiq = Student.query.filter(Student.director == False, Student.locations == 3, Student.money <= 0,
                                                 Student.xojakent_admin == False, Student.gazalkent_admin == False)
    all_debt_chir = 0
    for debt_chir in student_debt_chirchiq:
        all_debt_chir += debt_chir.money

    xojakent_salary = Teacher_cash.query.filter_by(locations='xojakent')
    all_xoj_sal = 0
    for xoj_sal in xojakent_salary:
        all_xoj_sal += xoj_sal.payment
    gazalkent_salary = Teacher_cash.query.filter_by(locations='gazalkent')
    all_gaz_sal = 0
    for gaz_sal in gazalkent_salary:
        all_gaz_sal += gaz_sal.payment
    chirchiq_salary = Teacher_cash.query.filter_by(locations='chirchiq')
    all_chir_sal = 0
    for chir_sal in chirchiq_salary:
        all_chir_sal += chir_sal.payment

    xojakent_payment = Student_cash.query.filter_by(locations='xojakent')
    all_xoj_pay = 0
    for xoj_pay in xojakent_payment:
        all_xoj_pay += xoj_pay.payment
    gazalkent_payment = Student_cash.query.filter_by(locations='gazalkent')
    all_gaz_pay = 0
    for gaz_pay in gazalkent_payment:
        all_gaz_pay += gaz_pay.payment
    chirchiq_payment = Student_cash.query.filter_by(locations='chirchiq')
    all_chir_pay = 0
    for chir_pay in chirchiq_payment:
        all_chir_pay += chir_pay.payment

    groups_xojakent = Groups.query.filter_by(location=1)
    number_gr_xoj = list(map(Groups.info, groups_xojakent))
    all_gr_xoj = len(number_gr_xoj)

    groups_gazalkent = Groups.query.filter_by(location=2)
    number_gr_gaz = list(map(Groups.info, groups_gazalkent))
    all_gr_gaz = len(number_gr_gaz)

    groups_chirchiq = Groups.query.filter_by(location=3)
    number_gr_chir = list(map(Groups.info, groups_chirchiq))
    all_gr_chir = len(number_gr_chir)

    student_xojakent = Student.query.filter(Student.locations == 1, Student.group1 != None,
                                            Student.director == False,
                                            Student.gazalkent_admin == False, Student.xojakent_admin == False)
    number_students_xoj = list(map(Student.info, student_xojakent))
    all_st_xoj = len(number_students_xoj)
    student_gazalkent = Student.query.filter(Student.locations == 2, Student.group1 != None,
                                             Student.director == False,
                                             Student.gazalkent_admin == False, Student.xojakent_admin == False)
    number_students_gaz = list(map(Student.info, student_gazalkent))
    all_st_gaz = len(number_students_gaz)
    student_chirchiq = Student.query.filter(Student.locations == 3, Student.group1 != None,
                                            Student.director == False, Student.chirchiq_admin == False,
                                            Student.gazalkent_admin == False, Student.xojakent_admin == False)
    number_students_chir = list(map(Student.info, student_chirchiq))
    all_st_chir = len(number_students_chir)

    xoj_charity = All_Charity_Sums.query.filter_by(id=1).first()
    gaz_charity = All_Charity_Sums.query.filter_by(id=2).first()
    chir_charity = All_Charity_Sums.query.filter_by(id=3).first()

    combine_xoj = all_cap_xoj + all_over_xoj + all_with_xoj + all_xoj_sal
    profit_xoj = all_xoj_pay - combine_xoj
    combine_gaz = all_cap_gaz + all_over_gaz + all_with_gaz + all_gaz_sal
    profit_gaz = all_gaz_pay - combine_gaz
    combine_chir = all_cap_chirchiq + all_over_chir + all_with_chir + all_chir_sal
    profit_chir = all_chir_pay - combine_chir
    return render_template('new/payment.html', user=user, capital_xojakent=capital_xojakent,
                           capital_gazalkent=capital_gazalkent, capital_chirchiq=capital_chirchiq,
                           all_cap_xoj=all_cap_xoj, all_cap_gaz=all_cap_gaz, all_cap_chirchiq=all_cap_chirchiq,
                           all_over_xoj=all_over_xoj, all_over_gaz=all_over_gaz, all_over_chir=all_over_chir,
                           overhead_xojakent=overhead_xojakent, overhead_gazalkent=overhead_gazalkent,
                           overhead_chirchiq=overhead_chirchiq,
                           all_with_xoj=all_with_xoj, all_with_gaz=all_with_gaz, all_with_chir=all_with_chir,
                           withdrawal_xojakent=withdrawal_xojakent, withdrawal_gazalkent=withdrawal_gazalkent,
                           withdrawal_chirchiq=withdrawal_chirchiq,
                           all_debt_xoj=all_debt_xoj, all_debt_gaz=all_debt_gaz, all_debt_chir=all_debt_chir,
                           student_debt_xojakent=student_debt_xojakent, student_debt_gazalkent=student_debt_gazalkent,
                           student_debt_chirchiq=student_debt_chirchiq,
                           all_xoj_sal=all_xoj_sal, all_gaz_sal=all_gaz_sal, all_chir_sal=all_chir_sal,
                           xojakent_salary=xojakent_salary, gazalkent_salary=gazalkent_salary,
                           chirchiq_salary=chirchiq_salary,
                           all_xoj_pay=all_xoj_pay, all_gaz_pay=all_gaz_pay, all_chir_pay=all_chir_pay,
                           xojakent_payment=xojakent_payment, gazalkent_payment=gazalkent_payment,
                           chirchiq_payment=chirchiq_payment,
                           all_gr_xoj=all_gr_xoj, all_gr_gaz=all_gr_gaz, all_gr_chir=all_gr_chir,
                           all_st_xoj=all_st_xoj, all_st_gaz=all_st_gaz, all_st_chir=all_st_chir,
                           xoj_charity=xoj_charity, gaz_charity=gaz_charity, chir_charity=chir_charity,
                           profit_xoj=profit_xoj, profit_gaz=profit_gaz, profit_chir=profit_chir, form=form)


@app.route('/teacher_search_name', methods=['POST'])
def teacher_search_name():
    user = get_current_user()
    try:
        if not user.gazalkent_admin and not user.director and not user.xojakent_admin:
            return redirect(url_for('nav'))
    except AttributeError:
        return redirect(url_for('nav'))
    teacher_name = Teachers.query.filter(Teachers.name.ilike("%" + request.form.get('teacher_name').upper() + "%"))
    find_name = list(map(Teachers.info, teacher_name))
    result_name = {
        "data": find_name,
        "count": len(find_name)
    }
    return render_template('new_continue/teacher_name.html', user=user, result_name=result_name,
                           search=request.form.get('teacher_name').upper())


@app.route('/teacher_search_surname', methods=['POST'])
def teacher_search_surname():
    user = get_current_user()
    try:
        if not user.gazalkent_admin and not user.director and not user.xojakent_admin:
            return redirect(url_for('nav'))
    except AttributeError:
        return redirect(url_for('nav'))
    teacher_surname = Teachers.query.filter(
        Teachers.surname.ilike("%" + request.form.get('teacher_surname').upper() + "%"))
    find_surname = list(map(Teachers.info, teacher_surname))
    result_surname = {
        "data": find_surname,
        "count": len(find_surname)
    }
    return render_template('new_continue/teacher_surname.html', user=user, result_surname=result_surname,
                           search=request.form.get('teacher_surname').upper())


@app.route('/teacher_search_username', methods=['POST'])
def teacher_search_username():
    user = get_current_user()
    try:
        if not user.gazalkent_admin and not user.director and not user.xojakent_admin:
            return redirect(url_for('nav'))
    except AttributeError:
        return redirect(url_for('nav'))
    teacher_username = Teachers.query.filter(
        Teachers.username.ilike("%" + request.form.get('teacher_username').upper() + "%"))
    find_surname = list(map(Teachers.info, teacher_username))
    result_username = {
        "data": find_surname,
        "count": len(find_surname)
    }
    return render_template('new_continue/teacher_username.html', user=user, result_username=result_username,
                           search=request.form.get('teacher_surname').upper())


@app.route('/search_name', methods=['POST'])
def search_name():
    user = get_current_user()
    try:
        if not user.director and not user.xojakent_admin:
            return redirect(url_for('nav'))
    except AttributeError:
        return redirect(url_for('nav'))
    if user.xojakent_admin or user.director:
        student_name = Student.query.filter(Student.director == False, Student.xojakent_admin == False,
                                            Student.gazalkent_admin == False, Student.locations == 1,
                                            Student.chirchiq_admin == False,Student.group1 != None,
                                            Student.name.ilike("%" + request.form.get('student').upper() + "%")).all()

        finding_name = list(map(Student.info, student_name))
        result_name = {
            "count": len(finding_name),
            "data": finding_name
        }

        group_1_xojakent = []
        group_2_xojakent = []
        group_3_xojakent = []
        for student1 in student_name:
            group1_xojakent = Groups.query.filter_by(id=student1.group1).first()
            group2_xojakent = Groups.query.filter_by(id=student1.group2).first()
            group3_xojakent = Groups.query.filter_by(id=student1.group3).first()
            group_1_xojakent.append(group1_xojakent)
            group_2_xojakent.append(group2_xojakent)
            group_3_xojakent.append(group3_xojakent)

        return render_template('new/search_by_name.html', user=user, group_info1=group_1_xojakent,
                               group_info2=group_2_xojakent, group_info3=group_3_xojakent,
                               search=request.form.get('student').upper(), names=result_name, student_name=student_name)


@app.route('/search_surname', methods=['POST'])
def search_surname():
    user = get_current_user()
    try:
        if not user.director and not user.xojakent_admin:
            return redirect(url_for('nav'))
    except AttributeError:
        return redirect(url_for('nav'))
    if user.xojakent_admin or user.director:
        student_surname = Student.query.filter(Student.director == False, Student.xojakent_admin == False,
                                               Student.gazalkent_admin == False, Student.locations == 1,
                                               Student.chirchiq_admin == False,Student.group1 != None,
                                               Student.surname.ilike("%" + request.form.get('student').upper() + "%"))

        finding_surname = list(map(Student.info, student_surname))
        result_surname = {
            "count": len(finding_surname),
            "data": finding_surname
        }

        group_1_xojakent = []
        group_2_xojakent = []
        group_3_xojakent = []
        for student1 in student_surname:
            group1_xojakent = Groups.query.filter_by(id=student1.group1).first()
            group2_xojakent = Groups.query.filter_by(id=student1.group2).first()
            group3_xojakent = Groups.query.filter_by(id=student1.group3).first()
            group_1_xojakent.append(group1_xojakent)
            group_2_xojakent.append(group2_xojakent)
            group_3_xojakent.append(group3_xojakent)

        return render_template('new/search_by_surname.html', user=user, student_surname=student_surname,
                               search=request.form.get('student').upper(), surnames=result_surname,
                               group_1_xojakent=group_1_xojakent, group_2_xojakent=group_2_xojakent,
                               group_3_xojakent=group_3_xojakent)


@app.route('/search_username', methods=['POST'])
def search_username():
    user = get_current_user()
    try:
        if not user.director and not user.xojakent_admin:
            return redirect(url_for('nav'))
    except AttributeError:
        return redirect(url_for('nav'))
    if user.xojakent_admin or user.director:
        student_username = Student.query.filter(Student.director == False, Student.xojakent_admin == False,
                                                Student.gazalkent_admin == False, Student.locations == 1,
                                                Student.chirchiq_admin == False,Student.group1 != None,
                                                Student.username.ilike("%" + request.form.get('student').upper() + "%"))

        finding_username = list(map(Student.info, student_username))
        result_username = {
            "count": len(finding_username),
            "data": finding_username
        }

        group_1_xojakent = []
        group_2_xojakent = []
        group_3_xojakent = []
        for student1 in student_username:
            group1_xojakent = Groups.query.filter_by(id=student1.group1).first()
            group2_xojakent = Groups.query.filter_by(id=student1.group2).first()
            group3_xojakent = Groups.query.filter_by(id=student1.group3).first()
            group_1_xojakent.append(group1_xojakent)
            group_2_xojakent.append(group2_xojakent)
            group_3_xojakent.append(group3_xojakent)
        return render_template('new/search_by_username.html', user=user, student_username=student_username,
                               search=request.form.get('student').upper(), usernames=result_username,
                               group_1_xojakent=group_1_xojakent, group_2_xojakent=group_2_xojakent,
                               group_3_xojakent=group_3_xojakent)


@app.route('/search_name2', methods=['POST'])
def search_name2():
    user = get_current_user()
    try:
        if not user.gazalkent_admin and not user.director:
            return redirect(url_for('nav'))
    except AttributeError:
        return redirect(url_for('nav'))
    if user.gazalkent_admin or user.director:
        student_name = Student.query.filter(Student.director == False, Student.xojakent_admin == False,
                                            Student.gazalkent_admin == False, Student.locations == 2,
                                            Student.chirchiq_admin == False,Student.group1 != None,
                                            Student.name.ilike("%" + request.form.get('student').upper() + "%"))
        finding_name = list(map(Student.info, student_name))
        result_name = {
            "count": len(finding_name),
            "data": finding_name
        }

        group_1_gazalkent = []
        group_2_gazalkent = []
        group_3_gazalkent = []
        for student2 in student_name:
            group1_gazalkent = Groups.query.filter_by(id=student2.group1).first()
            group2_gazalkent = Groups.query.filter_by(id=student2.group2).first()
            group3_gazalkent = Groups.query.filter_by(id=student2.group3).first()
            group_1_gazalkent.append(group1_gazalkent)
            group_2_gazalkent.append(group2_gazalkent)
            group_3_gazalkent.append(group3_gazalkent)

        return render_template('new/search_by_name2.html', user=user, student_name=student_name,
                               search=request.form.get('student').upper(), names=result_name,
                               group_1_gazalkent=group_1_gazalkent, group_2_gazalkent=group_2_gazalkent,
                               group_3_gazalkent=group_3_gazalkent)


@app.route('/search_surname2', methods=['POST'])
def search_surname2():
    user = get_current_user()
    try:
        if not user.gazalkent_admin and not user.director:
            return redirect(url_for('nav'))
    except AttributeError:
        return redirect(url_for('nav'))
    if user.gazalkent_admin or user.director:
        student_surname = Student.query.filter(Student.director == False, Student.xojakent_admin == False,
                                               Student.gazalkent_admin == False, Student.locations == 2,
                                               Student.chirchiq_admin == False,Student.group1 != None,
                                               Student.surname.ilike("%" + request.form.get('student').upper() + "%"))

        finding_surname = list(map(Student.info, student_surname))
        result_surname = {
            "count": len(finding_surname),
            "data": finding_surname
        }

        group_1_gazalkent = []
        group_2_gazalkent = []
        group_3_gazalkent = []
        for student2 in student_surname:
            group1_gazalkent = Groups.query.filter_by(id=student2.group1).first()
            group2_gazalkent = Groups.query.filter_by(id=student2.group2).first()
            group3_gazalkent = Groups.query.filter_by(id=student2.group3).first()
            group_1_gazalkent.append(group1_gazalkent)
            group_2_gazalkent.append(group2_gazalkent)
            group_3_gazalkent.append(group3_gazalkent)

        return render_template('new/search_by_surname2.html', user=user, student_surname=student_surname,
                               search=request.form.get('student').upper(), surnames=result_surname,
                               group_1_gazalkent=group_1_gazalkent, group_2_gazalkent=group_2_gazalkent,
                               group_3_gazalkent=group_3_gazalkent)


@app.route('/search_username2', methods=['POST'])
def search_username2():
    user = get_current_user()
    try:
        if not user.gazalkent_admin and not user.director:
            return redirect(url_for('nav'))
    except AttributeError:
        return redirect(url_for('nav'))
    if user.gazalkent_admin or user.director:
        student_username = Student.query.filter(Student.director == False, Student.xojakent_admin == False,
                                                Student.gazalkent_admin == False, Student.locations == 2,
                                                Student.chirchiq_admin == False,
                                                Student.username.ilike("%" + request.form.get('student').upper() + "%"))

        finding_username = list(map(Student.info, student_username))
        result_username = {
            "count": len(finding_username),
            "data": finding_username
        }

        group_1_gazalkent = []
        group_2_gazalkent = []
        group_3_gazalkent = []
        for student2 in student_username:
            group1_gazalkent = Groups.query.filter_by(id=student2.group1).first()
            group2_gazalkent = Groups.query.filter_by(id=student2.group2).first()
            group3_gazalkent = Groups.query.filter_by(id=student2.group3).first()
            group_1_gazalkent.append(group1_gazalkent)
            group_2_gazalkent.append(group2_gazalkent)
            group_3_gazalkent.append(group3_gazalkent)

        return render_template('new/search_by_username2.html', user=user, student_username=student_username,
                               search=request.form.get('student').upper(), usernames=result_username,
                               group_1_gazalkent=group_1_gazalkent, group_2_gazalkent=group_2_gazalkent,
                               group_3_gazalkent=group_3_gazalkent)


@app.route('/search_name3', methods=['POST'])
def search_name3():
    user = get_current_user()
    try:
        if not user.chirchiq_admin and not user.director:
            return redirect(url_for('nav'))
    except AttributeError:
        return redirect(url_for('nav'))
    if user.chirchiq_admin or user.director:
        student_name = Student.query.filter(Student.director == False, Student.xojakent_admin == False,
                                            Student.gazalkent_admin == False, Student.locations == 3,
                                            Student.chirchiq_admin == False,Student.group1 != None,
                                            Student.name.ilike("%" + request.form.get('student').upper() + "%"))
        finding_name = list(map(Student.info, student_name))
        result_name = {
            "count": len(finding_name),
            "data": finding_name
        }

        group_1_gazalkent = []
        group_2_gazalkent = []
        group_3_gazalkent = []
        for student2 in student_name:
            group1_gazalkent = Groups.query.filter_by(id=student2.group1).first()
            group2_gazalkent = Groups.query.filter_by(id=student2.group2).first()
            group3_gazalkent = Groups.query.filter_by(id=student2.group3).first()
            group_1_gazalkent.append(group1_gazalkent)
            group_2_gazalkent.append(group2_gazalkent)
            group_3_gazalkent.append(group3_gazalkent)

        return render_template('new/search_by_name2.html', user=user, student_name=student_name,
                               search=request.form.get('student').upper(), names=result_name,
                               group_1_gazalkent=group_1_gazalkent, group_2_gazalkent=group_2_gazalkent,
                               group_3_gazalkent=group_3_gazalkent)


@app.route('/search_surname3', methods=['POST'])
def search_surname3():
    user = get_current_user()
    try:
        if not user.chirchiq_admin and not user.director:
            return redirect(url_for('nav'))
    except AttributeError:
        return redirect(url_for('nav'))
    if user.chirchiq_admin or user.director:
        student_surname = Student.query.filter(Student.director == False, Student.xojakent_admin == False,
                                            Student.gazalkent_admin == False, Student.locations == 3,
                                            Student.chirchiq_admin == False, Student.group1 != None,
                                            Student.surname.ilike("%" + request.form.get('student').upper() + "%"))
        finding_surname = list(map(Student.info, student_surname))
        result_surname = {
            "count": len(finding_surname),
            "data": finding_surname
        }

        group_1_chirchiq = []
        group_2_chirchiq = []
        group_3_chirchiq = []
        for student2 in student_surname:
            group1_chirchiq = Groups.query.filter_by(id=student2.group1).first()
            group2_chirchiq = Groups.query.filter_by(id=student2.group2).first()
            group3_chirchiq = Groups.query.filter_by(id=student2.group3).first()
            group_1_chirchiq.append(group1_chirchiq)
            group_2_chirchiq.append(group2_chirchiq)
            group_3_chirchiq.append(group3_chirchiq)

        return render_template('new/search_by_surname3.html', user=user, student_surname=student_surname,
                               search=request.form.get('student').upper(),surnames=result_surname,
                               group_1_chirchiq=group_1_chirchiq, group_2_chirchiq=group_2_chirchiq,
                               group_3_chirchiq=group_3_chirchiq)


@app.route('/search_username3', methods=['POST'])
def search_username3():
    user = get_current_user()
    try:
        if not user.chirchiq_admin and not user.director:
            return redirect(url_for('nav'))
    except AttributeError:
        return redirect(url_for('nav'))
    if user.chirchiq_admin or user.director:
        student_username = Student.query.filter(Student.director == False, Student.xojakent_admin == False,
                                            Student.gazalkent_admin == False, Student.locations == 3,
                                            Student.chirchiq_admin == False, Student.group1 != None,
                                            Student.username.ilike("%" + request.form.get('student').upper() + "%"))
        finding_username = list(map(Student.info, student_username))
        result_username = {
            "count": len(finding_username),
            "data": finding_username
        }

        group_1_chirchiq = []
        group_2_chirchiq = []
        group_3_chirchiq = []
        for student2 in student_username:
            group1_chirchiq = Groups.query.filter_by(id=student2.group1).first()
            group2_chirchiq = Groups.query.filter_by(id=student2.group2).first()
            group3_chirchiq = Groups.query.filter_by(id=student2.group3).first()
            group_1_chirchiq.append(group1_chirchiq)
            group_2_chirchiq.append(group2_chirchiq)
            group_3_chirchiq.append(group3_chirchiq)

        return render_template('new/search_by_username3.html', user=user, student_username=student_username,
                               search=request.form.get('student').upper(),usernames=result_username,
                               group_1_chirchiq=group_1_chirchiq, group_2_chirchiq=group_2_chirchiq,
                               group_3_chirchiq=group_3_chirchiq)


@app.route('/student_info/<int:student_id>')
def student_info(student_id):
    form = PhotoForm(meta={'csrf': False})
    user = get_current_user()
    try:
        if not user.xojakent_admin and not user.director and not user.gazalkent_admin and not user.chirchiq_admin:
            return redirect(url_for('nav'))
    except AttributeError:
        return redirect(url_for('nav'))
    student = Student.query.filter_by(id=student_id).first()
    info1 = Shartnoma.query.filter_by(student_id=student_id).first()
    group_name1 = Groups.query.filter_by(id=student.group1).first()
    group_name2 = Groups.query.filter_by(id=student.group2).first()
    group_name3 = Groups.query.filter_by(id=student.group3).first()
    for_group1 = Student.query.filter(or_(Student.group1 == student.group1, Student.group2 == student.group1,
                                          Student.group3 == student.group1)).all()
    result1 = len(for_group1)
    for_group2 = Student.query.filter(or_(Student.group1 == student.group2, Student.group2 == student.group2,
                                          Student.group3 == student.group2)).all()
    result2 = len(for_group2)
    for_group3 = Student.query.filter(or_(Student.group1 == student.group3, Student.group2 == student.group3,
                                          Student.group3 == student.group3)).all()
    result3 = len(for_group3)
    teacher_1 = []
    teacher_2 = []
    teacher_3 = []
    if group_name1:
        teacher = Teachers.query.filter(Teachers.id == group_name1.teacher_1).first()
        teacher_1.append(teacher)
    if group_name2:
        teacher2 = Teachers.query.filter(Teachers.id == group_name2.teacher_1).first()
        teacher_2.append(teacher2)
    if group_name3:
        teacher3 = Teachers.query.filter(Teachers.id == group_name3.teacher_1).first()
        teacher_3.append(teacher3)
    shartnoma = Shartnoma.query.filter_by(student_id=student_id).first()
    return render_template('new/student_info.html', user=user, student=student,teacher=teacher_1,teacher_2=teacher_2,
                           group_name1=group_name1, group_name2=group_name2, group_name3=group_name3,result1=result1,
                           student_id=student_id, info1=info1, form=form,result2=result2,result3=result3,
                           teacher_3=teacher_3,shartnoma=shartnoma)


@app.route('/withdrawal', methods=['POST'])
def withdrawal():
    user = get_current_user()
    try:
        if not user.gazalkent_admin and not user.chirchiq_admin and not user.xojakent_admin:
            return redirect(url_for('nav'))
    except AttributeError:
        return redirect(url_for('nav'))
    if request.method == "POST":
        who = request.form.get('who')
        why = request.form.get('why')
        sum = int(request.form.get('amount'))
        if user.xojakent_admin:
            add = Withdrawal(who=who, why=why, amount=sum, date=now, locations='xojakent')
            db.session.add(add)
            db.session.commit()
        elif user.gazalkent_admin:
            add2 = Withdrawal(who=who, why=why, amount=sum, date=now, locations='gazalkent')
            db.session.add(add2)
            db.session.commit()
        elif user.chirchiq_admin:
            add3 = Withdrawal(who=who, why=why, amount=sum, date=now, locations='chirchiq')
            db.session.add(add3)
            db.session.commit()
        flash('Данные успешно добавлены')
        return redirect(url_for('payment'))
