from flask import Flask, render_template
import pandas as pd
import numpy as np
from sklearn.linear_model import LinearRegression
from sklearn.model_selection import train_test_split

app = Flask(__name__)

# Function to generate predictions
def generate_predictions():
    # Read data from CSV file
    data = pd.read_csv('final1.csv')

    # Assuming your data has columns 'date', 'temperature', 'surface_pressure', 'wind_speed', 'humidity'
    X = data[['date']]  # Input features
    y = data[['temperature', 'surface_pressure', 'wind speed', 'humidity']]  # Target variables

    # Convert the 'date' column to datetime format
    data['date'] = pd.to_datetime(data['date'])

    # Extract the number of days since the minimum date in the dataset
    data['days_since_min_date'] = (data['date'] - data['date'].min()).dt.days

    # Use the 'days_since_min_date' column as the input feature
    X = data[['days_since_min_date']]

    # Split the data into training and testing sets
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

    # Create a dictionary to store models for each target variable
    models = {}

    # Train separate Linear Regression models for each target variable
    for column in y.columns:
        model = LinearRegression()
        model.fit(X_train, y_train[column])
        models[column] = model

    # Set start date to today's date
    start_date = pd.Timestamp.today().date()

    # To predict future data, set the start date to today's date
    future_dates = pd.date_range(start=start_date, periods=10, freq='D')  # Ten days in the future

    # Convert the 'date' column to datetime format
    future_X = pd.DataFrame(future_dates, columns=['date'])

    # Extract the number of days since the minimum date in the future dates
    future_X['days_since_min_date'] = (future_X['date'] - data['date'].min()).dt.days

    # Use the 'days_since_min_date' column as the input feature for prediction
    future_X = future_X[['days_since_min_date']]

    # Make predictions on the future data for each target variable
    future_predictions = pd.DataFrame({'date': future_dates})

    for column in y.columns:
        # Make predictions
        future_predictions[column] = models[column].predict(future_X)
        
        # Add random noise to the predicted values
        np.random.seed(42)  # Set seed for reproducibility
        noise = np.random.normal(loc=0, scale=1.0, size=len(future_predictions))
        future_predictions[column] += noise
        
        # Round the predicted values to 2 decimal places
        future_predictions[column] = np.round(future_predictions[column], 2)
        
        # Calculate the variation range for each target variable
        variation_range = future_predictions[column].max() - future_predictions[column].min()

    return future_predictions

@app.route('/')
def index():
    # Generate predictions
    future_predictions = generate_predictions()
    # Convert DataFrame to HTML table
    predictions_table = future_predictions.to_html(index=False)
    # Render the template with predictions table
    return render_template('index.html', predictions_table=predictions_table)

if __name__ == '__main__':
    app.run(debug=True)

