# create a basic server using Flask
from flask import Flask, jsonify, request
from flask import Flask, request, jsonify
from flask_cors import CORS, cross_origin
import pickle

app = Flask(__name__)

# Enable CORS
CORS(app)
app.config['CORS_HEADERS'] = 'Content-Type'


@app.route('/')
@cross_origin()
def home():
    return "Let's build a flight delay prediction api!"


# Load the model from the file
model = pickle.load(open('model.pkl', 'rb'))

# Create a route that returns a prediction of flight delay using the model
# the model accepts two params, day of the week and airport id


app = Flask(__name__)


@app.route('/predict', methods=['GET'])
@cross_origin()
def predict():
    try:
        airport_id = int(request.args.get('airport_id'))
        day_of_week = int(request.args.get('day_of_week'))
        prediction = model.predict_proba([[day_of_week, airport_id]])
        prediction_list = prediction[0].tolist()

        # split the prediction into two variables
        # the first value is the probability of the flight not being delayed
        # the second value is the probability of the flight being delayed
        confident_not_delayed, delayed = prediction_list

        # convert the prediction to a percentage and make it 0 decimal places
        confident_not_delayed = int(round(confident_not_delayed * 100, 0))
        delayed = int(round(delayed * 100, 0))

        print(confident_not_delayed, delayed)

        return jsonify(
            {
                'model_prediction': prediction_list,
                'confidence_percent': confident_not_delayed,
                'delayed_percent': delayed,
                'interpretation': 'There is a {:.0f}% chance that your flight will be delayed. We are {:.0f}% confident.'.format(delayed, confident_not_delayed)
            })
    except Exception as e:
        return jsonify({'error': str(e)}), 400

# Create a GET route that returns the list of airports
# the list of airports is stored in a file called origion_airports.csv


@app.route('/airports', methods=['GET'])
@cross_origin()
def airports():
    try:
        with open('origin_airport.csv', 'r') as f:
            airports = f.read().splitlines()

            # remove first line of airports
            airports.pop(0)

            # split the airports into a list of dictionaries
            airports = [airport.split(',') for airport in airports]
            airports = [{'id': int(airport[0]), 'name': airport[1]}
                        for airport in airports]

            # sort alphabetically
            airports = sorted(airports, key=lambda k: k['name'])

        return jsonify(
            {
                'airports': airports
            })
    except Exception as e:
        return jsonify({'error': str(e)}), 400


if __name__ == '__main__':
    app.run(debug=True)
