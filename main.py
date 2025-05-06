import io

import qrcode
import streamlit as st


def generate(
    content: str,
    error_correction=qrcode.ERROR_CORRECT_L,
    version: float = 1,
    size: float = 10,
    border: float = 4,
    fill: str = "black",
    back_color: str = "white",
):
    qr = qrcode.QRCode(
        version=version,
        error_correction=error_correction,
        box_size=size,
        border=border,
    )
    qr.add_data(content)
    qr.make(fit=True)
    return qr.make_image(fill=fill, back_color=back_color)


def main():
    st.title("QR Code Generator")
    file_name = st.text_input("File name")
    file_type = st.selectbox("Choose file type", ("jpeg", "png", "svg"))
    content = st.text_area("Content")
    col1, col2, col3 = st.columns(3)
    with col1:
        version = st.number_input("Enter version", min_value=1, max_value=10, value=1)
    with col2:
        size = st.number_input("Enter size", min_value=0, max_value=10, value=10)
    with col3:
        border = st.number_input("Enter border", min_value=0, max_value=10, value=4)
    fill = st.text_input("Fill Colour", value="#000000")
    back_color = st.text_input("Background Colour", value="#ffffff")
    if content:
        qr_code_img = generate(
            content,
            version=version,
            size=size,
            border=border,
            fill=fill,
            back_color=back_color,
        )
        img_byte_arr = io.BytesIO()
        qr_code_img.save(img_byte_arr)
        img_byte_arr = img_byte_arr.getvalue()

        if file_type == "svg":
            mime = "image/svg+xml"
        elif file_type == "jpeg":
            mime = "image/jpeg"
        elif file_type == "png":
            mime = "image/png"

        st.download_button(
            label="Download",
            data=img_byte_arr,
            file_name=f"{file_name}.{file_type}",
            mime=f"{mime}",
        )


if __name__ == "__main__":
    main()
