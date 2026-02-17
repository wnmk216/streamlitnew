import pandas as pd
import numpy as np
import plotly.express as px
import streamlit as st

st.markdown("""
<style>
body {
    background-color: #f8f9fa;
    font-family: "Prompt", sans-serif;
}
</style>
""", unsafe_allow_html=True)


# Give a title to the app
st.title('Welcome to BMI Calculator')

# Take weight input in kgs
weight = st.number_input("Enter your weight (in kgs)")

# Radio button to choose height format
status = st.radio('Select your height format: ', ('cms', 'meters', 'feet'))

# Initialize bmi variable
bmi = None

# Compare status value to take the appropriate height input
if status == 'cms':
    height = st.number_input('Centimeters')
    try:
        bmi = weight / ((height / 100) ** 2)
    except ZeroDivisionError:
        st.text("Enter a valid value for height")
elif status == 'meters':
    height = st.number_input('Meters')
    try:
        bmi = weight / (height ** 2)
    except ZeroDivisionError:
        st.text("Enter a valid value for height")
else:
    height = st.number_input('Feet')
    try:
        bmi = weight / ((height / 3.28) ** 2)
    except ZeroDivisionError:
        st.text("Enter a valid value for height")

# สร้าง DataFrame ใน session_state ถ้ายังไม่มี
if 'bmi_data' not in st.session_state:
    st.session_state.bmi_data = pd.DataFrame(
        columns=["Weight", "Height", "Unit", "BMI", "Category"]
    )



# Check if the 'Calculate BMI' button is pressed
if st.button('Calculate BMI'):
    if bmi is not None:
        st.text("Your BMI Index is {:.2f}.".format(bmi))
        if bmi < 16:
            st.error("You are Extremely Underweight")
            category = "You are Extremely Underweight"
            
        elif 16 <= bmi < 18.5:
            st.warning("You are Underweight")
            category = "You are Extremely Underweight"
        elif 18.5 <= bmi < 25:
            st.success("Healthy")
            category = "Healthy"
        elif 25 <= bmi < 30:
            st.warning("Overweight")
            category = "Overweight"
        elif bmi >= 30:
            st.error("Extremely Overweight")
            category = "Extremely Overweight"

               # สร้างข้อมูลใหม่ 1 แถว
        new_row = pd.DataFrame([{
            "Weight": weight,
            "Height": height,
            "Unit": status,
            "BMI": round(bmi, 2),
            "Category": category
        }])

        # เพิ่มเข้า DataFrame เดิม
        st.session_state.bmi_data = pd.concat(
            [st.session_state.bmi_data, new_row],
            ignore_index=True
        )

    else:
        st.error("Please enter valid weight and height to calculate BMI.")



   # แสดงตารางผลลัพธ์
if not st.session_state.bmi_data.empty:
    st.subheader("BMI Records")
    
    df_display = st.session_state.bmi_data.copy()
    df_display.insert(0, "No", range(1, len(df_display) + 1))
    
    st.dataframe(df_display, width=700, height=400,hide_index=True)

