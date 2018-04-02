import os
from flask import *
import pandas as pd
app = Flask(__name__)

APP_ROOT = os.path.dirname(os.path.abspath(__file__))

def calculateBudget(fileName):
    import pandas as pd
    data = pd.read_csv(fileName, encoding = "ISO-8859-1", delimiter=";")
    data = data.stack().str.replace(",", ".").unstack()
    food_stores = ["kvickly", "fdb", "rema", "kantine", "netto", "coop", "meny", "texas", "gudhjem", "restaurant", "fisk"]
    food_rows = data[data.Tekst.str.lower().str.contains("|".join(food_stores))]
    total = abs(sum(food_rows.Beløb.astype(float)))
    avg = total / 12
    return [int(total), int(avg)]

@app.route('/')
def index():
    return render_template('index.html')


@app.route('/upload', methods = ['POST'])
def upload():
    target = os.path.join(APP_ROOT, 'uploads/')

    if not os.path.isdir(target):
        os.mkdir(target)

    file = request.files["file"]
    destination = '/'.join([target, file.filename])
    file.save(destination)

    budget = calculateBudget(destination)

    return '''<p>Penge brugt på mad i alt: {} kr</p>
            <p>Gennemsnit pr. måned: {} kr</p>'''.format(budget[0], budget[1])

if __name__ == '__main__':
    app.run(debug = True)
