import cv2
import streamlit as st
import numpy as np
from PIL import Image

hide_streamlit_style = """
            <style>
            #MainMenu {visibility: hidden;}
            footer {visibility: hidden;}
            stDeployButton {visibility: hidden !important;}
            </style>
            """
st.markdown(hide_streamlit_style, unsafe_allow_html=True)

def draw_grid(image, line_space=20):
    H = image.shape[0]
    W = image.shape[1]
    image[0:H:line_space] = 1
    image[:, 0:W:line_space] = 1
    grid_image = image
    return grid_image

def three_to_two(image, scaling_height):
      h = image.shape[0]
      w = image.shape[1]
      scaler = int(scaling_height) / h
      # cropper for 2:3
      new_height = h * scaler
      new_width = w * scaler
      dim = (int(new_width), int(new_height))
      scaled_image = cv2.resize(image, dim, interpolation = cv2.INTER_AREA)
      # 700 / 3 * 2 = 466
      scaling_width = int(scaling_height) / 3 * 2
      a = new_width - scaling_width
      width_start = int(a / 2)
      width_end = width_start + int(scaling_width)
      cropped_image = scaled_image[0:int(scaling_height), width_start:width_end]
      return cropped_image


def brighten_image(image, amount):
    img_bright = cv2.convertScaleAbs(image, beta=amount)
    return img_bright


def blur_image(image, amount):
    img = cv2.cvtColor(image, 1)
    blur_img = cv2.GaussianBlur(img, (11, 11), amount)
    return blur_img


def enhance_details(img):
    hdr = cv2.detailEnhance(img, sigma_s=12, sigma_r=0.15)
    return hdr


# cropper for 3:4
def four_to_three(image, scaling_height):
  h = image.shape[0]
  w = image.shape[1]
  scaler = int(scaling_height) / h
  # cropper for 2:3
  new_height = h * scaler
  new_width = w * scaler
  dim = (int(new_width), int(new_height))
  scaled_image = cv2.resize(image, dim, interpolation=cv2.INTER_AREA)
  # 700 / 3 * 2 = 466
  scaling_width = int(scaling_height) / 4 * 3
  a = new_width - scaling_width
  width_start = int(a / 2)
  width_end = width_start + int(scaling_width)
  cropped_image = scaled_image[0:int(scaling_height), width_start:width_end]
  return cropped_image


# cropper for 9:16
def nine_to_sixteen(image, scaling_height):
  h = image.shape[0]
  w = image.shape[1]
  scaler = int(scaling_height) / h
  # cropper for 2:3
  new_height = h * scaler
  new_width = w * scaler
  dim = (int(new_width), int(new_height))
  scaled_image = cv2.resize(image, dim, interpolation=cv2.INTER_AREA)
  # 700 / 3 * 2 = 466
  scaling_width = int(scaling_height) / 16 * 9
  a = new_width - scaling_width
  width_start = int(a / 2)
  width_end = width_start + int(scaling_width)
  cropped_image = scaled_image[0:int(scaling_height), width_start:width_end]
  return cropped_image

def main_loop():
    st.title("Demo App")
    st.subheader("Voit vaihtaa kuvasuhdetta ja kokeilla yksinkertaisia kuvafiltereitä")

    picture_caption = ""

    blur_rate = st.sidebar.slider("Blurring", min_value=0, max_value=25, value=0)
    brightness_amount = st.sidebar.slider("Brightness", min_value=-50, max_value=50, value=0)
    apply_enhancement_filter = st.sidebar.checkbox('korosta kuvan yksityiskohtia')
    scale_picture = st.sidebar.checkbox('skaalaa kuvasuhdetta')
    grid_pic = st.sidebar.checkbox('Käytä ristikkoa')

    if scale_picture:
        scale_relation = st.sidebar.radio('valitse kuvasuhde', [':kaksi_kolmeen', ':kolme_neljaan', ':yhdeksan_kuuteentoista'],
                                          captions = ['3:2', '4:3', '16:9'])
        scale_height = st.sidebar.text_input("kuvan korkeus", value=700)


    kuva = st.radio("Muokattava kuva", [':oma', ':oletus'],
             captions=['Käytä omaa kuvaa', 'Muokkaa oletuskuvaa'])
    if kuva == ":oma":
        picture_caption = picture_caption + "ladattu kuva, "
        image_file = st.file_uploader("Upload Your Image", type=['jpg', 'png', 'jpeg'])
        if not image_file:
            return None
    elif kuva == ":oletus":
        picture_caption = picture_caption + "Oletus kuva, "
        image_file = "Haataja.jpg"
    else:
        st.text("Kuvaa ei voitu ladata, yritä ladata sivu uudestaan")

    orig_image = Image.open(image_file)
    orig_image = np.array(orig_image)
    image = orig_image
    blurred_image = orig_image
    #brightened_image = orig_image
    #original_image = Image.open(image_file)
    #original_image = np.array(original_image)

    blurred_image = blur_image(blurred_image, blur_rate)
    brightened_image = blurred_image
    brightened_image = brighten_image(brightened_image, brightness_amount)

    if apply_enhancement_filter:
        processed_image = enhance_details(brightened_image)

    if scale_picture:
        if scale_relation == ':kaksi_kolmeen':
            picture_caption = picture_caption + "kuvasuhde 3:2, "
            if blur_rate != 0:
                blurred_image = three_to_two(blurred_image, scale_height)
            if brightness_amount != 0:
                brightened_image = three_to_two(brightened_image, scale_height)
            if apply_enhancement_filter:
                processed_image = three_to_two(processed_image, scale_height)
            else:
                image = three_to_two(orig_image, scale_height)
        elif scale_relation == ':kolme_neljaan':
            picture_caption = picture_caption + "kuvasuhde 4:3, "
            if blur_rate != 0:
                blurred_image = four_to_three(blurred_image, scale_height)
            if brightness_amount != 0:
                brightened_image = four_to_three(brightened_image, scale_height)
            if apply_enhancement_filter:
                processed_image = four_to_three(processed_image, scale_height)
            else:
                image = four_to_three(orig_image, scale_height)
        elif scale_relation == ':yhdeksan_kuuteentoista':
            picture_caption = picture_caption + "kuvasuhde 16:9, "
            if blur_rate != 0:
                blurred_image = nine_to_sixteen(blurred_image, scale_height)
            if brightness_amount != 0:
                brightened_image = nine_to_sixteen(brightened_image, scale_height)
            if apply_enhancement_filter:
                processed_image = nine_to_sixteen(processed_image, scale_height)
            else:
                image = nine_to_sixteen(orig_image, scale_height)
        #processed_image = enhance_details(processed_image)


    #st.image([original_image, processed_image])
    if blur_rate != 0:
        picture_caption = picture_caption + "sumennus arvolla: " + blur_rate + ", "
        if brightness_amount != 0:
            if apply_enhancement_filter:
                showing_image = processed_image
            else:
                showing_image = brightened_image
        else:
            showing_image = blurred_image
    elif brightness_amount != 0:
        picture_caption = picture_caption + "kuvan kirkkaus arvolla: " + brightness_amount + ", "
        if apply_enhancement_filter:
            showing_image = processed_image
        else:
            showing_image = brightened_image
    elif apply_enhancement_filter:
        picture_caption = picture_caption + "kuvan yksityiskohtia korostettu, "
        showing_image = processed_image
    else:
        showing_image = image

    if grid_pic:
        picture_caption = picture_caption + "näytetään ristikon kanssa."
        linespace = st.sidebar.text_input("viivojen väli pikseleinä (oletusarvo 20)", value=20)
        showing_image = draw_grid(showing_image, int(linespace))
        st.image(showing_image, caption=picture_caption)
    else:
        picture_caption = picture_caption + "näytetään ilman ristikkoa"
        st.image(showing_image, caption=picture_caption)

if __name__ == '__main__':
    main_loop()


