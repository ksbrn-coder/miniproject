import os

from flask import Flask, render_template, session, redirect, url_for
from common import Session
from domain import Member
from service import MemberService

app = Flask(__name__)
app.secret_key = '1234535'

@app.route('/')
def index():
    # 세션에 저장된 user_name이 있는지 확인 (없으면 None)
    user_name = session.get('user_name')
    return render_template('index.html', user_name=user_name)

# 마이페이지 라우터 추가
@app.route('/mypage')
def mypage():
    if 'user_name' not in session:
        return redirect(url_for('login')) # 로그인 안 되어 있으면 로그인 창으로
    return render_template('mypage.html')