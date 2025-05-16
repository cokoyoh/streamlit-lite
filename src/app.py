import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

st.title("BMI Calculator")
st.write("This is a simple BMI calculator app.")

height = st.number_input("Enter your height (cm):", min_value=100, max_value=250, step=1)
weight = st.number_input("Enter your weight (kg):", min_value=30, max_value=200, step=1)

if st.button("Calculate BMI"):
  if height and weight:
    bmi = weight / ((height / 100) ** 2)
    st.write(f"Your BMI is: {bmi:.2f}")
    if bmi < 18.5:
      st.write("You are underweight.")
    elif 18.5 <= bmi < 24.9:
      st.write("You have a normal weight.")
    elif 25 <= bmi < 29.9:
      st.write("You are overweight.")
    else:
      st.write("You are obese.")


st.title("Weight Tracker")
st.write("This is a simple weight tracker app.")

#Upload a file
uploaded_file = st.file_uploader("Upload a CSV file with your weight data", type=["csv"])
if uploaded_file is not None:
    df = pd.read_csv(uploaded_file)
    st.dataframe(df)

    # Normalize column names to avoid case or space issues
    df.columns = df.columns.str.strip()  # Remove leading/trailing spaces
    df.columns = df.columns.str.capitalize()  # Capitalize column names

    if "Date" in df.columns and "Weight" in df.columns:
        fig, ax = plt.subplots()
        df['Date'] = pd.to_datetime(df['Date'])
        df.sort_values('Date', inplace=True)
        ax.plot(df['Date'], df['Weight'], marker='o')
        ax.set_title("Weight Over Time")
        ax.set_xlabel("Date")
        ax.set_ylabel("Weight (kg)")
        st.pyplot(fig)
    else:
        st.error("CSV must contain 'Date' and 'Weight' columns.")
