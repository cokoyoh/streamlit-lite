import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import requests

# Initialize session state for page navigation
if "page" not in st.session_state:
    st.session_state.page = "BMI Calculator"  # Default page

# Sidebar for navigation with buttons
st.sidebar.title("Nutrition App")
if st.sidebar.button("BMI Calculator"):
    st.session_state.page = "BMI Calculator"
if st.sidebar.button("Weight Tracker"):
    st.session_state.page = "Weight Tracker"
if st.sidebar.button("Nutrition Lookup"):
    st.session_state.page = "Nutrition Lookup"

# BMI Calculator Page
if st.session_state.page == "BMI Calculator":
    st.title("BMI Calculator")
    st.write("This is a simple BMI calculator app.")

    height = st.number_input(
        "Enter your height (cm):", min_value=100, max_value=250, step=1
    )
    weight = st.number_input(
        "Enter your weight (kg):", min_value=30, max_value=200, step=1
    )

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

# Weight Tracker Page
elif st.session_state.page == "Weight Tracker":
    st.title("Weight Tracker")
    st.write("This is a simple weight tracker app.")

    # Upload a file
    uploaded_file = st.file_uploader(
        "Upload a CSV file with your weight data", type=["csv"]
    )
    if uploaded_file is not None:
        df = pd.read_csv(uploaded_file)
        st.dataframe(df)

        # Normalize column names to avoid case or space issues
        df.columns = df.columns.str.strip()  # Remove leading/trailing spaces
        df.columns = df.columns.str.capitalize()  # Capitalize column names

        if "Date" in df.columns and "Weight" in df.columns:
            fig, ax = plt.subplots()
            df["Date"] = pd.to_datetime(df["Date"])
            df.sort_values("Date", inplace=True)
            ax.plot(df["Date"], df["Weight"], marker="o")
            ax.set_title("Weight Over Time")
            ax.set_xlabel("Date from April 1st to April 15th")
            ax.set_ylabel("Weight (kg)")
            st.pyplot(fig)
        else:
            st.error("CSV must contain 'Date' and 'Weight' columns.")

# Nutrition Lookup Page
elif st.session_state.page == "Nutrition Lookup":

    @st.cache_data
    def get_food_nutrition(query):
        url = "https://api.calorieninjas.com/v1/nutrition?query=" + query
        headers = {"X-Api-Key": st.secrets["API_KEY"]}
        response = requests.get(url, headers=headers)
        return response.json()

    st.title("Nutrition Lookup")

    food = st.text_input("Enter a food item:")
    if st.button("Get Nutrition"):
        if food:
            result = get_food_nutrition(food)
            if "items" in result:
                # Convert the result to a pandas DataFrame for better styling
                nutrition_data = pd.DataFrame(result["items"])

                # Remove underscores, capitalize column titles, and replace 'G' with '(gm)'
                nutrition_data.columns = (
                    nutrition_data.columns.str.replace(
                        "_", " "
                    )  # Replace underscores with spaces
                    .str.title()  # Capitalize column titles
                    .str.replace(
                        " G", " (gm)", regex=False
                    )  # Replace ' G' with ' (gm)'
                )

                # Format numeric values to 2 decimal places
                nutrition_data = nutrition_data.applymap(
                    lambda x: f"{x:.2f}" if isinstance(x, (int, float)) else x
                )

                # Reset the index to remove it from the table
                nutrition_data.reset_index(drop=True, inplace=True)

                st.write("### Nutrition Information")
                st.table(nutrition_data)  # Display the data as a table
            else:
                st.error("No data found.")
