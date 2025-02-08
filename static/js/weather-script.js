// Function to capitalize the first letter of a string
function capitalizeFirstLetter(str) {
    return str.charAt(0).toUpperCase() + str.slice(1).toLowerCase();
}

// Function to save a city to localStorage
function saveCityToCache(city) {
    let cachedCities = JSON.parse(localStorage.getItem("cachedCities")) || [];
    if (!cachedCities.includes(city)) {
        cachedCities.push(city);
        localStorage.setItem("cachedCities", JSON.stringify(cachedCities));
        updateCachedCitiesDropdown();
    }
}

// Function to update the dropdown with cached cities
function updateCachedCitiesDropdown() {
    let cachedCities = JSON.parse(localStorage.getItem("cachedCities")) || [];
    let datalist = document.getElementById("cachedCities");
    datalist.innerHTML = ""; // Clear existing options
    cachedCities.forEach(city => {
        let option = document.createElement("option");
        option.value = city;
        datalist.appendChild(option);
    });
}

// Function to check the weather
function checkWeather() {
    let city = document.getElementById("city").value;
    let resultBox = document.getElementById("weatherResult");

    if (city.trim() === "") {
        resultBox.style.display = "block";
        resultBox.innerHTML = "Please enter a city name!";
        return;
    }

    // Show loading indicator
    resultBox.style.display = "block";
    resultBox.innerHTML = `<div class="loading">Loading... ⏳</div>`;

    // Make an API call to the Flask backend
    fetch(`/getweather?city=${city}`)
        .then(response => {
            if (!response.ok) {
                // Handle specific HTTP status codes
                switch (response.status) {
                    case 400:
                        throw new Error("Bad request. Please check the city name.");
                    case 401:
                        throw new Error("Unauthorized request. Invalid API Key.");
                    case 403:
                        throw new Error("Forbidden. Access Denied.");
                    case 404:
                        throw new Error(`City "${city}" not found.`);
                    case 500:
                        throw new Error("Internal Server Error. Please try again later.");
                    case 502:
                        throw new Error("Bad Gateway. Please try again later.");
                    case 503:
                        throw new Error("Service Unavailable. Please try again later.");
                    case 504:
                        throw new Error("Gateway Timeout. Please try again later.");
                    default:
                        throw new Error(`Error: ${response.statusText}`);
                }
            }
            return response.json();
        })
        .then(data => {
            if (data.error) {
                // Display error message from the API
                resultBox.innerHTML = `<strong>Error:</strong> ${data.error}`;
            } else {
                // Weather data
                const weatherDescription = data.weather[0].description;
                const temperature = (data.main.temp - 273.15).toFixed(2); // Convert Kelvin to Celsius
                const humidity = data.main.humidity;
                const windSpeed = data.wind.speed;

                // Set appropriate weather icon based on the description
                let weatherIcon = '';
                if (weatherDescription.includes("clear")) {
                    weatherIcon = "🌞";  // Sunny
                } else if (weatherDescription.includes("cloud")) {
                    weatherIcon = "☁️";  // Cloudy
                } else if (weatherDescription.includes("rain")) {
                    weatherIcon = "🌧️";  // Rainy
                } else if (weatherDescription.includes("snow")) {
                    weatherIcon = "❄️";  // Snowy
                } else if (weatherDescription.includes("storm")) {
                    weatherIcon = "🌩️";  // Stormy
                } else {
                    weatherIcon = "🌤️";  // Default icon
                }

                // Capitalize the first letter of the city
                const capitalizedCity = capitalizeFirstLetter(city);

                resultBox.innerHTML = `
                    <strong>Weather in ${capitalizedCity}</strong> <br>
                    <span style="font-size: 48px;">${weatherIcon}</span> <br>
                    🌡️ Temperature: ${temperature}°C <br>
                    🌧️ Weather: ${weatherDescription} <br>
                    💧 Humidity: ${humidity}% <br>
                    🌬️ Wind Speed: ${windSpeed} m/s
                `;

                // Save the city to localStorage
                saveCityToCache(capitalizedCity);
            }
        })
        .catch(error => {
            // Handle network or other errors
            resultBox.innerHTML = `<strong>Error:</strong> ${error.message}`;
        });
}

// Load cached cities on page load
window.onload = function () {
    updateCachedCitiesDropdown();
};

// Add event listener for Enter key
document.getElementById("city").addEventListener("keypress", function (event) {
    if (event.key === "Enter") {
        event.preventDefault(); // Prevent default form submission behavior
        checkWeather();
    }
});

// Generate falling effects (Clouds, Snow, Rain, Dew)
function generateWeatherEffects() {
    let effectContainer = document.querySelector('.weather-effect');
    for (let i = 0; i < 50; i++) {
        let drop = document.createElement("span");
        drop.style.left = Math.random() * 100 + "vw";
        drop.style.animationDuration = (Math.random() * 5 + 3) + "s";
        drop.style.animationDelay = Math.random() * 5 + "s";
        effectContainer.appendChild(drop);
    }
}

generateWeatherEffects();