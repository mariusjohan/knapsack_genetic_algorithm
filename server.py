from flask import (
    Flask,
    request,
    redirect,
    render_template
)

import opt_knapsack_v2

app = Flask(__name__)

max_fitness_score = []
avg_fitness_score = []
min_fitness_score = []
labels = []

gene_size = 200
mutat_risk = 0.005
weight_size = 5000

agent = None

# Initialiser algoritmen
opt_knapsack_v2.create_agent(gene_size, mutat_risk, weight_size)

@app.route('/')
def index():
    return redirect('settings')

@app.route('/settings/', methods=['GET', 'POST'])
def settings():
    if request.method == 'POST':
        gen_size = request.form.get('gen_size')
        mut_risk = request.form.get('mutation_risk')
        backpack_size = request.form.get('max_weight')

        try:
            global gene_size
            global mutat_risk
            global weight_size
            gene_size = int(gen_size)
            mutat_risk = float(mut_risk)
            weight_size = int(backpack_size)
            return redirect('/reset')
        except Exception as e:
            print(e)
            return render_template('settings.html', error = 'Fejl i indtastninng')

    return render_template('settings.html')

@app.route('/run')
def run():
    global labels
    max_value, min_value, avg_value, max_weight, item_string = opt_knapsack_v2.get_next_valueset()
    max_fitness_score.append(max_value)
    min_fitness_score.append(min_value)
    avg_fitness_score.append(avg_value)
    

    if len(labels) == 0:
        labels = [0]
    else:
        labels.append(labels[-1] + 1)

    return render_template(
        'home.html',
        labels = labels,
        max_fitness_score = max_fitness_score,
        avg_fitness_score = avg_fitness_score,
        min_fitness_score = min_fitness_score,
        item_string = item_string,
        max_value = max_value,
        max_weight = max_weight
    )

@app.route('/reset')
def reset():
    global agent, max_fitness_score, avg_fitness_score, min_fitness_score, labels

    global gene_size
    global mutat_risk
    global weight_size
    opt_knapsack_v2.create_agent(gene_size, mutat_risk, weight_size)

    max_fitness_score = []
    avg_fitness_score = []
    min_fitness_score = []
    labels = []
    return redirect('/run')


if __name__ == '__main__':
    app.run(debug=True)