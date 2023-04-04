import streamlit as st
import numpy as np
# Qr -Code
import os
import qrcode
import time
import cv2
# Loading
# Globals

from PIL import Image
def load_image(img):
    im=Image.open(img)
    return im


def read_qr_code(filename):
    try:
        img = cv2.imread(filename)
        detect = cv2.QRCodeDetector()
        value, points, straight_qrcode = detect.detectAndDecode(img)
        return value
    except:
        return "###"


qr=qrcode.QRCode(version=1,
                 box_size=10
                 ,border=14)
# .................................................
def main():
    st.set_page_config(page_title=None, page_icon=None, layout="centered", initial_sidebar_state="auto",menu_items=None)
    hide_menu_style = """
            <style>
            #MainMenu {visibility: hidden;}
            </style>
            """
    st.markdown(hide_menu_style, unsafe_allow_html=True)
    menu=["Home","Decode-QR","Scan QR","About"]
    choice =st.sidebar.selectbox("Menu",menu)
    if choice==menu[0]:
        st.subheader("Home")
        #
        with st.form(key='myqr_form'):
            raw_text=st.text_input("Text Here")
            submit_button=st.form_submit_button("Generate QR")
        if submit_button:
            col1,col2=st.columns(2)
            with col1:
                #Qr code generatin
                qr.add_data(raw_text)
                qr.make(fit=True)
                img = qr.make_image(fill_color='black',
                                    black_color='white')

                # img_filename=f'img|{datetime.datetime.utcnow()}|.png'
                # path_img=os.path.join('image_folder',img_filename)
                uniquename=f'{time.time()}'
                img_filename=f'image_folder/{uniquename}'
                img.save(img_filename)

                #load img
                final_img=load_image(img_filename)
                st.image(final_img)

            with col2:
                st.info("you entered")
                st.write(raw_text)
            dire = r"image_folder"
            path=os.path.join(dire,uniquename)
            os.remove(path)
    elif choice==menu[1]:
        st.subheader("Decode-Qr")
        image_file=st.file_uploader("Upload Image",type=['jpg','png','jpeg'])
        if image_file is not None:
            img=load_image(image_file)
            st.image(img)
            name=f'image_folder/{image_file.name}'
            value=read_qr_code(name)
            if(value=="###"):
                st.write("Error happened")
            else:
                st.write("Link Inside QR")
                st.info(value)

    elif choice==menu[2]:
        st.subheader("Scan")
        picture = st.camera_input("Scan Your QR")
        if picture:
            st.image(picture)
            value=read_qr_code(picture.name)
            if (value == "###"):
                st.write("Error happened")
            else:
                st.write("Link Inside QR")
                st.info(value)
    elif choice==menu[3]:
        st.subheader("About")
if __name__=='__main__':
    main()