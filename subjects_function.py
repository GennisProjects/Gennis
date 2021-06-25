from app import app, render_template, redirect, request, url_for, \
    session, get_current_user, db, get_current_teacher,PhotoForm,images
from models import Student, Teachers,All_Charity_Sums, Locations, Coments,Home, GapFilling, Lessons, MCHQ, ConfusingWords
from werkzeug.security import generate_password_hash, check_password_hash
from datetime import datetime
import json


@app.route('/list_of_subjects')
def list_subjects():
    user = get_current_user()
    teacher = get_current_teacher()
    return render_template('subjects/list_of_subjects.html', user=user, teacher=teacher)


@app.route('/English_subject')
def english():
    user = get_current_user()
    teacher = get_current_teacher()
    return render_template('subjects/English.html', user=user, teacher=teacher)


@app.route('/gram_eng', methods=['POST'])
def gram_eng():
    id_lesson = request.form.get('id_lesson')
    title_lesson = request.form.get('title_lesson')
    video_link = request.form.get('video_link')
    lesson = Lessons(lesson_number=id_lesson,title=title_lesson,video_link=video_link)
    db.session.add(lesson)
    ex_video1 = request.form.get('ex_video1')
    ex_video2 = request.form.get('ex_video2')
    ex_video3 = request.form.get('ex_video3')
    ex_video4 = request.form.get('ex_video4')
    ex_video5 = request.form.get('ex_video5')
    # Gap Fill
    gap_fill_description = request.form.get('gap_fill_description')
    question_text_gap_filling = request.form.getlist('question_text_gap_filling')
    answer_gap_filling = request.form.getlist('answer_gap_filling')
    for gap,answer_gap in zip(question_text_gap_filling,answer_gap_filling):
        add = GapFilling(lesson_number=id_lesson,question_text=gap,answer=answer_gap,
                         exercise_description=gap_fill_description,video_link=ex_video1)
        db.session.add(add)

    #Matching
    matching_description = request.form.get('matching_description')
    matching_question_text = request.form.get('matching_question_text')
    matching_answer = request.form.get('matching_answer')
    for match,answer_match in zip(matching_question_text,matching_answer):

        add2 = MCHQ(lesson_number=id_lesson,exercise_description=matching_description,answer=answer_match,
                    question_text=match,video_link=ex_video2)
        db.session.add(add2)
    #
    #
    # # Multiple_choice_questions
    # mchq_description = request.form.get('mchq_description')
    # mchq_question_text = request.form.get('mchq_question_text')
    # answer_mchq = request.form.get('answer_mchq')
    # a = request.form.get('a')
    # b = request.form.get('b')
    # c = request.form.get('c')
    # d = request.form.get('d')
    # for (mchq_ques,mchq_ans,a_variant,b_variant,c_variant,d_variant) in (mchq_question_text,answer_mchq,a,b,c,d):
    #     add3 = MCHQ(question_text=mchq_ques,answer=mchq_ans,a=a_variant,b=b_variant,c=c_variant,d=d_variant,
    #                 lesson_number=id_lesson,video_link=ex_video3)
    #     db.session.add(add3)
    # confuse_word
    confuse_word_description = request.form.get('confuse_word_description')
    question_text_confuse = request.form.get('question_text_confuse')
    answer_confuse = request.form.get('answer_confuse')
    # print('Lesson',id_lesson,title_lesson,video_link)
    # print('Gapfilling',ex_video1,gap_fill_description,question_text_gap_filling,answer_gap_filling)
    # print('Matching',ex_video2,matching_description,matching_question_text,matching_answer)
    # print('MCHQ',ex_video3,mchq_description,mchq_question_text,answer_mchq,a,b,c,d)
    # print('Confuse',ex_video4,confuse_word_description,question_text_confuse,answer_confuse)
    db.session.commit()
    return redirect(url_for('english'))
