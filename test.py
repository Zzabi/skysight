import streamlit as st
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
    model = pickle.load(open('model.pkl','rb'))

    st.title("Weather prediction")

    st.subheader("This is a ai based weather predictor, please provide the following values to see the prediction")

    max_temp = st.number_input("Max Temperature")
    min_temp = st.number_input("Min Temperature")
    precip = st.number_input("Precipitation")
    wind = st.number_input("Wind")

    if st.button("Predict"):
        predict(precip,max_temp,min_temp,wind)


if __name__=="__main__":
    main()



    