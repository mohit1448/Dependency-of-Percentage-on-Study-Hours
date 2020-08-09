

import numpy as np
from flask import Flask, request, jsonify, render_template
import pickle

app = Flask(__name__)
app = Flask(__name__, template_folder='template')
model = pickle.load(open('model.pkl', 'rb'))
app.static_folder = 'static'

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/predict',methods=['POST'])
def predict():
    '''
    For rendering results on HTML GUI
    '''
    int_features = [float(x) for x in request.form.values()]
    final_features = [np.array(int_features)]
    prediction = model.predict(final_features)

    output = prediction[0]
    if (output > 100):
        output = 100
    if (int_features[0] > 24):
        return render_template('index.html', prediction_text='Enter a value in the range of (0 to 24)')
    elif (int_features[0] < 0):
        return render_template('index.html', prediction_text='Enter a value in the range of (0 to 24)')
    else:
        return render_template('index.html', prediction_text='Expected percentage for {} hours study is {}'.format(int_features[0],output))
        
    

@app.route('/predict_api',methods=['POST'])
def predict_api():
    '''
    For direct API calls trought request
    '''
    data = request.get_json(force=True)
    prediction = model.predict([np.array(list(data.values()))])

    output = prediction[0]
    return jsonify(output)

if __name__ == "__main__":
    app.run(debug=True)
