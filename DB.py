from flask import Flask, render_template, request, redirect, url_for, flash
from werkzeug.utils import secure_filename
import pymysql
import os
import sys
import importlib
import random
from datetime import datetime


importlib.reload(sys)

app = Flask(__name__)

# 全局变量
username = ""
# TODO: username变量的赋值  方法1：全局变量实现，随登录进行修改  方法2：给每个页面传递username
userRole = ""
notFinishedNum = 0
# 上传文件要储存的目录
UPLOAD_FOLDER = '/static/images/'
# 允许上传的文件扩展名的集合
ALLOWED_EXTENSIONS = set(['png', 'jpg', 'jpeg'])


def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1] in ALLOWED_EXTENSIONS


@app.route('/')
@app.route('/index')
# 首页
def indexpage():
    return render_template('index.html')

# 登录
@app.route('/logIn', methods=['GET', 'POST'])
def logInPage():
    global username
    global userRole
    msg = ""
    if request.method == 'GET':
        return render_template('logIn.html')
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        userRole = request.form.get('userRole')
        print(userRole)
        print(username)

        db = pymysql.connect("localhost", "root", password="20000106", db="Hospital", charset='utf8')

        if userRole == 'doctor':
            cursor = db.cursor()
            try:
                cursor.execute("use Hospital")
            except:
                print("Error: unable to use database!")
            sql = "SELECT * from doctor where d_id = '{}' and password='{}'".format(username, password)
            cursor.execute(sql)
            db.commit()
            res = cursor.fetchall()
            num = 0
            for row in res:
                num = num + 1
            # 如果存在该医生且密码正确
            if num == 1:
                print("登录成功！！")
                msg = "done1"
            else:
                print("您没有主治医生用户权限或登陆信息出错。")
                msg = "fail1"
            return render_template('logIn.html', messages=msg, username=username, userRole=userRole)

        elif userRole == 'head_nurse':
            cursor = db.cursor()
            try:
                cursor.execute("use Hospital")
            except:
                print("Error: unable to use database!")
            sql = "SELECT * from head_nurse where hn_id = '{}' and password='{}'".format(username, password)
            cursor.execute(sql)
            db.commit()
            res = cursor.fetchall()
            num = 0
            for row in res:
                num = num + 1
            # 如果存在该护士长且密码正确
            if num == 1:
                print("登录成功！")
                msg = "done2"
            else:
                print("您没有护士长用户权限或登录信息出错。")
                msg = "fail2"
            return render_template('logIn.html', messages=msg, username=username, userRole=userRole)

        elif userRole == 'ward_nurse':
            cursor = db.cursor()
            try:
                cursor.execute("use Hospital")
            except:
                print("Error: unable to use database!")
            sql = "SELECT * from ward_nurse where wn_id = '{}' and password='{}'".format(username, password)
            cursor.execute(sql)
            db.commit()
            res = cursor.fetchall()
            num = 0
            for row in res:
                num = num + 1
            # 如果存在该用户且密码正确
            if num == 1:
                print("登录成功！")
                msg = "done3"
            else:
                print("您没有病房护士权限或登录信息出错。")
                msg = "fail3"
            return render_template('logIn.html', messages=msg, username=username, userRole=userRole)

        elif userRole == 'emergency_nurse':
            cursor = db.cursor()
            try:
                cursor.execute("use Hospital")
            except:
                print("Error: unable to use database!")
            sql = "SELECT * from emergency_nurse where en_id = '{}' and password='{}'".format(username, password)
            cursor.execute(sql)
            db.commit()
            res = cursor.fetchall()
            num = 0
            for row in res:
                num = num + 1
            # 如果存在该护士且密码正确
            if num == 1:
                print("登录成功！")
                msg = "done4"
            else:
                print("您没有急诊护士权限或登录信息出错。")
                msg = "fail4"
            return render_template('logIn.html', messages=msg, username=username, userRole=userRole)

@app.errorhandler(404)
def page_not_found(error):
    return render_template("404.html"), 404

# 个人中心页面
@app.route('/d')
def dPage():
    return render_template('d.html')

@app.route('/hn')
def hnPage():
    return render_template('hn.html')

@app.route('/wn')
def wnPage():
    return render_template('wn.html')

@app.route('/en')
def enPage():
    return render_template('en.html')

# 修改个人信息页面
@app.route('/ModifyPersonalInfo', methods=['GET', 'POST'])
def ModifyPersonalInfo():
    msg = ""
    if request.method == 'GET':
        return render_template('ModifyPersonalInfo.html', username=username)
    if request.method == 'POST':
        # username = request.form['username']
        phonenum = request.form['phonenum']
        # 连接数据库，默认数据库用户名root，密码空
        db = pymysql.connect("localhost", "root", password="20000106", db="Hospital", charset='utf8')
        cursor = db.cursor()
        try:
            cursor.execute("use Hospital")
        except:
            print("Error: unable to use database!")
        if userRole == 'doctor':
            sql = "Update {} SET contact_info = '{}' where d_id = '{}'".format(userRole, phonenum,
                                                                                        username)
        elif userRole == 'head_nurse':
            sql = "Update {} SET contact_info = '{}' where hn_id = '{}'".format(userRole, phonenum,
                                                                               username)
        elif userRole == 'ward_nurse':
            sql = "Update {} SET contact_info = '{}' where wn_id = '{}'".format(userRole, phonenum,
                                                                               username)
        elif userRole == 'emergency_nurse':
            sql = "Update {} SET contact_info = '{}' where en_id = '{}'".format(userRole, phonenum,
                                                                              username)
        try:
            cursor.execute(sql)
            db.commit()
            # print("修改个人信息成功")
            msg = "done"
        except ValueError as e:
            print("--->", e)
            print("修改个人信息失败")
            msg = "fail"
        return render_template('ModifyPersonalInfo.html', messages=msg, username=username, userRole=userRole)


# 修改密码页面
@app.route('/ModifyPassword', methods=['GET', 'POST'])
def ModifyPassword():
    msg = ""
    if request.method == 'GET':
        return render_template('ModifyPassword.html', username=username, userRole=userRole)
    if request.method == 'POST':
        # username = request.form['username']
        psw1 = request.form['psw1']
        psw2 = request.form['psw2']
        # 两次输入密码是否相同
        if psw1 == psw2:
            db = pymysql.connect("localhost", "root", password="20000106", db="Hospital", charset='utf8')
            cursor = db.cursor()
            try:
                cursor.execute("use Hospital")
            except:
                print("Error: unable to use database!")
            if userRole == 'doctor':
                sql = "Update {} SET password = '{}' where d_id = '{}'".format(userRole, psw1,
                                                                                   username)
            elif userRole == 'head_nurse':
                sql = "Update {} SET password = '{}' where hn_id = '{}'".format(userRole, psw1,
                                                                                    username)
            elif userRole == 'ward_nurse':
                sql = "Update {} SET password = '{}' where wn_id = '{}'".format(userRole, psw1,
                                                                                    username)
            elif userRole == 'emergency_nurse':
                sql = "Update {} SET password = '{}' where en_id = '{}'".format(userRole, psw1,
                                                                                    username)
            try:
                cursor.execute(sql)
                db.commit()
                # print("修改密码成功")
                msg = "done"
            except ValueError as e:
                print("--->", e)
                print("修改密码失败")
                msg = "fail"
            return render_template('ModifyPassword.html', messages=msg, username=username, userRole=userRole)
        else:
            msg = "not equal"
            return render_template('ModifyPassword.html', messages=msg, username=username, userRole=userRole)

# 医生查看护士信息
@app.route('/d_viewn', methods=['GET', 'POST'])
def d_viewn():
    msg = ""
    if request.method == 'GET':
        return render_template('d_viewn.html')
    if request.method == 'POST':
        checkRole = request.form.get('checkRole')
        print(checkRole)
        return render_template('d_viewn.html', messages=checkRole, username=username, userRole=userRole)

@app.route('/d_viewhn')
def d_viewhn():
    msg = ''
    db = pymysql.connect("localhost", "root", password="20000106", db="Hospital", charset='utf8')
    cursor = db.cursor()
    try:
        cursor.execute("use Hospital")
    except:
        print("Error: unable to use database!")
    # 查询
    sql = "SELECT * FROM head_nurse as hn WHERE hn.hn_id = (SELECT distinct hn_id FROM location as l WHERE (l.d_id =  '%s'))" % username
    cursor.execute(sql)
    res = cursor.fetchall()
    if len(res) != 0:
        msg = "done"
        print(msg)
        print(len(res))
        return render_template('d_viewhn.html', username=username, result=res, messages=msg,
                               userRole=userRole)
    else:
        print("NULL")
        msg = "none"
        return render_template('d_viewhn.html', username=username, messages=msg, userRole=userRole)
    return render_template('d_viewhn.html')

@app.route('/d_viewwn')
def d_viewwn():
    msg = ''
    db = pymysql.connect("localhost", "root", password="20000106", db="Hospital", charset='utf8')
    cursor = db.cursor()
    try:
        cursor.execute("use Hospital")
    except:
        print("Error: unable to use database!")
    # 查询
    sql = "SELECT * FROM ward_nurse as wn WHERE wn.wn_id = some(SELECT distinct wn_id FROM location as l WHERE (l.d_id =  '%s'))" % username
    cursor.execute(sql)
    res = cursor.fetchall()

    if len(res) != 0:
        msg = "done"
        print(msg)
        print(len(res))
        sql2 = "SELECT l.wn_id, l.bed_no,l.room_no FROM location as l WHERE l.d_id = '%s' and l.wn_id is not null" % username
        cursor.execute(sql2)
        res2 = cursor.fetchall()
        res_final = []
        for i in res:
            aNew = list(i)
            a =""
            for j in res2:
                if i[0] == j[0]:
                   a += "房间"+str(j[2])+"床位"+str(j[1])+" "
            aNew.append(a)
            res_final.append(aNew)
        return render_template('d_viewwn.html', username=username, result=res_final, messages=msg,
                               userRole=userRole)
    else:
        print("NULL")
        msg = "none"
        return render_template('d_viewwn.html', username=username, messages=msg, userRole=userRole)
    return render_template('d_viewwn.html')

@app.route('/d_viewen')
def d_viewen():
    msg = ''
    db = pymysql.connect("localhost", "root", password="20000106", db="Hospital", charset='utf8')
    cursor = db.cursor()
    try:
        cursor.execute("use Hospital")
    except:
        print("Error: unable to use database!")
    # 查询
    sql = "SELECT * FROM emergency_nurse"
    cursor.execute(sql)
    res = cursor.fetchall()
    if len(res) != 0:
        msg = "done"
        print(msg)
        print(len(res))
        return render_template('d_viewen.html', username=username, result=res, messages=msg,
                               userRole=userRole)
    else:
        print("NULL")
        msg = "none"
        return render_template('d_viewen.html', username=username, messages=msg, userRole=userRole)
    return render_template('d_viewen.html')


@app.route('/d_recoverp', methods=['GET', 'POST'])
def d_recoverp():

    msg = ""
    if request.method == 'GET':
        db = pymysql.connect("localhost", "root", password="20000106", db="Hospital", charset='utf8')
        cursor = db.cursor()
        try:
            cursor.execute("use Hospital")
        except:
            print("Error: unable to use database!")
        sql4 = "SELECT distinct area FROM location WHERE location.d_id = '%s'" % username
        cursor.execute(sql4)
        db.commit()
        res = cursor.fetchall()
        print(res[0])
        if res[0][0] != '1':
            msg = 'none'
            return render_template('d_recoverp.html', messages=msg, username=username)
        sql3 = "SELECT distinct area FROM location WHERE location.d_id = '%s'" % username
        cursor.execute(sql3)
        db.commit()
        res = cursor.fetchall()
        print(res[0])
        if res[0][0] != '1':
            msg = 'none'
            return render_template('d_recoverp.html', messages=msg, username=username)
        # 检验3天体温和2次核酸
        # for loop 找pid
        sql9 = "SELECT * FROM patient"
        cursor.execute(sql9)
        db.commit()
        print("查询成功")
        all_p_id = cursor.fetchall()
        the_list = []
        for p_id in all_p_id:

            sql1 = "SELECT temperature FROM daily_info WHERE daily_info.p_id = %s  ORDER BY the_date DESC" % p_id[0]
            cursor.execute(sql1)
            db.commit()
            print("查询成功")
            res = cursor.fetchall()
            print(res)
            good = 0
            counter = 0
            if len(res) < 3:
                continue
            for i in res:
                if counter > 2:
                    break
                counter += 1
                if i[0] < '37.3':
                    good += 1
            if good != 3:
                continue
            sql2 = "SELECT result FROM covid_test WHERE covid_test.p_id = '%s'  ORDER BY the_date DESC" % p_id[0]
            cursor.execute(sql2)
            db.commit()
            print("查询成功2")
            res = cursor.fetchall()
            print(res)
            good = 0
            counter = 0
            if len(res) < 2:
                continue
            for i in res:
                if counter > 1:
                    break
                counter += 1
                if not i[0]:
                    good += 1
            if good != 2:
                continue
            the_list.append(p_id)
        if len(the_list) != 0:
            msg = "done"
            print(msg)
            print(len(the_list))
            return render_template('d_recoverp.html', username=username, result=the_list, messages=msg,
                                   userRole=userRole)
        else:
            print("NULL")
            msg = "none"
            return render_template('d_recoverp.html', username=username, messages=msg, userRole=userRole)
    elif request.form["action"] == "出院":
        # 执行出院康复操作
        db = pymysql.connect("localhost", "root", password="20000106", db="Hospital", charset='utf8')
        cursor = db.cursor()
        try:
            cursor.execute("use Hospital")
        except:
            print("Error: unable to use database!")
        p_id = request.form['p_id']
        sql = "UPDATE patient as p SET p.life_state = '康复出院' WHERE p_id = '%s'" % (p_id)
        print(sql)
        cursor.execute(sql)
        db.commit()
        msg = 'done2'
        # 查找隔离区病人
        sql3 = "SELECT * FROM patient WHERE patient.p_id = some(SELECT p_id FROM location WHERE location.area = 0) and patient.severity = '轻症'"
        cursor.execute(sql3)
        db.commit()
        res = cursor.fetchall()

        if len(res) == 0:
            # 无隔离区等候，开始搜索另外两个区域
            sql6 = "SELECT * FROM patient WHERE patient.p_id = some(SELECT p_id FROM location WHERE location.area != 1 and location.area != 0) and patient.severity = '轻症'"
            cursor.execute(sql6)
            db.commit()
            res = cursor.fetchall()
            if len(res) == 0:
                # 无适合患者
                sql5 = "UPDATE location as l SET l.p_id = NULL, l.wn_id = NULL  WHERE l.p_id = '%s'" % p_id
                cursor.execute(sql5)
                db.commit()
                return render_template('d_recoverp.html', messages=msg, username=username)
            else:
                # 找到第一个轻症患者安排进相同病房/医生/护士/护士长
                for i in res:
                    print(i)
                    # 删除其他区选中的人
                    sql5 = "UPDATE location as l SET l.p_id = NULL WHERE l.p_id = '%s'" % i[0]
                    cursor.execute(sql5)
                    db.commit()
                    print(sql5)
                    # 更换区域病人信息
                    sql4 = "UPDATE location as l SET l.p_id = '%s' WHERE l.p_id = '%s'" % (i[0], p_id)
                    cursor.execute(sql4)
                    db.commit()
                    print(sql4)
                    msg = 'done1'
                    print(msg)
                    return render_template('d_recoverp.html', messages=msg, username=username)
        else:
            # 找到第一个轻症患者安排进相同病房/医生/护士/护士长
            for i in res:
                print(i)
                # 删除隔离区选中的人
                sql5 = "UPDATE location as l SET l.p_id = NULL WHERE l.p_id = '%s'" % i[0]
                cursor.execute(sql5)
                db.commit()
                print(sql5)
                # 更换区域病人信息
                sql4 = "UPDATE location as l SET l.p_id = '%s' WHERE l.p_id = '%s'" % (i[0], p_id)
                cursor.execute(sql4)
                db.commit()
                print(sql4)
                msg = 'done1'
                print(msg)
                return render_template('d_recoverp.html', messages=msg, username=username)

    return render_template('d_recoverp.html', username=username, messages=msg, userRole=userRole)



@app.route('/d_viewp', methods=['GET', 'POST'])
def d_viewp():
    msg = ""
    if request.method == 'GET':
        db = pymysql.connect("localhost", "root", password="20000106", db="Hospital", charset='utf8')
        cursor = db.cursor()
        try:
            cursor.execute("use Hospital")
        except:
            print("Error: unable to use database!")
        # 查询
        sql = "SELECT * FROM patient as p WHERE p_id = some(SELECT p_id FROM location WHERE Location.d_id = '%s')" % username
        cursor.execute(sql)
        res = cursor.fetchall()
        if len(res) != 0:
            msg = "done"
            print(msg)
            print(len(res))
            return render_template('d_viewp.html', username=username, result=res, messages=msg,
                                   userRole=userRole)
        else:
            print("NULL")
            msg = "none"
            return render_template('d_viewp.html', username=username, messages=msg, userRole=userRole)
    return render_template('d_viewp.html', username=username, messages=msg, userRole=userRole)

def get_tid():
    j = 5
    id = ''.join(str(i) for i in random.sample(range(0, 9), j))  # sample(seq, n) 从序列seq中选择n个随机且独立的元素；
    print("1"+id)
    return ("1"+id)

@app.route('/covid_add', methods=['GET', 'POST'])
def covid_add():
    msg = ""
    if request.form["action"] == "增加核酸检测报告":
        p_id = request.form['p_id']
        severity = request.form['severity']
        print(p_id)
        print(severity)
        return render_template('covid_add.html', p_id=p_id, severity=severity)

    elif request.form["action"] == "确认增加":
        db = pymysql.connect("localhost", "root", password="20000106", db="Hospital", charset='utf8')
        cursor = db.cursor()
        try:
            cursor.execute("use Hospital")
        except:
            print("Error: unable to use database!")
        p_id = request.form['p_id']
        severity = request.form['severity']
        date = request.form.get('date')
        result = request.form.get('result')
        tid = get_tid()
        sql = "INSERT into covid_test values ('{}', '{}',{}, '{}','{}', '{}')".format(tid, date, result, severity, p_id,
                                                                                        username)
        print(sql)
        cursor.execute(sql)
        db.commit()
        print("添加成功")
        msg = "done"
        return render_template('covid_add.html', messages=msg, username=username)

@app.route('/d_viewp_ml', methods=['GET', 'POST'])
def d_viewp_ml():
    msg = ""
    if request.form["action"] == '修改生命状态':
        p_id = request.form['p_id']
        print(p_id)
        return render_template('d_viewp_ml.html', p_id=p_id)

    elif request.form["action"] == '确认':
        db = pymysql.connect("localhost", "root", password="20000106", db="Hospital", charset='utf8')
        cursor = db.cursor()
        try:
            cursor.execute("use Hospital")
        except:
            print("Error: unable to use database!")
        result = request.form['result']
        p_id = request.form['p_id']
        print(p_id)
        print(result)
        sql8 = "SELECT distinct area FROM location WHERE location.d_id = '%s'" %username
        cursor.execute(sql8)
        db.commit()
        res = cursor.fetchall()
        areaa = res[0][0]
        if areaa == '1':
            pos = '轻症'
        elif areaa == '2':
            pos = '重症'
        else:
            pos = '危重症'
        # 让病人死
        if result == '病亡':
            # 执行死亡操作
            sql = "UPDATE patient as p SET p.life_state = '%s' WHERE p_id = '%s'" % (result, p_id)
            print(sql)
            cursor.execute(sql)
            db.commit()
            msg = 'done'
            # 查找隔离区病人
            sql3 = "SELECT * FROM patient WHERE patient.p_id = some(SELECT p_id FROM location WHERE location.area = 0) and patient.severity = '%s'" % pos
            cursor.execute(sql3)
            db.commit()
            res = cursor.fetchall()

            if len(res) == 0:
                # 无隔离区等候，开始搜索另外两个区域
                sql6 = "SELECT * FROM patient WHERE patient.p_id = some(SELECT p_id FROM location WHERE location.area != '%s' and location.area != 0) and patient.severity = '%s'" % (areaa,pos)
                cursor.execute(sql6)
                db.commit()
                res = cursor.fetchall()
                if len(res) == 0:
                    # 无适合患者
                    sql5 = "UPDATE location as l SET l.p_id = NULL, l.wn_id = NULL  WHERE l.p_id = '%s'" % p_id
                    cursor.execute(sql5)
                    db.commit()
                    return render_template('d_viewp_ml.html', messages=msg, username=username)
                else:
                    # 找到第一个轻症患者安排进相同病房/医生/护士/护士长
                    for i in res:
                        print(i)
                        # 删除其他区选中的人
                        sql5 = "UPDATE location as l SET l.p_id = NULL WHERE l.p_id = '%s'" % i[0]
                        cursor.execute(sql5)
                        db.commit()
                        print(sql5)
                        # 更换区域病人信息
                        sql4 = "UPDATE location as l SET l.p_id = '%s' WHERE l.p_id = '%s'" % (i[0], p_id)
                        cursor.execute(sql4)
                        db.commit()
                        print(sql4)
                        msg = 'done1'
                        print(msg)
                        return render_template('d_viewp_ml.html', messages=msg, username=username)
            else:
                # 找到第一个轻症患者安排进相同病房/医生/护士/护士长
                for i in res:
                    print(i)
                    # 删除隔离区选中的人
                    sql5 = "UPDATE location as l SET l.p_id = NULL WHERE l.p_id = '%s'" % i[0]
                    cursor.execute(sql5)
                    db.commit()
                    print(sql5)
                    # 更换区域病人信息
                    sql4 = "UPDATE location as l SET l.p_id = '%s' WHERE l.p_id = '%s'" % (i[0], p_id)
                    cursor.execute(sql4)
                    db.commit()
                    print(sql4)
                    msg = 'done1'
                    print(msg)
                    return render_template('d_viewp_ml.html', messages=msg, username=username)
        # check if the patient is qualified to be healthy
        if result == '康复出院':
            # 检验是否是轻症区域，有无权限
            sql3 = "SELECT distinct area FROM location WHERE location.d_id = '%s'" % username
            cursor.execute(sql3)
            db.commit()
            res = cursor.fetchall()
            print(res[0])
            if res[0][0] != '1':
                msg = 'fail1'
                return render_template('d_viewp_ml.html', messages=msg, username=username)
            # 检验3天体温和2次核酸
            sql1 = "SELECT temperature FROM daily_info WHERE daily_info.p_id = %s  ORDER BY the_date DESC" % p_id
            cursor.execute(sql1)
            db.commit()
            print("查询成功")
            res = cursor.fetchall()
            print(res)
            good = 0
            counter = 0
            if len(res) < 3:
                msg = 'fail'
                return render_template('d_viewp_ml.html', messages=msg, username=username)
            for i in res:
                if counter > 2:
                    break
                counter += 1
                if i[0] < '37.3':
                    good += 1
            if good != 3:
                msg = 'fail'
                return render_template('d_viewp_ml.html', messages=msg, username=username)
            sql2 = "SELECT result FROM covid_test WHERE covid_test.p_id = '%s'  ORDER BY the_date DESC" %p_id
            cursor.execute(sql2)
            db.commit()
            print("查询成功2")
            res = cursor.fetchall()
            print(res)
            good = 0
            counter = 0
            if len(res) < 2:
                msg = 'fail'
                return render_template('d_viewp_ml.html', messages=msg, username=username)
            for i in res:
                if counter > 1:
                    break
                counter += 1
                if not i[0]:
                    good += 1
            if good != 2:
                msg = 'fail'
                return render_template('d_viewp_ml.html', messages=msg, username=username)

            #执行出院康复操作
            sql = "UPDATE patient as p SET p.life_state = '%s' WHERE p_id = '%s'" % (result, p_id)
            print(sql)
            cursor.execute(sql)
            db.commit()
            msg = 'done'
            # 查找隔离区病人
            sql3 = "SELECT * FROM patient WHERE patient.p_id = some(SELECT p_id FROM location WHERE location.area = 0) and patient.severity = '%s'" % pos
            cursor.execute(sql3)
            db.commit()
            res = cursor.fetchall()

            if len(res) == 0:
                # 无隔离区等候，开始搜索另外两个区域
                sql6 = "SELECT * FROM patient WHERE patient.p_id = some(SELECT p_id FROM location WHERE location.area != '%s' and location.area != 0) and patient.severity = '%s'" % (areaa, pos)
                cursor.execute(sql6)
                db.commit()
                res = cursor.fetchall()
                if len(res) == 0:
                    # 无适合患者
                    sql5 = "UPDATE location as l SET l.p_id = NULL, l.wn_id = NULL  WHERE l.p_id = '%s'" % p_id
                    cursor.execute(sql5)
                    db.commit()
                    return render_template('d_viewp_ml.html', messages=msg, username=username)
                else:
                    # 找到第一个轻症患者安排进相同病房/医生/护士/护士长
                    for i in res:
                        print(i)
                        # 删除其他区选中的人
                        sql5 = "UPDATE location as l SET l.p_id = NULL WHERE l.p_id = '%s'" % i[0]
                        cursor.execute(sql5)
                        db.commit()
                        print(sql5)
                        # 更换区域病人信息
                        sql4 = "UPDATE location as l SET l.p_id = '%s' WHERE l.p_id = '%s'" % (i[0], p_id)
                        cursor.execute(sql4)
                        db.commit()
                        print(sql4)
                        msg = 'done1'
                        print(msg)
                        return render_template('d_viewp_ml.html', messages=msg, username=username)
            else:
                # 找到第一个轻症患者安排进相同病房/医生/护士/护士长
                for i in res:
                    print(i)
                    # 删除隔离区选中的人
                    sql5 = "UPDATE location as l SET l.p_id = NULL WHERE l.p_id = '%s'" % i[0]
                    cursor.execute(sql5)
                    db.commit()
                    print(sql5)
                    # 更换区域病人信息
                    sql4 = "UPDATE location as l SET l.p_id = '%s' WHERE l.p_id = '%s'" % (i[0], p_id)
                    cursor.execute(sql4)
                    db.commit()
                    print(sql4)
                    msg = 'done1'
                    print(msg)
                    return render_template('d_viewp_ml.html', messages=msg, username=username)

        sql = "UPDATE patient as p SET p.life_state = '%s' WHERE p_id = '%s'" %(result, p_id)
        print(sql)
        cursor.execute(sql)
        db.commit()
        print("成功")
        msg = "done"
        return render_template('d_viewp_ml.html', messages=msg, username=username)

@app.route('/d_viewp_ms', methods=['GET', 'POST'])
def d_viewp_ms():
    msg = 'done'
    if request.form["action"] == '修改病情':
        p_id = request.form['p_id']
        print(p_id)
        return render_template('d_viewp_ms.html', p_id=p_id)

    elif request.form["action"] == '确认':
        db = pymysql.connect("localhost", "root", password="20000106", db="Hospital", charset='utf8')
        cursor = db.cursor()
        try:
            cursor.execute("use Hospital")
        except:
            print("Error: unable to use database!")
        result = request.form.get('result')
        p_id = request.form['p_id']
        # 得到目前是什么区域 area
        sql10 = "SELECT distinct area FROM location WHERE d_id = '%s'" % username
        cursor.execute(sql10)
        db.commit()
        areaaa = cursor.fetchall()[0][0]
        # 将area对应名称
        if areaaa == '1':
            pos = '轻症'
        elif areaaa == '2':
            pos = '重症'
        else:
            pos = '危重症'
        # 将病人病情评级对应area
        if result == '轻症':
            areaa = 1
        elif result == '重症':
            areaa = 2
        else:
            areaa = 3
        # 只有现在的area和之前的不相同才进行下属操作
        if areaa != areaaa:
            sql = "UPDATE patient as p SET p.severity = '%s' WHERE p_id = '%s'" % (result, p_id)
            print(sql)
            print(p_id)
            print(result)
            cursor.execute(sql)
            db.commit()
            print("修改成功")
            msg = "done2"
            # 送病人到对应区域
            # 检查有无空床位
            sql3 = "SELECT * FROM location WHERE location.area = '%s' and location.p_id is null" % areaa
            cursor.execute(sql3)
            db.commit()
            res = cursor.fetchall()
            # 无空床位，取消送人操作
            if len(res) == 0:
                msg = 'done1'
                return render_template('d_viewp_ms.html', messages=msg, username=username)
            # 有空床位则送入
            else:
                if areaa == 1:
                    sql9 = "(SELECT wn_id FROM ward_nurse WHERE wn_id NOT IN ((SELECT wn_id FROM location l WHERE l.area = 1 and wn_id is not null) UNION (SELECT wn_id FROM location l WHERE l.area = 2 and wn_id is not null) UNION (SELECT wn_id FROM location l WHERE l.area = 3 and wn_id is not null) )) UNION (SELECT h.wn_id FROM (SELECT l.wn_id, COUNT(*) as job FROM location as l WHERE l.area = 1 GROUP BY l.wn_id) as h WHERE h.job < 4)"
                elif areaa == 2:
                    sql9 = "(SELECT wn_id FROM ward_nurse WHERE wn_id NOT IN ((SELECT wn_id FROM location l WHERE l.area = 1 and wn_id is not null) UNION (SELECT wn_id FROM location l WHERE l.area = 2 and wn_id is not null) UNION (SELECT wn_id FROM location l WHERE l.area = 3 and wn_id is not null) )) UNION (SELECT h.wn_id FROM (SELECT l.wn_id, COUNT(*) as job FROM location as l WHERE l.area = 2 GROUP BY l.wn_id) as h WHERE h.job < 2)"
                elif areaa == 3:
                    sql9 = "(SELECT wn_id FROM ward_nurse WHERE wn_id NOT IN ((SELECT wn_id FROM location l WHERE l.area = 1 and wn_id is not null) UNION (SELECT wn_id FROM location l WHERE l.area = 2 and wn_id is not null) UNION (SELECT wn_id FROM location l WHERE l.area = 3 and wn_id is not null) )) UNION (SELECT h.wn_id FROM (SELECT l.wn_id, COUNT(*) as job FROM location as l WHERE l.area = 3 GROUP BY l.wn_id) as h WHERE h.job < 1)"
                cursor.execute(sql9)
                db.commit()
                res2 = cursor.fetchall()
                if len(res2) == 0:
                    msg = 'done1'
                    return render_template('d_viewp_ms.html', messages=msg, username=username)
                a = res[0][0]
                b = res[0][1]
                c = res[0][2]

                # 从其他区域接收病人
                # 查找隔离区病人
                sql3 = "SELECT * FROM patient WHERE patient.p_id = some(SELECT p_id FROM location WHERE location.area = 0) and patient.severity = '%s'" % pos
                cursor.execute(sql3)
                db.commit()
                res = cursor.fetchall()
                print(res)
                if len(res) == 0:
                    # 无隔离区等候，开始搜索另外两个区域
                    sql6 = "SELECT * FROM patient WHERE patient.p_id = some(SELECT p_id FROM location WHERE location.area != '%s' and location.area != 0) and patient.severity = '%s'" % (
                        areaaa, pos)
                    cursor.execute(sql6)
                    db.commit()
                    res = cursor.fetchall()
                    print(res)
                    if len(res) == 0:
                        # 无适合患者
                        sql5 = "UPDATE location as l SET l.p_id = NULL, l.wn_id = NULL  WHERE l.p_id = '%s'" % p_id
                        cursor.execute(sql5)
                        db.commit()
                        sql7 = "UPDATE location as l SET l.p_id = '%s',l.wn_id = '%s' WHERE l.area = '%s' and l.room_no = '%s' and l.bed_no = '%s'" % (
                            p_id, res2[0][0], a, b, c)
                        print(sql7)
                        cursor.execute(sql7)
                        db.commit()
                        msg = 'done'
                        return render_template('d_viewp_ms.html', messages=msg, username=username)
                    else:
                        # 找到第一个轻症患者安排进相同病房/医生/护士/护士长
                        for i in res:
                            print(i)
                            # 删除其他区选中的人
                            sql5 = "UPDATE location as l SET l.p_id = NULL WHERE l.p_id = '%s'" % i[0]
                            cursor.execute(sql5)
                            db.commit()
                            print(sql5)
                            # 更换区域病人信息
                            sql4 = "UPDATE location as l SET l.p_id = '%s' WHERE l.p_id = '%s'" % (i[0], p_id)
                            cursor.execute(sql4)
                            db.commit()
                            print(sql4)
                            msg = 'done'
                            # 完成最初病人更新
                            sql5 = "UPDATE location as l SET l.p_id = '%s',l.wn_id = '%s' WHERE l.area = '%s' and l.room_no = '%s' and l.bed_no = '%s'" % (
                            p_id, res2[0][0], a, b, c)
                            print(sql5)
                            cursor.execute(sql5)
                            db.commit()
                            return render_template('d_viewp_ms.html', messages=msg, username=username)
                else:
                    # 找到第一个轻症患者安排进相同病房/医生/护士/护士长
                    for i in res:
                        # 删除隔离区选中的人
                        sql5 = "UPDATE location as l SET l.p_id = NULL WHERE l.p_id = '%s'" % i[0]
                        cursor.execute(sql5)
                        db.commit()
                        print(sql5)
                        # 更换区域病人信息
                        sql4 = "UPDATE location as l SET l.p_id = '%s' WHERE l.p_id = '%s'" % (i[0], p_id)
                        cursor.execute(sql4)
                        db.commit()
                        print(sql4)
                        # 完成最初病人更新
                        sql5 = "UPDATE location as l SET l.p_id = '%s',l.wn_id = '%s' WHERE l.area = '%s' and l.room_no = '%s' and l.bed_no = '%s'" % (
                        p_id, res2[0][0], a, b, c)
                        print(sql5)
                        cursor.execute(sql5)
                        db.commit()
                        msg = 'done'
                        return render_template('d_viewp_ms.html', messages=msg, username=username)
        return render_template('d_viewp_ms.html', messages=msg, username=username)

# 护士长！！！！！！！！！！！！！！！！！！！！！！！！！！！！！！！！！！！！！！！！！！！！！！！！！！！！！！！
# 修改个人信息页面
@app.route('/ModifyPersonalInfo_hn', methods=['GET', 'POST'])
def ModifyPersonalInfo_hn():
    msg = ""
    if request.method == 'GET':
        return render_template('ModifyPersonalInfo_hn.html', username=username)
    if request.method == 'POST':
        # username = request.form['username']
        phonenum = request.form['phonenum']
        # 连接数据库，默认数据库用户名root，密码空
        db = pymysql.connect("localhost", "root", password="20000106", db="Hospital", charset='utf8')
        cursor = db.cursor()
        try:
            cursor.execute("use Hospital")
        except:
            print("Error: unable to use database!")
        if userRole == 'doctor':
            sql = "Update {} SET contact_info = '{}' where d_id = '{}'".format(userRole, phonenum,
                                                                                        username)
        elif userRole == 'head_nurse':
            sql = "Update {} SET contact_info = '{}' where hn_id = '{}'".format(userRole, phonenum,
                                                                               username)
        elif userRole == 'ward_nurse':
            sql = "Update {} SET contact_info = '{}' where wn_id = '{}'".format(userRole, phonenum,
                                                                               username)
        elif userRole == 'emergency_nurse':
            sql = "Update {} SET contact_info = '{}' where en_id = '{}'".format(userRole, phonenum,
                                                                              username)
        try:
            cursor.execute(sql)
            db.commit()
            # print("修改个人信息成功")
            msg = "done"
        except ValueError as e:
            print("--->", e)
            print("修改个人信息失败")
            msg = "fail"
        return render_template('ModifyPersonalInfo_hn.html', messages=msg, username=username, userRole=userRole)


# 修改密码页面
@app.route('/ModifyPassword_hn', methods=['GET', 'POST'])
def ModifyPassword_hn():
    msg = ""
    if request.method == 'GET':
        return render_template('ModifyPassword_hn.html', username=username, userRole=userRole)
    if request.method == 'POST':
        # username = request.form['username']
        psw1 = request.form['psw1']
        psw2 = request.form['psw2']
        # 两次输入密码是否相同
        if psw1 == psw2:
            db = pymysql.connect("localhost", "root", password="20000106", db="Hospital", charset='utf8')
            cursor = db.cursor()
            try:
                cursor.execute("use Hospital")
            except:
                print("Error: unable to use database!")
            if userRole == 'doctor':
                sql = "Update {} SET password = '{}' where d_id = '{}'".format(userRole, psw1,
                                                                                   username)
            elif userRole == 'head_nurse':
                sql = "Update {} SET password = '{}' where hn_id = '{}'".format(userRole, psw1,
                                                                                    username)
            elif userRole == 'ward_nurse':
                sql = "Update {} SET password = '{}' where wn_id = '{}'".format(userRole, psw1,
                                                                                    username)
            elif userRole == 'emergency_nurse':
                sql = "Update {} SET password = '{}' where en_id = '{}'".format(userRole, psw1,
                                                                                    username)
            try:
                cursor.execute(sql)
                db.commit()
                # print("修改密码成功")
                msg = "done"
            except ValueError as e:
                print("--->", e)
                print("修改密码失败")
                msg = "fail"
            return render_template('ModifyPassword_hn.html', messages=msg, username=username, userRole=userRole)
        else:
            msg = "not equal"
            return render_template('ModifyPassword_hn.html', messages=msg, username=username, userRole=userRole)


@app.route('/hn_viewp', methods=['GET', 'POST'])
def hn_viewp():
    msg = ""
    if request.method == 'GET':
        db = pymysql.connect("localhost", "root", password="20000106", db="Hospital", charset='utf8')
        cursor = db.cursor()
        try:
            cursor.execute("use Hospital")
        except:
            print("Error: unable to use database!")
        # 查询
        sql = "SELECT * FROM patient as p WHERE p_id = some(SELECT p_id FROM location WHERE Location.hn_id = '%s')" % username
        cursor.execute(sql)
        res = cursor.fetchall()
        db.commit()
        if len(res) != 0:
            msg = "done"
            print(msg)
            print(len(res))
            return render_template('hn_viewp.html', username=username, result=res, messages=msg,
                                   userRole=userRole)
        else:
            print("NULL")
            msg = "none"
            return render_template('hn_viewp.html', username=username, messages=msg, userRole=userRole)


    return render_template('hn_viewp.html', username=username, messages=msg, userRole=userRole)

@app.route('/hn_viewwn', methods=['GET', 'POST'])
def hn_viewwn():
    msg = ''
    db = pymysql.connect("localhost", "root", password="20000106", db="Hospital", charset='utf8')
    cursor = db.cursor()
    try:
        cursor.execute("use Hospital")
    except:
        print("Error: unable to use database!")
    # 查询
    sql = "SELECT * FROM ward_nurse as wn WHERE wn.wn_id = some(SELECT distinct wn_id FROM location as l WHERE (l.hn_id =  '%s') and l.wn_id is not null)" % username
    cursor.execute(sql)
    db.commit()
    res = cursor.fetchall()


    if len(res) != 0:
        msg = "done"
        print(msg)
        print(len(res))
        sql2 = "SELECT l.wn_id, l.bed_no,l.room_no FROM location as l WHERE l.hn_id = '%s' and l.wn_id is not null" % username
        cursor.execute(sql2)
        db.commit()
        res2 = cursor.fetchall()
        sql3 = "SELECT wn_id, p.name FROM patient as p natural join location  WHERE p.p_id = some (SELECT l.p_id FROM location as l WHERE l.hn_id = '%s'  and l.wn_id is not null)" % username
        cursor.execute(sql3)
        db.commit()
        res3 = cursor.fetchall()
        res_final = []
        for i in res:
            aNew = list(i)
            a = ""
            for j in res2:
                if i[0] == j[0]:
                    for k in res3:
                        if i[0] == k[0]:
                            a += "房间" + str(j[2]) + "床位" + str(j[1]) + ": "+" " + str(k[1]) + " "+" "
                            res3 = res3[1:]
            aNew.append(a)
            res_final.append(aNew)
        return render_template('hn_viewwn.html', username=username, result=res_final, messages=msg,
                               userRole=userRole)
    else:
        print("NULL")
        msg = "none"
        return render_template('hn_viewwn.html', username=username, messages=msg, userRole=userRole)


@app.route('/hn_viewb', methods=['GET', 'POST'])
def hn_viewb():
    msg = ''
    db = pymysql.connect("localhost", "root", password="20000106", db="Hospital", charset='utf8')
    cursor = db.cursor()
    try:
        cursor.execute("use Hospital")
    except:
        print("Error: unable to use database!")
    # 查询
    sql = "SELECT * FROM location LEFT OUTER JOIN patient ON location.p_id = patient.p_id WHERE hn_id = '%s'" % username
    cursor.execute(sql)
    db.commit()
    res = cursor.fetchall()

    if len(res) != 0:
        msg = "done"
        print(msg)
        print(len(res))
        res_final = []
        a = ''
        for i in res:
            aNew = []
            if i[6] is None:
                a = "房间" + str(i[1]) + "床位" + str(i[2]) +"（空闲） "
                aNew.append(a)
                aNew.append('无'+'')
                aNew.append('无'+'')
            else:
                a = "房间" + str(i[1]) + "床位" + str(i[2])
                aNew.append(a)
                aNew.append(i[6])
                aNew.append(i[8])
            res_final.append(aNew)
        return render_template('hn_viewb.html', username=username, result=res_final, messages=msg,
                               userRole=userRole)
    else:
        print("NULL")
        msg = "none"
        return render_template('hn_viewb.html', username=username, messages=msg, userRole=userRole)

# 病房护士！！！！！！！！！！！！！！！！！！！！！！！！！！！！！！！！！！！！！！！！！！！！！！！！！！！！！！！
# 修改个人信息页面
@app.route('/ModifyPersonalInfo_wn', methods=['GET', 'POST'])
def ModifyPersonalInfo_wn():
    msg = ""
    if request.method == 'GET':
        return render_template('ModifyPersonalInfo_wn.html', username=username)
    if request.method == 'POST':
        # username = request.form['username']
        phonenum = request.form['phonenum']
        # 连接数据库，默认数据库用户名root，密码空
        db = pymysql.connect("localhost", "root", password="20000106", db="Hospital", charset='utf8')
        cursor = db.cursor()
        try:
            cursor.execute("use Hospital")
        except:
            print("Error: unable to use database!")
        if userRole == 'doctor':
            sql = "Update {} SET contact_info = '{}' where d_id = '{}'".format(userRole, phonenum,
                                                                                        username)
        elif userRole == 'head_nurse':
            sql = "Update {} SET contact_info = '{}' where hn_id = '{}'".format(userRole, phonenum,
                                                                               username)
        elif userRole == 'ward_nurse':
            sql = "Update {} SET contact_info = '{}' where wn_id = '{}'".format(userRole, phonenum,
                                                                               username)
        elif userRole == 'emergency_nurse':
            sql = "Update {} SET contact_info = '{}' where en_id = '{}'".format(userRole, phonenum,
                                                                              username)
        try:
            cursor.execute(sql)
            db.commit()
            # print("修改个人信息成功")
            msg = "done"
        except ValueError as e:
            print("--->", e)
            print("修改个人信息失败")
            msg = "fail"
        return render_template('ModifyPersonalInfo_wn.html', messages=msg, username=username, userRole=userRole)


# 修改密码页面
@app.route('/ModifyPassword_wn', methods=['GET', 'POST'])
def ModifyPassword_wn():
    msg = ""
    if request.method == 'GET':
        return render_template('ModifyPassword_wn.html', username=username, userRole=userRole)
    if request.method == 'POST':
        # username = request.form['username']
        psw1 = request.form['psw1']
        psw2 = request.form['psw2']
        # 两次输入密码是否相同
        if psw1 == psw2:
            db = pymysql.connect("localhost", "root", password="20000106", db="Hospital", charset='utf8')
            cursor = db.cursor()
            try:
                cursor.execute("use Hospital")
            except:
                print("Error: unable to use database!")
            if userRole == 'doctor':
                sql = "Update {} SET password = '{}' where d_id = '{}'".format(userRole, psw1,
                                                                                   username)
            elif userRole == 'head_nurse':
                sql = "Update {} SET password = '{}' where hn_id = '{}'".format(userRole, psw1,
                                                                                    username)
            elif userRole == 'ward_nurse':
                sql = "Update {} SET password = '{}' where wn_id = '{}'".format(userRole, psw1,
                                                                                    username)
            elif userRole == 'emergency_nurse':
                sql = "Update {} SET password = '{}' where en_id = '{}'".format(userRole, psw1,
                                                                                    username)
            try:
                cursor.execute(sql)
                db.commit()
                # print("修改密码成功")
                msg = "done"
            except ValueError as e:
                print("--->", e)
                print("修改密码失败")
                msg = "fail"
            return render_template('ModifyPassword_wn.html', messages=msg, username=username, userRole=userRole)
        else:
            msg = "not equal"
            return render_template('ModifyPassword_wn.html', messages=msg, username=username, userRole=userRole)

# 急诊护士！！！！！！！！！！！！！！！！！！！！！！！！！！！！！！！！！！！！！！！！！！！！！！！！！！！！！！！
# 修改个人信息页面
@app.route('/ModifyPersonalInfo_en', methods=['GET', 'POST'])
def ModifyPersonalInfo_en():
    msg = ""
    if request.method == 'GET':
        return render_template('ModifyPersonalInfo_en.html', username=username)
    if request.method == 'POST':
        # username = request.form['username']
        phonenum = request.form['phonenum']
        # 连接数据库，默认数据库用户名root，密码空
        db = pymysql.connect("localhost", "root", password="20000106", db="Hospital", charset='utf8')
        cursor = db.cursor()
        try:
            cursor.execute("use Hospital")
        except:
            print("Error: unable to use database!")
        if userRole == 'doctor':
            sql = "Update {} SET contact_info = '{}' where d_id = '{}'".format(userRole, phonenum,
                                                                                        username)
        elif userRole == 'head_nurse':
            sql = "Update {} SET contact_info = '{}' where hn_id = '{}'".format(userRole, phonenum,
                                                                               username)
        elif userRole == 'ward_nurse':
            sql = "Update {} SET contact_info = '{}' where wn_id = '{}'".format(userRole, phonenum,
                                                                               username)
        elif userRole == 'emergency_nurse':
            sql = "Update {} SET contact_info = '{}' where en_id = '{}'".format(userRole, phonenum,
                                                                              username)
        try:
            cursor.execute(sql)
            db.commit()
            # print("修改个人信息成功")
            msg = "done"
        except ValueError as e:
            print("--->", e)
            print("修改个人信息失败")
            msg = "fail"
        return render_template('ModifyPersonalInfo_en.html', messages=msg, username=username, userRole=userRole)


# 修改密码页面
@app.route('/ModifyPassword_en', methods=['GET', 'POST'])
def ModifyPassword_en():
    msg = ""
    if request.method == 'GET':
        return render_template('ModifyPassword_en.html', username=username, userRole=userRole)
    if request.method == 'POST':
        # username = request.form['username']
        psw1 = request.form['psw1']
        psw2 = request.form['psw2']
        # 两次输入密码是否相同
        if psw1 == psw2:
            db = pymysql.connect("localhost", "root", password="20000106", db="Hospital", charset='utf8')
            cursor = db.cursor()
            try:
                cursor.execute("use Hospital")
            except:
                print("Error: unable to use database!")
            if userRole == 'doctor':
                sql = "Update {} SET password = '{}' where d_id = '{}'".format(userRole, psw1,
                                                                                   username)
            elif userRole == 'head_nurse':
                sql = "Update {} SET password = '{}' where hn_id = '{}'".format(userRole, psw1,
                                                                                    username)
            elif userRole == 'ward_nurse':
                sql = "Update {} SET password = '{}' where wn_id = '{}'".format(userRole, psw1,
                                                                                    username)
            elif userRole == 'emergency_nurse':
                sql = "Update {} SET password = '{}' where en_id = '{}'".format(userRole, psw1,
                                                                                    username)
            try:
                cursor.execute(sql)
                db.commit()
                # print("修改密码成功")
                msg = "done"
            except ValueError as e:
                print("--->", e)
                print("修改密码失败")
                msg = "fail"
            return render_template('ModifyPassword_en.html', messages=msg, username=username, userRole=userRole)
        else:
            msg = "not equal"
            return render_template('ModifyPassword_hn.html', messages=msg, username=username, userRole=userRole)


def get_dailyid():
    j = 5
    id = ''.join(str(i) for i in random.sample(range(0, 9), j))  # sample(seq, n) 从序列seq中选择n个随机且独立的元素；
    return ("0"+id)

@app.route('/wn_daily', methods=['GET', 'POST'])
def wn_daily():
    msg = ""
    if request.method == 'GET':
        return render_template('wn_daily.html', username=username, userRole=userRole)

    if request.form["action"] == "确认":
        db = pymysql.connect("localhost", "root", password="20000106", db="Hospital", charset='utf8')
        cursor = db.cursor()
        try:
             cursor.execute("use Hospital")
        except:
            print("Error: unable to use database!")
        p_id = request.form['p_id']
        temperature = request.form['temperature']
        symptom = request.form['symptom']
        date = request.form.get('date')
        result = request.form.get('result')
        dfid = get_dailyid()
        life = request.form.get('result3')
        if p_id is None or temperature is None or symptom is None or date is None or result is None or life is None:
            msg = 'fail'
            return render_template('en_newp.html', messages=msg, username=username)
        print(p_id)
        print(temperature)
        print(symptom)
        print(date)
        print(result)
        print(dfid)
        print(life)
        sql1 ="SELECT * FROM location natural join patient WHERE patient.p_id = '%s' and location.wn_id = '%s'" %(p_id, username)
        cursor.execute(sql1)
        db.commit()
        res = cursor.fetchall()
        if len(res) == 0:
            msg = 'fail1'
            return render_template('wn_daily.html', messages=msg, username=username)
        if temperature > '41' or temperature < '36':
            msg = 'fail2'
            return render_template('wn_daily.html', messages=msg, username=username)
        sql = "INSERT into daily_info values ('{}', '{}','{}', '{}',{},'{}', '{}','{}')".format(dfid, date, temperature, symptom, result, life, p_id, username)
        print(sql)
        cursor.execute(sql)
        db.commit()
        print("添加成功")
        msg = "done"
        return render_template('wn_daily.html', messages=msg, username=username)
    return render_template('wn_daily.html', username=username, userRole=userRole)


@app.route('/wn_viewp', methods=['GET', 'POST'])
def wn_viewp():
    msg = ""
    if request.method == 'GET':
        db = pymysql.connect("localhost", "root", password="20000106", db="Hospital", charset='utf8')
        cursor = db.cursor()
        try:
            cursor.execute("use Hospital")
        except:
            print("Error: unable to use database!")
        # 查询
        sql = "SELECT * FROM patient as p WHERE p_id = some(SELECT p_id FROM location WHERE Location.wn_id = '%s')" % username
        cursor.execute(sql)
        res = cursor.fetchall()
        db.commit()
        if len(res) != 0:
            msg = "done"
            print(msg)
            print(len(res))
            return render_template('wn_viewp.html', username=username, result=res, messages=msg,
                                   userRole=userRole)
        else:
            print("NULL")
            msg = "none"
            return render_template('wn_viewp.html', username=username, messages=msg, userRole=userRole)

def get_pid():
    j = 5
    id = ''.join(str(i) for i in random.sample(range(0, 9), j))  # sample(seq, n) 从序列seq中选择n个随机且独立的元素；
    return ("7"+id)

@app.route('/en_newp', methods=['GET', 'POST'])
def en_newp():
    msg = ""
    if request.method == 'GET':
        return render_template('en_newp.html', username=username, userRole=userRole)

    if request.form["action"] == "确认":
        db = pymysql.connect("localhost", "root", password="20000106", db="Hospital", charset='utf8')
        cursor = db.cursor()
        try:
             cursor.execute("use Hospital")
        except:
            print("Error: unable to use database!")
        p_id = get_pid()
        name = request.form['name']
        age = request.form['age']
        contact = request.form.get('contact_info')
        severity = request.form.get('severity')
        life = '住院治疗'


        sql = "INSERT into patient values ('{}', '{}',{}, '{}','{}','{}','{}')".format(p_id, name, age, contact, severity, life,username)
        print(sql)
        cursor.execute(sql)
        db.commit()
        print("添加成功")
        msg = "done"
        if severity == '轻症':
            areaa = 1
        elif severity == '重症':
            areaa = 2
        else:
            areaa =3
        # 查找适合床位
        sql3 = "SELECT * FROM location WHERE location.area = '%s' and location.p_id is null" % areaa
        cursor.execute(sql3)
        db.commit()
        res = cursor.fetchall()
        # 无空床位，取消送人操作
        if len(res) == 0:
            msg = 'done'
            sql = "SELECT room_no, bed_no FROM location WHERE area = 0 and p_id is null"
            cursor.execute(sql)
            db.commit()
            tey = cursor.fetchall()
            a = tey[0][0]
            b = tey[0][1]
            sql5 = "UPDATE location as l SET l.p_id = '%s' WHERE l.area = 0 and l.room_no = '%s' and l.bed_no = '%s'" % (
                p_id, a, b)
            print(sql5)
            cursor.execute(sql5)
            db.commit()
            return render_template('en_newp.html', messages=msg, username=username)
        # 有空床位则送入
        else:
            if areaa == 1:
                sql9 = "(SELECT wn_id FROM ward_nurse WHERE wn_id NOT IN ((SELECT wn_id FROM location l WHERE l.area = 1 and wn_id is not null) UNION (SELECT wn_id FROM location l WHERE l.area = 2 and wn_id is not null) UNION (SELECT wn_id FROM location l WHERE l.area = 3 and wn_id is not null) )) UNION (SELECT h.wn_id FROM (SELECT l.wn_id, COUNT(*) as job FROM location as l WHERE l.area = 1 GROUP BY l.wn_id) as h WHERE h.job < 4)"
            elif areaa == 2:
                sql9 = "(SELECT wn_id FROM ward_nurse WHERE wn_id NOT IN ((SELECT wn_id FROM location l WHERE l.area = 1 and wn_id is not null) UNION (SELECT wn_id FROM location l WHERE l.area = 2 and wn_id is not null) UNION (SELECT wn_id FROM location l WHERE l.area = 3 and wn_id is not null) )) UNION (SELECT h.wn_id FROM (SELECT l.wn_id, COUNT(*) as job FROM location as l WHERE l.area = 2 GROUP BY l.wn_id) as h WHERE h.job < 2)"
            elif areaa == 3:
                sql9 = "(SELECT wn_id FROM ward_nurse WHERE wn_id NOT IN ((SELECT wn_id FROM location l WHERE l.area = 1 and wn_id is not null) UNION (SELECT wn_id FROM location l WHERE l.area = 2 and wn_id is not null) UNION (SELECT wn_id FROM location l WHERE l.area = 3 and wn_id is not null) )) UNION (SELECT h.wn_id FROM (SELECT l.wn_id, COUNT(*) as job FROM location as l WHERE l.area = 3 GROUP BY l.wn_id) as h WHERE h.job < 1)"
            cursor.execute(sql9)
            db.commit()
            res2 = cursor.fetchall()
            # 无法送达因为没有空余护士
            if len(res2) == 0:
                msg = 'done'
                return render_template('en_newp.html', messages=msg, username=username)
            a = res[0][0]
            b = res[0][1]
            c = res[0][2]
            sql5 = "UPDATE location as l SET l.p_id = '%s',l.wn_id = '%s' WHERE l.area = '%s' and l.room_no = '%s' and l.bed_no = '%s'" % (
                p_id, res2[0][0], a, b, c)
            print(sql5)
            cursor.execute(sql5)
            db.commit()
        return render_template('en_newp.html', messages=msg, username=username)
    return render_template('en_newp.html', username=username, userRole=userRole)

# 急诊护士选择
@app.route('/en_viewp_i', methods=['GET', 'POST'])
def en_viewp_i():
    msg = ""
    if request.method == 'GET':
        return render_template('en_viewp_i.html')
    if request.method == 'POST':
        area = request.form.get('area')
        print(area)
        return render_template('en_viewp_i.html', messages=area, username=username, userRole=userRole)

@app.route('/en_viewp0', methods=['GET', 'POST'])
def en_viewp0():
    msg = ""
    if request.method == 'GET':
        db = pymysql.connect("localhost", "root", password="20000106", db="Hospital", charset='utf8')
        cursor = db.cursor()
        try:
            cursor.execute("use Hospital")
        except:
            print("Error: unable to use database!")
        # 查询
        sql = "SELECT * FROM patient as p WHERE p_id = some(SELECT p_id FROM location WHERE Location.area = 0)"
        cursor.execute(sql)
        res = cursor.fetchall()
        db.commit()
        if len(res) != 0:
            msg = "done"
            print(msg)
            print(len(res))
            return render_template('en_viewp0.html', username=username, result=res, messages=msg,
                                   userRole=userRole)
        else:
            print("NULL")
            msg = "none"
            return render_template('en_viewp0.html', username=username, messages=msg, userRole=userRole)

@app.route('/en_viewp1', methods=['GET', 'POST'])
def en_viewp1():
    msg = ""
    if request.method == 'GET':
        db = pymysql.connect("localhost", "root", password="20000106", db="Hospital", charset='utf8')
        cursor = db.cursor()
        try:
            cursor.execute("use Hospital")
        except:
            print("Error: unable to use database!")
        # 查询
        sql = "SELECT * FROM patient as p WHERE p_id = some(SELECT p_id FROM location WHERE Location.area = 1)"
        cursor.execute(sql)
        res = cursor.fetchall()
        db.commit()
        if len(res) != 0:
            msg = "done"
            print(msg)
            print(len(res))
            return render_template('en_viewp1.html', username=username, result=res, messages=msg,
                                   userRole=userRole)
        else:
            print("NULL")
            msg = "none"
            return render_template('en_viewp1.html', username=username, messages=msg, userRole=userRole)

@app.route('/en_viewp2', methods=['GET', 'POST'])
def en_viewp2():
    msg = ""
    if request.method == 'GET':
        db = pymysql.connect("localhost", "root", password="20000106", db="Hospital", charset='utf8')
        cursor = db.cursor()
        try:
            cursor.execute("use Hospital")
        except:
            print("Error: unable to use database!")
        # 查询
        sql = "SELECT * FROM patient as p WHERE p_id = some(SELECT p_id FROM location WHERE Location.area = 2)"
        cursor.execute(sql)
        res = cursor.fetchall()
        db.commit()
        if len(res) != 0:
            msg = "done"
            print(msg)
            print(len(res))
            return render_template('en_viewp2.html', username=username, result=res, messages=msg,
                                   userRole=userRole)
        else:
            print("NULL")
            msg = "none"
            return render_template('en_viewp2.html', username=username, messages=msg, userRole=userRole)

@app.route('/en_viewp3', methods=['GET', 'POST'])
def en_viewp3():
    msg = ""
    if request.method == 'GET':
        db = pymysql.connect("localhost", "root", password="20000106", db="Hospital", charset='utf8')
        cursor = db.cursor()
        try:
            cursor.execute("use Hospital")
        except:
            print("Error: unable to use database!")
        # 查询
        sql = "SELECT * FROM patient as p WHERE p_id = some(SELECT p_id FROM location WHERE Location.area = 3)"
        cursor.execute(sql)
        res = cursor.fetchall()
        db.commit()
        if len(res) != 0:
            msg = "done"
            print(msg)
            print(len(res))
            return render_template('en_viewp3.html', username=username, result=res, messages=msg,
                                   userRole=userRole)
        else:
            print("NULL")
            msg = "none"
            return render_template('en_viewp3.html', username=username, messages=msg, userRole=userRole)

@app.route('/d_viewp_m', methods=['GET', 'POST'])
def d_viewp_m():
    msg = ""
    if request.form["action"] == "确认条件":
        recover = request.form['recover']
        right = request.form['right']
        print(recover)
        print(right)
        db = pymysql.connect("localhost", "root", password="20000106", db="Hospital", charset='utf8')
        cursor = db.cursor()
        cursor.execute("use Hospital")

        if right == "1" and recover == "0":
            sql3 = "SELECT distinct area FROM location WHERE location.d_id = '%s'" % username
            cursor.execute(sql3)
            db.commit()
            res = cursor.fetchall()
            print(res[0])

            # 检验3天体温和2次核酸
            # for loop 找pid
            areaa = res[0][0]

            if areaa == '1':
                pos = '轻症'
            elif areaa == '2':
                pos = '重症'
            else:
                pos = '危重症'

            sql2 = "SELECT * FROM patient WHERE patient.p_id = some(SELECT p_id FROM location WHERE location.area = '%s' and location.area != 0) and patient.severity != '%s'" % (
                areaa, pos)
            cursor.execute(sql2)
            db.commit()
            all_p_id = cursor.fetchall()
            the_list = []
            for p_id in all_p_id:

                sql1 = "SELECT temperature FROM daily_info WHERE daily_info.p_id = %s  ORDER BY the_date DESC" % p_id[0]
                cursor.execute(sql1)
                db.commit()
                print("查询成功")
                res = cursor.fetchall()
                print(res)
                good = 0
                counter = 0
                all = 0
                if len(res) < 3:
                    all += 1
                for i in res:
                    if counter > 2:
                        break
                    counter += 1
                    if i[0] < '37.3':
                        good += 1
                if good != 3:
                    all += 1
                sql2 = "SELECT result FROM covid_test WHERE covid_test.p_id = '%s'  ORDER BY the_date DESC" % p_id[0]
                cursor.execute(sql2)
                db.commit()
                print("查询成功2")
                res = cursor.fetchall()
                print(res)
                good = 0
                counter = 0
                if len(res) < 2:
                    all += 1
                for i in res:
                    if counter > 1:
                        break
                    counter += 1
                    if not i[0]:
                        good += 1
                if good != 2:
                    all += 1

                if all != 0:
                    the_list.append(p_id)
            if len(the_list) != 0:
                msg = "done"
                print(msg)
                print(len(the_list))
                return render_template('d_viewp_m.html', username=username, result=the_list, messages=msg,
                                       userRole=userRole)
            else:
                print("NULL")
                msg = "none"
                return render_template('d_viewp_m.html', username=username, messages=msg, userRole=userRole)

        if right == "0" and recover == "0":
            sql3 = "SELECT distinct area FROM location WHERE location.d_id = '%s'" % username
            cursor.execute(sql3)
            db.commit()
            res = cursor.fetchall()
            print(res[0])

            # 检验3天体温和2次核酸
            # for loop 找pid
            areaa = res[0][0]

            if areaa == '1':
                pos = '轻症'
            elif areaa == '2':
                pos = '重症'
            else:
                pos = '危重症'

            sql2 = "SELECT * FROM patient WHERE patient.p_id = some(SELECT p_id FROM location WHERE location.area = '%s' and location.area != 0) and patient.severity = '%s'" % (
                areaa, pos)
            cursor.execute(sql2)
            db.commit()
            all_p_id = cursor.fetchall()
            the_list = []
            for p_id in all_p_id:

                sql1 = "SELECT temperature FROM daily_info WHERE daily_info.p_id = %s  ORDER BY the_date DESC" % p_id[0]
                cursor.execute(sql1)
                db.commit()
                print("查询成功")
                res = cursor.fetchall()
                print(res)
                good = 0
                counter = 0
                all = 0
                if len(res) < 3:
                    all += 1
                for i in res:
                    if counter > 2:
                        break
                    counter += 1
                    if i[0] < '37.3':
                        good += 1
                if good != 3:
                    all += 1
                sql2 = "SELECT result FROM covid_test WHERE covid_test.p_id = '%s'  ORDER BY the_date DESC" % p_id[0]
                cursor.execute(sql2)
                db.commit()
                print("查询成功2")
                res = cursor.fetchall()
                print(res)
                good = 0
                counter = 0
                if len(res) < 2:
                    all += 1
                for i in res:
                    if counter > 1:
                        break
                    counter += 1
                    if not i[0]:
                        good += 1
                if good != 2:
                    all += 1

                if all != 0:
                    the_list.append(p_id)
            if len(the_list) != 0:
                msg = "done"
                print(msg)
                print(len(the_list))
                return render_template('d_viewp_m.html', username=username, result=the_list, messages=msg,
                                       userRole=userRole)
            else:
                print("NULL")
                msg = "none"
                return render_template('d_viewp_m.html', username=username, messages=msg, userRole=userRole)

        if right == "1" and recover == "1":
            sql3 = "SELECT distinct area FROM location WHERE location.d_id = '%s'" % username
            cursor.execute(sql3)
            db.commit()
            res = cursor.fetchall()
            print(res[0])
            if res[0][0] != '1':
                msg = "none"
                return render_template('d_viewp_m.html', messages=msg, username=username)
            # 检验3天体温和2次核酸
            # for loop 找pid
            areaa = res[0][0]

            if areaa == '1':
                pos = '轻症'
            elif areaa == '2':
                pos = '重症'
            else:
                pos = '危重症'

            sql2 = "SELECT * FROM patient WHERE patient.p_id = some(SELECT p_id FROM location WHERE location.area = '%s' and location.area != 0) and patient.severity != '%s'" % (
                areaa, pos)
            cursor.execute(sql2)
            db.commit()
            all_p_id = cursor.fetchall()
            the_list = []
            for p_id in all_p_id:

                sql1 = "SELECT temperature FROM daily_info WHERE daily_info.p_id = %s  ORDER BY the_date DESC" % p_id[0]
                cursor.execute(sql1)
                db.commit()
                print("查询成功")
                res = cursor.fetchall()
                print(res)
                good = 0
                counter = 0
                if len(res) < 3:
                    continue
                for i in res:
                    if counter > 2:
                        break
                    counter += 1
                    if i[0] < '37.3':
                        good += 1
                if good != 3:
                    continue
                sql2 = "SELECT result FROM covid_test WHERE covid_test.p_id = '%s'  ORDER BY the_date DESC" % p_id[0]
                cursor.execute(sql2)
                db.commit()
                print("查询成功2")
                res = cursor.fetchall()
                print(res)
                good = 0
                counter = 0
                if len(res) < 2:
                    continue
                for i in res:
                    if counter > 1:
                        break
                    counter += 1
                    if not i[0]:
                        good += 1
                if good != 2:
                    continue
                the_list.append(p_id)
            if len(the_list) != 0:
                msg = "done"
                print(msg)
                print(len(the_list))
                return render_template('d_viewp_m.html', username=username, result=the_list, messages=msg,
                                       userRole=userRole)
            else:
                print("NULL")
                msg = "none"
                return render_template('d_viewp_m.html', username=username, messages=msg, userRole=userRole)

        if right == "0" and recover == "1":
            sql3 = "SELECT distinct area FROM location WHERE location.d_id = '%s'" % username
            cursor.execute(sql3)
            db.commit()
            res = cursor.fetchall()
            print(res[0])
            if res[0][0] != '1':
                msg = "none"
                return render_template('d_viewp_m.html', messages=msg, username=username)
            # 检验3天体温和2次核酸
            # for loop 找pid
            areaa = res[0][0]

            if areaa == '1':
                pos = '轻症'
            elif areaa == '2':
                pos = '重症'
            else:
                pos = '危重症'

            sql2 = "SELECT * FROM patient WHERE patient.p_id = some(SELECT p_id FROM location WHERE location.area = '%s' and location.area != 0) and patient.severity = '%s'" % (
                areaa, pos)
            cursor.execute(sql2)
            db.commit()
            all_p_id = cursor.fetchall()
            the_list = []
            for p_id in all_p_id:

                sql1 = "SELECT temperature FROM daily_info WHERE daily_info.p_id = %s  ORDER BY the_date DESC" % p_id[0]
                cursor.execute(sql1)
                db.commit()
                print("查询成功")
                res = cursor.fetchall()
                print(res)
                good = 0
                counter = 0
                if len(res) < 3:
                    continue
                for i in res:
                    if counter > 2:
                        break
                    counter += 1
                    if i[0] < '37.3':
                        good += 1
                if good != 3:
                    continue
                sql2 = "SELECT result FROM covid_test WHERE covid_test.p_id = '%s'  ORDER BY the_date DESC" % p_id[0]
                cursor.execute(sql2)
                db.commit()
                print("查询成功2")
                res = cursor.fetchall()
                print(res)
                good = 0
                counter = 0
                if len(res) < 2:
                    continue
                for i in res:
                    if counter > 1:
                        break
                    counter += 1
                    if not i[0]:
                        good += 1
                if good != 2:
                    continue
                the_list.append(p_id)
            if len(the_list) != 0:
                msg = "done"
                print(msg)
                print(len(the_list))
                return render_template('d_viewp_m.html', username=username, result=the_list, messages=msg,
                                       userRole=userRole)
            else:
                print("NULL")
                msg = "none"
                return render_template('d_viewp_m.html', username=username, messages=msg, userRole=userRole)

    else:
        db = pymysql.connect("localhost", "root", password="20000106", db="Hospital", charset='utf8')
        cursor = db.cursor()
        try:
            cursor.execute("use Hospital")
        except:
            print("Error: unable to use database!")
        # 查询
        sql = "SELECT * FROM patient as p WHERE p_id = some(SELECT p_id FROM location WHERE Location.d_id = '%s')" % username
        cursor.execute(sql)
        res = cursor.fetchall()
        if len(res) != 0:
            msg = "done"
            print(msg)
            print(len(res))
            return render_template('d_viewp_m.html', username=username, result=res, messages=msg,
                                   userRole=userRole)
        else:
            print("NULL")
            msg = "none"
            return render_template('d_viewp_m.html', username=username, messages=msg, userRole=userRole)

@app.route('/hn_viewp_m', methods=['GET', 'POST'])
def hn_viewp_m():
    msg = ""
    if request.form["action"] == "确认条件":
        recover = request.form['recover']
        right = request.form['right']
        print(recover)
        print(right)
        db = pymysql.connect("localhost", "root", password="20000106", db="Hospital", charset='utf8')
        cursor = db.cursor()
        cursor.execute("use Hospital")

        if right == "1" and recover == "0":
            sql3 = "SELECT distinct area FROM location WHERE location.hn_id = '%s'" % username
            cursor.execute(sql3)
            db.commit()
            res = cursor.fetchall()
            print(res[0])

            # 检验3天体温和2次核酸
            # for loop 找pid
            areaa = res[0][0]

            if areaa == '1':
                pos = '轻症'
            elif areaa == '2':
                pos = '重症'
            else:
                pos = '危重症'

            sql2 = "SELECT * FROM patient WHERE patient.p_id = some(SELECT p_id FROM location WHERE location.area = '%s' and location.area != 0) and patient.severity != '%s'" % (
                areaa, pos)
            cursor.execute(sql2)
            db.commit()
            all_p_id = cursor.fetchall()
            the_list = []
            for p_id in all_p_id:

                sql1 = "SELECT temperature FROM daily_info WHERE daily_info.p_id = %s  ORDER BY the_date DESC" % p_id[0]
                cursor.execute(sql1)
                db.commit()
                print("查询成功")
                res = cursor.fetchall()
                print(res)
                good = 0
                counter = 0
                all = 0
                if len(res) < 3:
                    all += 1
                for i in res:
                    if counter > 2:
                        break
                    counter += 1
                    if i[0] < '37.3':
                        good += 1
                if good != 3:
                    all += 1
                sql2 = "SELECT result FROM covid_test WHERE covid_test.p_id = '%s'  ORDER BY the_date DESC" % p_id[0]
                cursor.execute(sql2)
                db.commit()
                print("查询成功2")
                res = cursor.fetchall()
                print(res)
                good = 0
                counter = 0
                if len(res) < 2:
                    all += 1
                for i in res:
                    if counter > 1:
                        break
                    counter += 1
                    if not i[0]:
                        good += 1
                if good != 2:
                    all += 1

                if all != 0:
                    the_list.append(p_id)
            if len(the_list) != 0:
                msg = "done"
                print(msg)
                print(len(the_list))
                return render_template('hn_viewp_m.html', username=username, result=the_list, messages=msg,
                                       userRole=userRole)
            else:
                print("NULL")
                msg = "none"
                return render_template('hn_viewp_m.html', username=username, messages=msg, userRole=userRole)

        if right == "0" and recover == "0":
            sql3 = "SELECT distinct area FROM location WHERE location.hn_id = '%s'" % username
            cursor.execute(sql3)
            db.commit()
            res = cursor.fetchall()
            print(res[0])

            # 检验3天体温和2次核酸
            # for loop 找pid
            areaa = res[0][0]

            if areaa == '1':
                pos = '轻症'
            elif areaa == '2':
                pos = '重症'
            else:
                pos = '危重症'

            sql2 = "SELECT * FROM patient WHERE patient.p_id = some(SELECT p_id FROM location WHERE location.area = '%s' and location.area != 0) and patient.severity = '%s'" % (
                areaa, pos)
            cursor.execute(sql2)
            db.commit()
            all_p_id = cursor.fetchall()
            the_list = []
            for p_id in all_p_id:

                sql1 = "SELECT temperature FROM daily_info WHERE daily_info.p_id = %s  ORDER BY the_date DESC" % p_id[0]
                cursor.execute(sql1)
                db.commit()
                print("查询成功")
                res = cursor.fetchall()
                print(res)
                good = 0
                counter = 0
                all = 0
                if len(res) < 3:
                    all += 1
                for i in res:
                    if counter > 2:
                        break
                    counter += 1
                    if i[0] < '37.3':
                        good += 1
                if good != 3:
                    all += 1
                sql2 = "SELECT result FROM covid_test WHERE covid_test.p_id = '%s'  ORDER BY the_date DESC" % p_id[0]
                cursor.execute(sql2)
                db.commit()
                print("查询成功2")
                res = cursor.fetchall()
                print(res)
                good = 0
                counter = 0
                if len(res) < 2:
                    all += 1
                for i in res:
                    if counter > 1:
                        break
                    counter += 1
                    if not i[0]:
                        good += 1
                if good != 2:
                    all += 1

                if all != 0:
                    the_list.append(p_id)
            if len(the_list) != 0:
                msg = "done"
                print(msg)
                print(len(the_list))
                return render_template('hn_viewp_m.html', username=username, result=the_list, messages=msg,
                                       userRole=userRole)
            else:
                print("NULL")
                msg = "none"
                return render_template('hn_viewp_m.html', username=username, messages=msg, userRole=userRole)

        if right == "1" and recover == "1":
            sql3 = "SELECT distinct area FROM location WHERE location.hn_id = '%s'" % username
            cursor.execute(sql3)
            db.commit()
            res = cursor.fetchall()
            print(res[0])
            if res[0][0] != '1':
                msg = "none"
                return render_template('hn_viewp_m.html', messages=msg, username=username)
            # 检验3天体温和2次核酸
            # for loop 找pid
            areaa = res[0][0]

            if areaa == '1':
                pos = '轻症'
            elif areaa == '2':
                pos = '重症'
            else:
                pos = '危重症'

            sql2 = "SELECT * FROM patient WHERE patient.p_id = some(SELECT p_id FROM location WHERE location.area = '%s' and location.area != 0) and patient.severity != '%s'" % (
                areaa, pos)
            cursor.execute(sql2)
            db.commit()
            all_p_id = cursor.fetchall()
            the_list = []
            for p_id in all_p_id:

                sql1 = "SELECT temperature FROM daily_info WHERE daily_info.p_id = %s  ORDER BY the_date DESC" % p_id[0]
                cursor.execute(sql1)
                db.commit()
                print("查询成功")
                res = cursor.fetchall()
                print(res)
                good = 0
                counter = 0
                if len(res) < 3:
                    continue
                for i in res:
                    if counter > 2:
                        break
                    counter += 1
                    if i[0] < '37.3':
                        good += 1
                if good != 3:
                    continue
                sql2 = "SELECT result FROM covid_test WHERE covid_test.p_id = '%s'  ORDER BY the_date DESC" % p_id[0]
                cursor.execute(sql2)
                db.commit()
                print("查询成功2")
                res = cursor.fetchall()
                print(res)
                good = 0
                counter = 0
                if len(res) < 2:
                    continue
                for i in res:
                    if counter > 1:
                        break
                    counter += 1
                    if not i[0]:
                        good += 1
                if good != 2:
                    continue
                the_list.append(p_id)
            if len(the_list) != 0:
                msg = "done"
                print(msg)
                print(len(the_list))
                return render_template('hn_viewp_m.html', username=username, result=the_list, messages=msg,
                                       userRole=userRole)
            else:
                print("NULL")
                msg = "none"
                return render_template('hn_viewp_m.html', username=username, messages=msg, userRole=userRole)

        if right == "0" and recover == "1":
            sql3 = "SELECT distinct area FROM location WHERE location.hn_id = '%s'" % username
            cursor.execute(sql3)
            db.commit()
            res = cursor.fetchall()
            print(res[0])
            if res[0][0] != '1':
                msg = "none"
                return render_template('hn_viewp_m.html', messages=msg, username=username)
            # 检验3天体温和2次核酸
            # for loop 找pid
            areaa = res[0][0]

            if areaa == '1':
                pos = '轻症'
            elif areaa == '2':
                pos = '重症'
            else:
                pos = '危重症'

            sql2 = "SELECT * FROM patient WHERE patient.p_id = some(SELECT p_id FROM location WHERE location.area = '%s' and location.area != 0) and patient.severity = '%s'" % (
                areaa, pos)
            cursor.execute(sql2)
            db.commit()
            all_p_id = cursor.fetchall()
            the_list = []
            for p_id in all_p_id:

                sql1 = "SELECT temperature FROM daily_info WHERE daily_info.p_id = %s  ORDER BY the_date DESC" % p_id[0]
                cursor.execute(sql1)
                db.commit()
                print("查询成功")
                res = cursor.fetchall()
                print(res)
                good = 0
                counter = 0
                if len(res) < 3:
                    continue
                for i in res:
                    if counter > 2:
                        break
                    counter += 1
                    if i[0] < '37.3':
                        good += 1
                if good != 3:
                    continue
                sql2 = "SELECT result FROM covid_test WHERE covid_test.p_id = '%s'  ORDER BY the_date DESC" % p_id[0]
                cursor.execute(sql2)
                db.commit()
                print("查询成功2")
                res = cursor.fetchall()
                print(res)
                good = 0
                counter = 0
                if len(res) < 2:
                    continue
                for i in res:
                    if counter > 1:
                        break
                    counter += 1
                    if not i[0]:
                        good += 1
                if good != 2:
                    continue
                the_list.append(p_id)
            if len(the_list) != 0:
                msg = "done"
                print(msg)
                print(len(the_list))
                return render_template('hn_viewp_m.html', username=username, result=the_list, messages=msg,
                                       userRole=userRole)
            else:
                print("NULL")
                msg = "none"
                return render_template('hn_viewp_m.html', username=username, messages=msg, userRole=userRole)

    else:
        db = pymysql.connect("localhost", "root", password="20000106", db="Hospital", charset='utf8')
        cursor = db.cursor()
        try:
            cursor.execute("use Hospital")
        except:
            print("Error: unable to use database!")
        # 查询
        sql = "SELECT * FROM patient as p WHERE p_id = some(SELECT p_id FROM location WHERE Location.hn_id = '%s')" % username
        cursor.execute(sql)
        res = cursor.fetchall()
        if len(res) != 0:
            msg = "done"
            print(msg)
            print(len(res))
            return render_template('hn_viewp_m.html', username=username, result=res, messages=msg,
                                   userRole=userRole)
        else:
            print("NULL")
            msg = "none"
            return render_template('hn_viewp_m.html', username=username, messages=msg, userRole=userRole)

if __name__ == '__main__':
    app.run(host='localhost', port='9090')
