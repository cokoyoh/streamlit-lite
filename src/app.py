import streamlit as st

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
