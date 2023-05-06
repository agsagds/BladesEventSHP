from flask import Flask, redirect, url_for, jsonify, request, render_template
import time
import config as cfg
from functools import wraps

app = Flask(__name__)
swarm_stage = 0
visitors = []
errs_count = 0

@app.route('/room<int:room_id>')
def room(room_id:int):
    
    if room_id<=0:
        return render_template('frontal_door.html')
    if room_id>12:
        return render_template('window.html')
    if room_id%4==0:
        if room_id<8:
            return render_template('staff_room.html')
        else:
            return render_template('bathroom.html')
    if room_id%3==0:
        return render_template('empty_clerk_room.html')
    #1,2,5,7,10,11
    if room_id==1:
        return render_template('key_room.html', cows=0, bulls=0, path="check_key_1")
    if room_id==2:
        return render_template('key_room.html', cows=0, bulls=0, path="check_key_2")
    if room_id==5:
        return render_template('key_room.html', cows=0, bulls=0, path="check_key_3")
    if room_id==7:
        return render_template('magic_room.html')
    if room_id==10:
        return render_template('mayor_s_room.html')
    if room_id==11:
        return render_template('key_room.html', cows=0, bulls=0, path="check_key_4")
    return KeyError


@app.route('/check_magic', methods=['GET', 'POST'])
def check_magic():
    default_value = '0'
    #check magic squre
    nums = [str(i) for i in range(1,17)]
    s = [int(request.form.get(f'num{i}', default_value)) for i in nums]
    s1 = s[0]+s[1]+s[2]+s[3]
    s2 = s[0]+s[4]+s[8]+s[12]
    s3 = s[0]+s[5]+s[10]+s[15]
    s4 = s[3]+s[7]+s[11]+s[15]
    s5 = s[3]+s[6]+s[9]+s[12]
    if len(set(s))==len(s) and s1==s2 and s1==s3 and s1==s4 and s1==s5:
        return render_template('mayor_s_room.html')
    else:
        return redirect(url_for('room', room_id=7))


def get_bulls_and_cows(ans, value):
    bulls = 0
    cows = 0
    for i in range(len(ans)):
        if ans[i] == value[i]:
            bulls += 1
            value[i] = '#'
    for i in value:
        if i in ans:
            cows += 1
    return bulls, cows

@app.route('/check_key_1', methods=['GET', 'POST'])
def check_key_1():
    default_value = '0'
    nums = [0,1,2,3]
    key = [request.form.get(f'num{i}', default_value) for i in nums]
    if ''.join(key)==cfg.KEY_1:
        return redirect(url_for('room', room_id=3))
    bulls, cows = get_bulls_and_cows(ans=cfg.KEY_1, value=key)
    return render_template('key_room.html', bulls=bulls, cows=cows, path="check_key_1")


@app.route('/check_key_2', methods=['GET', 'POST'])
def check_key_2():
    default_value = '0'
    nums = [0,1,2,3]
    key = [request.form.get(f'num{i}', default_value) for i in nums]
    if ''.join(key)==cfg.KEY_2:
        return redirect(url_for('room', room_id=4))
    bulls, cows = get_bulls_and_cows(ans=cfg.KEY_2, value=key)
    return render_template('key_room.html', bulls=bulls, cows=cows, path="check_key_2")


@app.route('/check_key_3', methods=['GET', 'POST'])
def check_key_3():
    default_value = '0'
    nums = [0,1,2,3]
    key = [request.form.get(f'num{i}', default_value) for i in nums]
    if ''.join(key)==cfg.KEY_3:
        return redirect(url_for('room', room_id=10))
    bulls, cows = get_bulls_and_cows(ans=cfg.KEY_1, value=key)
    return render_template('key_room.html', bulls=bulls, cows=cows, path="check_key_3")


@app.route('/check_key_4', methods=['GET', 'POST'])
def check_key_4():
    default_value = '0'
    nums = [0,1,2,3]
    key = [request.form.get(f'num{i}', default_value) for i in nums]
    if ''.join(key)==cfg.KEY_4:
        return render_template('invoice.html')
    bulls, cows = get_bulls_and_cows(ans=cfg.KEY_4, value=key)
    return render_template('key_room.html', bulls=bulls, cows=cows, path="check_key_4")



@app.route("/")
def index():
    return render_template('rooms.html')


def get_question_part(pos):
    question = cfg.SWARM_QUESTIONS[swarm_stage]
    q_part_len = len(question)//cfg.TEAM_SIZE
    q_part = question[pos*q_part_len:(pos+1)*q_part_len]
    return q_part


@app.route("/swarm")
def swarm():
    if swarm_stage == 3:
        return redirect(url_for('final'))
    
    client_addr = request.remote_addr
    if client_addr not in visitors:
        visitors.append(client_addr)
    pos = visitors.index(client_addr)
    q_part = get_question_part(pos)
    return render_template('swarm.html', question = q_part, is_leader = (pos+1==cfg.TEAM_SIZE), errors = errs_count)


@app.route("/get_swarm_stage")
def get_swarm_stage():
    return jsonify({'stage': swarm_stage})


@app.route("/check_swarm<string:value>")
def check_swarm(value):
    if value==cfg.SWARM_ANSWERS[swarm_stage]:
        swarm_stage += 1
        visitors.clear()
    else:
        errs_count += 1
    return redirect(url_for('swarm'))


@app.route("/final")
def final():
    return render_template('final.html')

# Run the application
if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=8080)
