from flask import Flask, render_template, request


app = Flask(__name__)

# Load the Naive Bayes model
import pickle

with open('naive_bayes_model1.pkl', 'rb') as model_file:
    loaded_model = pickle.load(model_file)

# Create a function to get recommendations based on Water_Usage_Category
def get_recommendations(Water_Usage_Category):
    if Water_Usage_Category == 0:
        return "Recommendations for Low water usage"
    elif Water_Usage_Category == 1:
        return "Recommendations for Normal water usage"
    elif Water_Usage_Category == 2:
        return "Recommendations for High water usage"

# Define the route for the home page
@app.route('/')
def home():
    return render_template('index_flask.html')

@app.route('/button_click')
def button_click():
    return render_template('index_flask.html')





# Define the route for the prediction form
@app.route('/predict', methods=['POST'])
def predict():
    if request.method == 'POST':
        # Get user input for water usage
        cooking_usage_litres = float(request.form['cooking_usage_litres'])
        bathing_usage_litres = float(request.form['bathing_usage_litres'])
        drinking_usage_litres = float(request.form['drinking_usage_litres'])
        washing_usage_litres = float(request.form['washing_usage_litres'])
        other_usage_litres = float(request.form['other_usage_litres'])

        # Calculate total usage litres
        total_usage_litres = (
            cooking_usage_litres + bathing_usage_litres +
            drinking_usage_litres + washing_usage_litres + other_usage_litres
        )

        # Make predictions for the user input
        predicted_category = loaded_model.predict([[total_usage_litres]])[0]

        # Map the numerical category back to the original labels
        predicted_category_label = {0: 'Low', 1: 'Normal', 2: 'High'}[predicted_category]

        # Get recommendations based on the predicted Water_Usage_Category
        recommendations = get_recommendations(predicted_category)

        return render_template('result.html', predicted_category_label=predicted_category_label, recommendations=recommendations)

if __name__ == '__main__':
    app.run(debug=True)
