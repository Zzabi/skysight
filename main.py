import streamlit as st

st.title("Classification and Forecasting of weather")

tab1,tab2 = st.tabs(["Classify","Forecast"])


with tab1:
    from streamlit_extras.let_it_rain import rain 
    import pickle


    def predict(precip,max_temp,min_temp,wind):
        input = [[precip,max_temp,min_temp,wind]]
        prediction = model.predict(input)[0]

        weather = {
            0:["Drizzly", "🌦️"],
            1:["Foggy", "🌫️"],
            2:["Rainy", "🌧️"],
            3:["Snowy", "❄️"],
            4:["Sunny", "☀️"]
        }

        main = f'<p style="font-family:Courier; color:White; font-size: 40px;">The weather is {weather[prediction][0]}</p>'
        st.markdown(str(main),unsafe_allow_html=True)

        rain(
            emoji=weather[prediction][1],
            font_size=64,
            falling_speed=4,
            animation_length=1
        )
        


    def main():
        global model
        model = pickle.load(open(r'classification/model.pkl','rb'))

        st.title("Weather Classification")

        st.subheader("This is a ai based weather Classifier, please provide the following values")

        max_temp = st.number_input("Max Temperature",step=0.5)
        min_temp = st.number_input("Min Temperature",step=0.5)
        precip = st.number_input("Precipitation",step=0.5)
        wind = st.number_input("Wind",step=0.5)

        if st.button("Predict"):
            predict(precip,max_temp,min_temp,wind)

    main()



with tab2:
    import datetime
    import pickle
    import pandas as pd
    import streamlit as st
    from neuralprophet import NeuralProphet


    def get_forecast(input_):
        start = input_
        last_date = datetime.datetime.strptime("2022-07-25","%Y-%m-%d").date()

        total = start-last_date
        total = total.days

        data = pd.read_csv(r"forecasting/processed.csv")
        data["ds"] = pd.to_datetime(data["ds"])
        m = pickle.load(open(r'forecasting/saved_model.pkl', "rb"))

        future = m.make_future_dataframe(data, periods=total+7)
        m.restore_trainer()
        forecast = m.predict(future)
        forecasted_data = forecast[["ds","yhat1"]]
        forecasted_data["ds"] = pd.to_datetime(forecasted_data["ds"]).dt.date
        forecasted_data.set_index("ds")

        return forecasted_data.iloc[-8:]

    st.title("Average Temperature Forecast")
    st.subheader("This is an ai based Temperature forecaster, please select Date for forecasting")

    today = datetime.date.today()

    d = st.date_input("Select Date", today,min_value=today)
    if st.button("Forecast"):

        forecast_data = get_forecast(d)
        forecast_data["ds"] = pd.to_datetime(forecast_data["ds"]).dt.date
        forecast_data.set_index("ds",inplace=True)
        forecast_data.rename(columns={"yhat1":"Avg Temperature"},inplace=True)

        st.write(forecast_data.transpose())