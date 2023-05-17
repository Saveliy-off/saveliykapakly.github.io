from flask import Flask, render_template, request, redirect
from datetime import datetime
from calendar import monthrange

app = Flask(__name__)

def calck(day,summ, precent, months):
    precent = precent * 0.010000
    overpayment = (precent/12*((1+precent/12))**months)/(((1+precent/12)**months)-1)
    ej = summ * overpayment
    t4 = precent/12
    pereplata = ej*months-summ
    return [round(ej, 2), round(pereplata, 2), round(pereplata + summ ,2), summ, months]

def grafic(day,summ, precent, months):
    precent = precent * 0.010000
    overpayment = (precent/12*((1+precent/12))**months)/(((1+precent/12)**months)-1)
    ej = summ * overpayment
    t4 = precent/365
    pereplata = ej*months
    pv = summ
    ps = summ
    pr = pereplata
    pg = pereplata - summ
    pc = precent
    ap = []
    month = 5
    monthz = 4
    for i in range(months):
        days = monthrange(2023, month)[1]
        dayz = monthrange(2023, monthz)[1]
        pd = ps*t4*(dayz-days+days)
        # print(dayz-days+days)
        # kd = ej-pd
        if ej > ps:
            zed = kd
            kd = (summ + ps) - summ
            pd = (pereplata + pg) - pereplata
            # pd += zed - kd
            ps -= kd
        else:
            kd = ej-pd
            ps -= kd
        pg -= pd
        ez = kd + pd
        pr -= ez
        ap.append([round(ps, 2), round(kd, 2), round(pd, 2), round(ez, 2), i+1, round(pv, 2), ez])
        pv -= kd
    
    obs = 0
    ovs = 0
    dvs = 0
    for i in range(months):
        obs += ap[i][2]
        ovs += ap[i][1]
        dvs += ap[i][6]
    ap.append([round(obs, 2), round(ovs), round(dvs, 2)])
    return ap
        


@app.route('/')
def index():
    return redirect('/credit')

@app.route('/credit')
def credit():
    return render_template('credit.html')

@app.route('/calendar', methods=['GET', 'POST'])
def calendar():
    if request.method == 'POST':
        summ = request.form.get('exampleInputSumm')
        precent = request.form.get('exampleInputPrecent')
        months = request.form.get('exampleInputMonths')
        date = request.form.get('exampleInputDate')
        summ = int(summ)
        precent = float(precent)
        months = int(months)
        sd = calck(date, summ, precent, months)
        gr = grafic(date, summ, precent, months)
    return render_template('calendar.html', sd=sd, gr=gr)

if __name__ == '__main__':
    app.run(debug=True)