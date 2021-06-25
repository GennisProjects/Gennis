from app import db, Integer, Column, String, Boolean, ForeignKey,DateTime


class Home(db.Model):
    id = Column(Integer,primary_key=True)
    news_1_image = Column(String)
    news_2_image = Column(String)
    news_3_image = Column(String)
    news_1_description = Column(String)
    news_2_description = Column(String)
    news_3_description = Column(String)
    subject_1_image = Column(String)
    subject_2_image = Column(String)
    subject_3_image = Column(String)
    subject_4_image = Column(String)
    subject_5_image = Column(String)
    subject_6_image = Column(String)
    subject_7_image = Column(String)
    subject_8_image = Column(String)
    subject_1_description = Column(String)
    subject_2_description = Column(String)
    subject_3_description = Column(String)
    subject_4_description = Column(String)
    subject_5_description = Column(String)
    subject_6_description = Column(String)
    subject_7_description = Column(String)
    subject_8_description = Column(String)


class Coments(db.Model):
    id = Column(Integer, primary_key=True)
    teacher_id = Column(Integer)
    comment = Column(String)
    education_centre = Column(Integer)
    user_id = Column(Integer)


class ReasonAbsentDays(db.Model):
    tablename = 'Reason'
    id = Column(Integer,primary_key=True)
    img_due_days = Column(String,nullable=False)
    reason_due = Column(String(),nullable=False)
    student_id = Column(Integer,nullable=False)
    date_abset = Column(DateTime,nullable=False)
    group_id = Column(Integer,nullable=False)
    student_locations = Column(Integer)

    def delete(self):
        db.session.delete(self)
        db.session.commit()


class due_days(db.Model):
    id = Column(Integer, primary_key=True)
    img_due_days = Column(String, nullable=False)
    group_id_student = Column(Integer,nullable=False)
    id_of_student = Column(Integer,nullable=False)
    date_of_absent = Column(DateTime,nullable=False)
    reason_due = Column(String(), nullable=False)


class Capital_expenditure(db.Model):
    id = Column(Integer,primary_key=True)
    item = Column(String)
    number_items = Column(Integer)
    amount_item = Column(Integer)
    bought_data = Column(DateTime)
    locations = Column(String)


class Withdrawal(db.Model):
    id = Column(Integer,primary_key=True)
    who = Column(String)
    why = Column(String)
    amount = Column(Integer)
    date = Column(DateTime)
    locations = Column(String)


class Overhead(db.Model):
    id = Column(Integer,primary_key=True)
    reason = Column(String)
    quantity = Column(String)
    sum = Column(Integer)
    payed_data = Column(DateTime)
    locations = Column(String)


class All_Charity_Sums(db.Model):
    id = Column(Integer,primary_key=True)
    bank_charity = Column(Integer)


class Student(db.Model):
    id = Column(Integer, primary_key=True)
    xojakent_admin = Column(Boolean)
    gazalkent_admin = Column(Boolean)
    chirchiq_admin = Column(Boolean,default=False)
    methodist = Column(Boolean)
    name = Column(String)
    surname = Column(String)
    born_day = Column(Integer)
    born_month = Column(Integer)
    age = Column(Integer)
    year_born = Column(Integer)
    username = Column(String)
    phone = Column(String)
    parent_phone = Column(String)
    password = Column(String)
    director = Column(Boolean)
    subject_1 = Column(String)
    subject_2 = Column(String)
    subject_3 = Column(String)
    for_group = Column(Boolean, default=False)
    group1 = Column(Integer)
    group2 = Column(Integer)
    group3 = Column(Integer)
    locations = Column(Integer, ForeignKey('Locations.id'))
    money = Column(Integer())
    attendance = Column(Boolean,default=False)
    charity = Column(Integer)
    photo = Column(String)
    otasining_ismi = Column(String)
    for_moved = Column(Boolean,default=False)
    join_data = Column(DateTime)
    ball_time = Column(DateTime)
    vakilning_ismi = Column(String)
    vakilning_familyasi = Column(String)
    vakilning_telefon_raqami = Column(String)
    vakilning_otchestvasi = Column(String)
    contract_image = Column(String)
    comment = Column(String)

    def info(self):
        return {
            "id": self.id,
            "name": self.name,
            "surname": self.surname,
            "username": self.username,
            "locations": self.locations,
            "xojakent_admin": self.xojakent_admin,
            "gazalkent_admin": self.gazalkent_admin,
            "chirchiq_admin":self.chirchiq_admin,
            "director": self.director,
            "money": self.money,
            "photo": self.phone,
            'vakilning_ismi':self.vakilning_ismi,
            'vakilning_familyasi':self.vakilning_familyasi,
            'vakilning_telefon_raqami':self.vakilning_telefon_raqami
        }

    def add(self):
        db.session.add(self)
        db.session.commit()

    def init(self,name,surname,age,username,for_group,phone,password,subject_1,subject_2,subject_3,locations,xojakent_admin,
             gazalkent_admin,director,charity,image):
        self.name = name
        self.surname = surname
        self.age = age
        self.username = username
        self.phone = phone
        self.for_group = for_group
        self.password = password
        self.subject_1 = subject_1
        self.subject_2 = subject_2
        self.subject_3 = subject_3
        self.locations = locations
        self.xojakent_admin = xojakent_admin
        self.gazalkent_admin = gazalkent_admin
        self.director = director
        self.charity = charity

    def delete(self):
        db.session.delete(self)
        db.session.commit()

    def format(self, name, surname, age, gmail, phone, password, subject_1,subject_2,subject_3, locations,xojakent_admin,gazalkent_admin,director):
        return {
            'name': name,
            'surname': surname,
            'age': age,
            'gmail': gmail,
            'phone': phone,
            'password': password,
            'subject_1': subject_1,
            'subject_2': subject_2,
            'subject_3': subject_3,
            'locations': locations,
            'xojakent_admin': xojakent_admin,
            'gazalkent_admin': gazalkent_admin,
            'director' : director
        }


class Attendance(db.Model):
    tablename = 'Attendance'
    id = Column(Integer,primary_key=True)
    group_id = Column(Integer, nullable=False)
    student_id = Column(Integer,nullable=False)
    teacher_id = Column(Integer, nullable=False)
    present = Column(DateTime)
    apset = Column(DateTime())
    darsga_tayyorgarligi = Column(Integer)
    lugat = Column(Integer)
    darsda_qatnashishi = Column(Integer)
    ortacha_baho = Column(Integer)
    fan = Column(String)
    for_sabab = Column(Boolean,default=False)
    student_name = Column(String)
    student_surname = Column(String)
    student_username = Column(String)
    test_delete = Column(String)

    def delete(self):
        db.session.delete(self)
        db.session.commit()

    def add_attendance(self):
        db.session.add(self)
        db.session.commit()

    def init(self,group_id,student_id,teacher_id, present,apset):
        self.group_id = group_id
        self.student_id = student_id
        self.teacher_id = teacher_id
        self.present = present
        self.apset = apset

    def update(self):
        db.session.commit()


class Locations(db.Model):
    __tablename__ = 'Locations'
    id = Column(Integer, primary_key=True)
    loc = Column(String, nullable=False)


class Teachers(db.Model):
    __tablename__ = 'Teachers'
    id = Column(Integer,primary_key=True)
    teacher = Column(Boolean)
    name = Column(String(),nullable=False)
    surname = Column(String(),nullable=False)
    phone = Column(String,nullable=False)
    password = Column(String,nullable=False)
    age = Column(String, nullable=False)
    year_born = Column(Integer)
    month_born = Column(Integer)
    day_born = Column(Integer)
    username = Column(String(), nullable=False)
    locations = Column(Integer, ForeignKey('Locations.id'), nullable=False)
    subject = Column(String(),nullable=False)
    for_group = Column(Boolean,default=False)
    otasining_ismi = Column(String)
    salary = Column(Integer)
    salary_for_gazalkent = Column(Integer)
    salary_for_chirchiq = Column(Integer)
    group1 = Column(Integer)
    group2 = Column(Integer)
    group3 = Column(Integer)
    group4 = Column(Integer)
    group5 = Column(Integer)
    group6 = Column(Integer)
    group7 = Column(Integer)
    group8 = Column(Integer)
    group9 = Column(Integer)
    group10 = Column(Integer)
    photo = Column(String)

    def add_teacher(self):
        db.session.add(self)
        db.session.commit()

    def init(self, name, surname, age, username, phone, password, subject, locations,
             teacher):
        self.name = name
        self.surname = surname
        self.age = age
        self.username = username
        self.phone = phone
        self.password = password
        self.subject = subject
        self.locations = locations
        self.teacher = teacher

    def info(self):
        return {
            "id": self.id,
            "name": self.name,
            "surname": self.surname,
            "username": self.username,
            "salary": self.salary,
            "phone": self.phone,
            "subject": self.subject,
            "photo":self.photo
        }

    def format_teacher(self, name, Surname, age, gmail, phone, password, subject, locations,xojakent_admin,gazalkent_admin,director,teacher):
        return {
            'name': name,
            'Surname': Surname,
            'age': age,
            'gmail': gmail,
            'phone': phone,
            'password': password,
            'subjects': subject,
            'locations': locations,
            'xojakent_admin': xojakent_admin,
            'gazalkent_admin': gazalkent_admin,
            'director': director,
            'teacher': teacher
        }

    def delete(self):
        db.session.delete(self)
        db.session.commit()


class Student_cash(db.Model):
    id = Column(Integer, primary_key=True)
    student_id = Column(Integer)
    student_name = Column(String)
    student_surname = Column(String)
    username = Column(String)
    debt = Column(Integer)
    payment = Column(Integer)
    result = Column(Integer)
    payment_data = Column(DateTime)
    locations = Column(String)

    def add(self):
        db.session.add(self)
        db.session.commit()


class Teacher_cash(db.Model):
    id = Column(Integer, primary_key=True)
    teacher_id = Column(Integer)
    teacher_name = Column(String)
    teacher_surname = Column(String)
    username = Column(String)
    salary = Column(Integer)
    payment = Column(Integer)
    result = Column(Integer)
    payment_data = Column(DateTime)
    locations = Column(String)


class Groups(db.Model):
    __tablename__ = 'Groups'
    id = Column(Integer,primary_key=True)
    name = Column(String(),nullable=False)
    old_name = Column(String)
    teacher_1 = Column(Integer, nullable=False)
    subject = Column(String)
    cost = Column(Integer)
    location = Column(Integer)
    teacher_name = Column(String)
    teacher_surname = Column(String)
    type_of_course = Column(String)

    def add_group(self):
        db.session.add(self)
        db.session.commit()

    def add_teacher(self):
        db.session.add(self)
        db.session.commit()

    def delete(self):
        db.session.delete(self)
        db.session.commit()

    def info(self):
        return {
            'id': self.id,
            'name': self.name,
            'location': self.location,
            'teacher_name': self.teacher_name,
            'type_of_course': self.type_of_course,
            'subject': self.subject,
            'teacher_surname': self.teacher_surname,
            'teacher_1':self.teacher_1,
            'cost': self.cost
        }

    def init(self,name,teacher_1, student1):
        self.name = name
        self.student1 = student1
        self.teacher_1 = teacher_1

    def format_teacher(self, name, location, teacher_1):
        return {
            'name': name,

            'location': location,


            'teacher_1': teacher_1
        }


class Deleted_students(db.Model):
    id = Column(Integer,primary_key=True)
    reason = Column(String)
    student_id = Column(Integer)
    student_name = Column(String)
    student_surname = Column(String)
    student_phone = Column(String)
    student_parent_phone = Column(Integer)

    def init(self,reason,student_id,student_name,student_surname,student_phone,student_parent_phone):
        self.reason = reason
        self.student_id=student_id
        self.student_name=student_name
        self.student_parent_phone = student_parent_phone
        self.student_phone = student_phone
        self.student_surname = student_surname

    def format(self, reason, student_surname, student_phone, student_parent_phone, student_name, student_id):
        return {
            'reason': reason,
            'student_surname': student_surname,
            'student_phone': student_phone,
            'student_parent_phone': student_parent_phone,
            'student_name': student_name,
            'student_id': student_id,

        }


class Lessons(db.Model):
    __tablename__ = "Lessons"
    id = Column(Integer,primary_key=True)
    lesson_number = Column(Integer)
    title = Column(String)
    video_link = Column(String)

    def insert(self):
        db.session.add(self)
        db.session.commit()

    def delete(self):
        db.session.delete(self)
        db.session.commit()


class MCHQ(db.Model):
    id = Column(Integer,primary_key=True)
    lesson_number = Column(Integer,db.ForeignKey(Lessons.id))
    question_text = Column(String)
    exercise_description = Column(String)
    answer = Column(String)
    a = Column(String)
    b = Column(String)
    c = Column(String)
    d = Column(String)
    ques_inputs = Column(Integer)
    video_link = Column(String)

    def insert(self):
        db.session.add(self)
        db.session.commit()

    def delete(self):
        db.session.delete(self)
        db.session.commit()


class GapFilling(db.Model):
    id = Column(Integer,primary_key=True)
    lesson_number = Column(Integer, db.ForeignKey(Lessons.id))
    question_text = Column(String)
    exercise_description = Column(String)
    answer = Column(String)
    video_link = Column(String)

    def insert(self):
        db.session.add(self)
        db.session.commit()

    def delete(self):
        db.session.delete(self)
        db.session.commit()


class ConfusingWords(db.Model):
    id = Column(Integer,primary_key=True)
    lesson_number = Column(Integer, db.ForeignKey(Lessons.id))
    question_text = Column(String)
    exercise_description = Column(String)
    answer = Column(String)
    number_inputs = Column(Integer)
    video_link = Column(String)

    def insert(self):
        db.session.add(self)
        db.session.commit()

    def delete(self):
        db.session.delete(self)
        db.session.commit()


class Shartnoma(db.Model):
    id = Column(Integer,primary_key=True)
    student_id = Column(Integer)
    ot = Column(String)
    do = Column(String)

    def info(self):
        return {
            "id":self.id,
            "student_id":self.student_id,
            "ot":self.ot,
            "do":self.do
        }

    def insert(self):
        db.session.add(self)
        db.session.commit()

    def delete(self):
        db.session.delete(self)
        db.session.commit()

