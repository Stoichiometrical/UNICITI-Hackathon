# Energy Usage Prediction Web Interface

This is a web interface that uses weather patterns to predict energy usage for the entire day. It takes weather data from the RapidAPI: https://rapidapi.com/weatherapi/api/weatherapi-com. The predictions are powered by the XGBoost machine learning algorithm. Users can also input manual weather features and get the expected trend. The user gets recommendations which they can automate to their IoT to adjust the necessary appliances during peak hours.

## Project Structure

- `energy_eda.ipynb`: Exploratory data analysis notebook
- `finalmodel.ipynb`: Model building and tuning notebook. Executed in Kaggle due to local dependency issues.
- `xgb_model.pkl`: Saved model
- `energy_complete.csv`: Initial dataset
- `energy_preprocessed.csv`: Preprocessed dataset
- `energy_final.csv`: Dataset with feature selection
- `hackathon-web.py`: Streamlit web interface code

## Data

The dataset used in this project was obtained from the UCI repository: https://archive-beta.ics.uci.edu/dataset/374/appliances+energy+prediction.

## Images

Lottie files were used as images for the website. They are the ones with .json extension.

## Requirements

The following libraries are required to run this project:

- pandas
- numpy
- matplotlib
- seaborn
- xgboost
- altair
- streamlit
- requests
- sklearn
- keras
- lgbm

## Usage

To run the web interface, navigate to the project directory and run the following command:
`streamlit run hackathon-web.py`

The notebook is available on kaggle at :
- [Kaggle](https://www.kaggle.com/davidgondo/finalmodel/edit)


## Authors

- [David Tendai Gondo](https://github.com/Stoichiometrical)
- [Strength Given]()
- [Benson Mugure]()
