# -*- coding: utf-8 -*-
from flask import Flask
from flask import request
from flask import render_template
import include.database as dt

app=Flask(__name__)

st_username=str()
st_password=str()

def retable(tablename,thrick='*'):
    sql="select %s from %s" % (thrick,tablename)
    dt.cursor.execute(sql)
    head=dt.cursor.description
    body=dt.cursor.fetchall()
    resul=str()
    if len(body)==0:
        return resul
    else:
        resul+='<tr>'
        for x in head:
            resul+='<th>'+x[0]+'</th>'
        resul+='</tr>'
        for y in body:
            resul+='<tr>'
            for o in y:
                if o==None:
                    resul+='<td>'+'Null'+'</td>'
                else:
                    resul+='<td>'+str(o)+'</td>'
            resul+='</tr>'
    return resul

def sqlable(proname):
    dt.cursor.callproc(proname)
    body=dt.cursor.stored_results()
    resul=str()
    for y in body:
        resul+='<tr>'
        for o in y.fetchall():
            if o==None:
                resul+='<td>'+'Null'+'</td>'
            else:
                for v in o:
                    resul+='<td>'+str(v)+'</td>'
        resul+='</tr>'
    return resul

@app.route('/',methods=['GET'])
def home():
    return render_template("demo.html")



rk_ftd='show tables;'
rk_text=str()
rk_bl=False  #标志是否为一个返回页面的标志

@app.route('/util',methods=['GET'])
def operhome():
    global rk_ftd,rk_text,rk_bl
    rk_bl=False
    return render_template("operator.html",ftd=rk_ftd,text=rk_text)

@app.route('/util',methods=['GET','POST'])
def operator():
    global rk_ftd,rk_text,rk_bl
    rk_bl=True
    mess=request.form['message']
    stk=dt.op(mess)
    rk_text=stk
    rk_ftd=mess
    return render_template("operator.html",text=stk,ftd=mess)


#如何让一个URL不能被浏览器直接访问
@app.route('/local',methods=['GET'])
def local():
    global st_username,rk_bl
    ls=str()
    dt.cursor.execute('select name from graduates where student_ID= %s',(st_username,))
    nameturn=dt.cursor.fetchall()
    taname='graduates left outer join (Employed_students natural join work) \
            on graduates.student_ID=Employed_students.student_ID'
    if len(nameturn) > 0 :
        ls=nameturn[0][0]
    else:
        ls=st_username
    sql="select identity from login where username='%s'" % (st_username)
    dt.cursor.execute(sql)
    ident=dt.cursor.fetchall()
    if ident[0][0]=='root':
        return render_template("signin-ok.html",username=ls,utable=retable(taname)
                               ,procedure1=sqlable("query"),
                               procedure2=sqlable("pr_query"),endk=rk_bl)
    else:
        taname="graduates left outer join (Employed_students natural join work) \
               on graduates.student_ID=Employed_students.student_ID where \
               graduates.student_ID='%s'" \
               % (st_username)
        thricx='graduates.student_ID,Employed_students.work_ID,work.company, \
                work.work_type,graduates.college,graduates.major,graduates.sex'
        return render_template("normal.html",username=ls,utable=retable(taname,thricx))

# post表示浏览器告诉服务器：想在 URL 上 发布新信息。并且，服务器必须确保
# 数据已存储且仅存储一次。这是 HTML表单通常发送数据到服务器的方法。
@app.route('/',methods=['GET','POST'])
def signin():
    global st_password,st_username
    st_username = request.form['username']
    st_password = request.form['password']
    dt.cursor.execute('select password from login where username = %s', (st_username,))
    passturn=dt.cursor.fetchall()
    if len(passturn) > 0 and str(passturn[0][0])==str(st_password):
        return render_template("sty.html", web='/local')
    return render_template("demo.html", message='Bad username or password', username=st_username)


if __name__=='__main__':
    app.run()

