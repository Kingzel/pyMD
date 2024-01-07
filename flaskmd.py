from flask import Flask, render_template, redirect, request, url_for, session
app = Flask(__name__,template_folder='web/html', static_folder='web' )
app.secret_key = 'pymdsecret1234@!!@'

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/logout')
def logout():
    session.clear()
    return redirect(url_for("diagnose"))

@app.route('/about')
def about():
    return render_template('about.html')

@app.route('/diagnose')
def diagnose():
    if 'name' in session:
        print(session["name"])
        return render_template('diagnose.html')
    else:
         return redirect(url_for("start_form"))

@app.route('/start', methods = ['POST','GET'])
def start_form():
        if request.method == 'POST':
             session.permanent = False
             session["name"],session["email"],session["gender"],session["is_send"] = request.form['name'],request.form['email'],request.form['gender'],request.form.get('send-chk')
            #  print(session.values(),session.keys())
             return redirect(url_for("diagnose"))
        else:
            return render_template('formstart.html')


if __name__ == "__main__":
    app.run(debug=True)