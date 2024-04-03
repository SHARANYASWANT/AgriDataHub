const express = require('express');
const bodyParser = require('body-parser');

const app = express();
const port = 3000;

// Set the view engine to EJS
app.set('view engine', 'ejs');

// Middleware to serve static files
app.use(express.static('public'));

// Middleware to parse JSON bodies
app.use(bodyParser.json());

// Initialize variables to store sensor data
let currentWeather = {}; 

// Route to handle incoming POST requests from ESP8266
app.post('/data', (req, res) => {
  // Extract sensor data from the request body
  const { humidity, temperature, soil_moisture } = req.body;

  // Store the current weather data
  currentWeather = {
    "humidity": humidity,
    "temperature": temperature,
    "soil_moisture": soil_moisture
  };

  // Log the received sensor data
  console.log(Received sensor data - Humidity: ${humidity}%, Temperature: ${temperature}°C, Soil Moisture: ${soil_moisture});

  // Send a success response
  res.sendStatus(200);
});
data = {
  "humidity": 60,
  "temperature": 29,
  "soil_moisture": 57
};

// Route to display the current weather
app.get('/', (req, res) => {
  // Provide default values if currentWeather is empty
  const { humidity = '', temperature = '', soil_moisture = '' } = currentWeather;

  res.render("index.ejs", data);
});

// Start the server
app.listen(port, () => {
  console.log(Server is running on http://localhost:${port});
});
