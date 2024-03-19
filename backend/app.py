from flask import Flask, request, jsonify
from flask_cors import cross_origin
from flask_cors import CORS
from email_classification import MultinomialNB_EmailClassification

model = MultinomialNB_EmailClassification("")
model.load_model('./email_classification_model')
app = Flask(__name__)
CORS(app)

@app.route('/predict', methods=['POST'])
@cross_origin()
def predict():
    # Get the JSON data from the request
    json_data = request.json
    email_content = []
    email_content.append(json_data['Subject'])
    email_content.append(json_data['Body'])
    return jsonify({'type': model.predict(email_content)})
   
if __name__ == '__main__':
    app.run(debug=True)