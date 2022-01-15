from flask import (
    Flask,
    request,
    redirect,
    render_template
)

app = Flask(__name__)

max_fitness_score = [1,2,3,4,5]
avg_fitness_score = [1,2,4,8,10]
labels = [1,2,3,4,5]

generation_size = 20
mutation_risk = 1

@app.route('/')
def index():
    return redirect('settings')

@app.route('/settings/', methods=['GET', 'POST'])
def settings():
    if request.method == 'POST':
        gen_size = request.form.get('gen_size')
        mut_risk = request.form.get('mutation_risk')

        try:
            gen_size = int(gen_size)
            mut_risk = int(mut_risk)
            return redirect('/reset')
        except:
            return render_template('settings.html', error = 'Alt skal angives i heltal (int)')

    return render_template('settings.html')

@app.route('/run')
def run():
    labels.append(labels[-1] +1)
    max_fitness_score.append(max_fitness_score[-1] +1)
    avg_fitness_score.append((avg_fitness_score[-1] +1)*2)

    return render_template(
        'home.html',
        labels = labels,
        max_fitness_score = max_fitness_score,
        avg_fitness_score = avg_fitness_score
    )

@app.route('/reset')
def reset():
    global max_fitness_score, avg_fitness_score, labels
    max_fitness_score = [0]
    avg_fitness_score = [0]
    labels = [0]

    return redirect('/run')


if __name__ == '__main__':
    app.run(debug=True)