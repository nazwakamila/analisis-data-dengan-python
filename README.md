# analisis-data-dengan-python
This document details a data analysis project focused on bike sharing data, completed as part of a Dicoding Data Analyst course.  The project leverages Python and several key libraries to extract meaningful insights from bike rental data, aiming to optimize service operations and enhance user experience.  It serves as a practical example of how data analysis can drive improvements in real-world applications and hopefully inspires others to explore this exciting field.

# Project Overview
The core objective of this project was to analyze bike-sharing data to understand user behavior and the influence of various factors on rental patterns.  These factors include weather conditions, time of day, and seasonality.  Python, along with libraries like Pandas, Matplotlib, Seaborn, and Streamlit, were instrumental in data manipulation, visualization, and presentation of the findings.

# Project Structure
```
The project files are organized as follows:
├── dashboard
│   ├── dashboard.py
│   └── main_data.csv
│   └── rental_logo.png
├── data
│   ├── day.csv
│   └── hour.csv
├── README.md
├── notebook.ipynb
├── requirements.txt
│── url.txt
```

# Dataset Description
Two primary datasets were used in this analysis:
 1. day.csv: Contains daily bike rental data, comprising 731 entries.
 2. hour.csv: Contains hourly bike rental data, comprising 17,379 entries.

Key data points within these datasets include:
 * instant: Record index.
 * dteday: Date of the rental.
 * season: Season (1: winter, 2: spring, 3: summer, 4: fall).
 * yr: Year (0: 2011, 1: 2012).
 * mnth: Month (1 to 12).
 * hr: Hour (0 to 23) - present only in hour.csv.
 * holiday: Binary indicator of whether the day was a holiday.
 * weekday: Day of the week.
 * workingday: Binary indicator of whether the day was a working day.
 * weathersit: Weather situation (1: clear, 2: misty, 3: light rain/snow, 4: heavy rain/snow).
 * temp: Normalized temperature in Celsius.
 * atemp: Normalized "feels like" temperature in Celsius.
 * hum: Normalized humidity.
 * windspeed: Normalized wind speed.
 * casual: Number of casual users.
 * registered: Number of registered users.
 * cnt: Total number of bike rentals.

# Setting up the Project
To replicate this analysis, follow these steps:
 1. Clone the Repository:
git clone https://github.com/nazwakamila/analisis-data-dengan-python.git

 2. Install Dependencies:
pip install -r requirements.txt

 3. Data Preparation:
Ensure the main_data_day.csv and main_data_hour.csv files are present in the appropriate directory.  Adjust file paths within dashboard.py if needed.
 4. Run the Streamlit Dashboard:
    cd analisis-data-dengan-python
    streamlit run dashboard/dashboard.py

# Interactive Dashboard and Key Features
The project culminates in an interactive Streamlit dashboard, accessible via the Streamlit Cloud: Dashboard Bike-Sharing.  The dashboard provides several key features:
 * Hourly Analysis: Visualizes bike rental trends by hour, highlighting peak and low usage times.
 * Seasonal Impact: Explores the correlation between seasons and bike rentals, identifying periods of high and low demand.
 * User Analytics:  Compares and contrasts the behavior of casual and registered users.
 * User Rental Analysis: Differentiates rental patterns between weekdays and weekends.
 * Monthly Rental Analysis:  Illustrates monthly rental trends, highlighting peak and low rental months.
 * Interactive Visualization: Leverages Streamlit for dynamic and user-friendly data exploration.

# Key Analysis Areas
The analysis focuses on several key areas:
 * Investigating bicycle usage across different seasons.
 * Identifying the distribution of bicycle usage throughout the day.
 * Analyzing the ratio of regular users to registered users.
 * Identifying bike rental patterns on weekdays versus weekends.
 * Analyzing total bike rentals on a monthly basis.
This project provides a comprehensive analysis of bike-sharing data, demonstrating the power of data analysis in understanding user behavior and informing business decisions.  The interactive Streamlit dashboard allows for easy exploration of the data and provides valuable insights into the factors influencing bike rentals.