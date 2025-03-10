# Data Analysis Project: Air Quality
- **Name:** Harry Hamara
- **Email:** harryhh246@gmail.com
- **Dicoding ID:** HarHamz

## Overview

### Data Source
This project takes data from [this](https://archive.ics.uci.edu/dataset/501/beijing+multi+site+air+quality+data) source, which includes hourly air pollutants data from 12 nationally-controlled air-quality monitoring sites in China. These data are then assessed and cleaned accordingly. We then do Exploratory Data Analysis to find the Minimum values, Maximum values, Average values, Q1, Median, and Q3 of the temperatures and pollutants in all the datasets.

### Business Questions
- At which stations were the highest and lowest temperatures recorded?
- How does the temperature change at each station every month in 2016?
- How does the concentration of SO2, NO2, CO, and O3 change at each station every month in 2016?
- Is there a correlation between the concentration of SO2, NO2, CO, O3, and temperatures recorded in 2016 at Shunyi?

### Streamlit Deployed Version
There is also a deployed Streamlit version which answers the 4 questions more thoroughly with visualisation.

Link to Streamlit: [Deployed Streamlit](https://air-quality-dashboard-harhamz.streamlit.app/)

### Setting Up the Environment Locally

1. Clone this repository

   ```bash
   git clone https://github.com/HarHamz/Air_Quality_Project.git
   ```

2. Navigate to the local repository

4. Install all the requirements

   ```bash
   pip install -r requirements.txt
   ```

5. Run the streamlit dashboard

   ```bash
   streamlit run .\dashboard\dashboard.py
   ```

6. To stop the streamlit dashboard, use `ctrl + c`

---


### Requirements
- matplotlib==3.10.1
- pandas==2.2.3
- seaborn==0.13.2
- streamlit==1.43.0



© HarHamz, 2025