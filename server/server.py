import joblib
from flask import Flask, request, jsonify
from flask_cors import CORS, cross_origin

app = Flask(__name__)

# Enable CORS
CORS(app)
app.config['CORS_HEADERS'] = 'Content-Type'

@app.route('/')
@cross_origin()
def home():
    return "Let's build a flight delay prediction api!"

# Load the model (ensure the path to your model file is correct)
model = joblib.load('model.pkl')

@app.route('/predict', methods=['GET'])
@cross_origin()
def predict():
    try:
        # Extract input parameters
        airport_id = request.args.get('airport_id')
        day_of_week = request.args.get('day_of_week')
        
        # Ensure the input parameters are valid integers
        if airport_id is None or day_of_week is None:
            raise ValueError("Missing required query parameters: 'airport_id' and 'day_of_week'")
        
        airport_id = int(airport_id)
        day_of_week = int(day_of_week)
        
        # Ensure the input is a 2D array
        input_data = [[day_of_week, airport_id]]
        
        # Make prediction
        prediction = model.predict_proba(input_data)
        prediction_list = prediction[0].tolist()

        confident_not_delayed, delayed = prediction_list
        return jsonify({
            'confident_not_delayed': confident_not_delayed,
            'delayed': delayed
        })
    except Exception as e:
        return jsonify({'error': str(e)})

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
