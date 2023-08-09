from solver import solve
import streamlit as st
import os 

# Add a title and intro text
st.markdown("<h1 style='text-align: center; color: white;'>Fill One Line Game (Solver)", unsafe_allow_html=True)
input_image = st.file_uploader('Upload a screenshot of the game you want to solve')

def save_uploadedfile(uploadedfile):
     with open(os.path.join("./",uploadedfile.name),"wb") as f:
         f.write(uploadedfile.getbuffer())
     return st.success(f"{uploadedfile.name} File Uploaded Successfully!")

if input_image:
    save_uploadedfile(input_image)
    solve(input_image.name)

    col1, col2 = st.columns(2)
    col1.image('edges.png', caption='Segmented blocks', use_column_width=True)
    col2.image('solved.png', caption='Solved puzzle', use_column_width=True)

#########################################################
st.markdown("<h1 style='font-size:15px; text-align: center; color: blue; font-family:SansSerif;'>Made with 💖 By Ahmed Hossam</h1>", unsafe_allow_html=True)
st.markdown("[My Github](https://github.com/Ahmed-Hossam-Aldeen)")
st.markdown("[Buy me a coffe!](https://www.buymeacoffee.com/ahmed01899a)")
st.image('https://www.buymeacoffee.com/assets/img/guidelines/download-assets-2.svg', width=200)    