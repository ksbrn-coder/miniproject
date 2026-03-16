import os

from flask import Flask, render_template, session, redirect, url_for, request
from common import Session
from domain import Member
from service import MemberService

app = Flask(__name__)
app.secret_key = '1234535'


@app.route('/')
def index():
    # 세션에 저장된 user_name이 있는지 확인 (없으면 None)
    user_name = session.get('user_name')
    return render_template('main.html', user_name=user_name)


@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'GET':
        return render_template('login.html')

    uid = request.form['uid']
    upw = request.form['upw']
    print("/login에서 넘어온 폼 데이터 출력 테스트")
    print(uid, upw)
    print("===============================")

    conn = Session.get_connection()
    try:
        with conn.cursor() as cursor:
            sql = "SELECT id, name, uid, role   \
                FROM members WHERE uid = %s AND password = %s"
            cursor.execute(sql, (uid, upw))
            user = cursor.fetchone()

            if user:
                session["user_id"] = user['id']
                session["user_name"] = user['name']
                session["user_uid"] = user['uid']
                session["user_role"] = user['role']

                return redirect(url_for('main'))

            else:
                return "<script>alert('아이디나 비밀번호가 일치하지 않습니다.');history.back();</script>"

    finally:
        conn.close()


@app.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('login'))


@app.route('/join', methods=['GET', 'POST'])
def join():
    if request.method == 'GET':
        return render_template('join.html')

    uid = request.form.get('uid')
    password = request.form.get('password')
    name = request.form.get('name')

    conn = Session.get_connection()
    try:
        with conn.cursor() as cursor:
            cursor.execute("SELECT id FROM members WHERE uid = %s", (uid,))
            if cursor.fetchone():
                return "<script>alert('이미 존재하는 아이디입니다.');history.back();</script>"

            sql = "INSERT INTO members (uid, password, name) VALUES (%s, %s, %s)"
            cursor.execute(sql, (uid, password, name))
            conn.commit()

            return "<script>alert('회원가입이 완료되었습니다!'); location.href = '/login';</script>"

    except Exception as e:
        print(f"회원가입 에러 : {e}")
        return "가입 중 오류가 발생했습니다. /n join() 메서드를 확인하세요!!!"

    finally:
        conn.close()


# 마이페이지 라우터 추가
@app.route('/member/edit')
def edit():
    if 'user_name' not in session:
        return redirect(url_for('login'))  # 로그인 안 되어 있으면 로그인 창으로
    return render_template('mypage.html')


@app.route('/member/delete/<int:member_id>', methods=['GET'])
def delete_member(member_id):
    # 1. 전달받은 member_id를 사용해 DB에서 회원 삭제 로직 실행
    # (예: MemberService.delete(member_id))
    print(f"회원 번호 {member_id}를 삭제합니다.")

    # 2. 삭제 후 메인 화면이나 목록으로 돌아가기
    return redirect(url_for('index'))


@app.route('/')
def main():
    return render_template('main.html')


if __name__ == '__main__':
    app.run(host='192.168.0.172', port=5019, debug=True)
