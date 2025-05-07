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
    file_type = st.selectbox("Select file type", ("jpeg", "png", "svg"))
    content = st.text_area("Content", max_chars = 2953, help="The content of the QR code can be a URL, text, or any other data. The maximum size is 2953 characters.")
    col1, col2, col3 = st.columns(3)
    with col1:
        version = st.number_input("Enter version", min_value=1, max_value=40, value=1, help="The higher the version, the larger the QR code (1-40).")
    with col2:
        size = st.number_input(
            "Enter size",
            min_value=0,
            max_value=10,
            value=10,
            help="The box_size parameter controls how many pixels each “box” of the QR code is.",
        )
    with col3:
        border = st.number_input("Enter border", min_value=0, max_value=10, value=4, help="The border parameter controls how many boxes thick the border should be (minimum 4).")
    fill = st.text_input("Fill colour", value="#000000", help="Must be defined using hex colour code")
    back_color = st.text_input("Background colour", value="#ffffff", help="You can use hex colour codes or colour names: transparent, red, green, blue, etc.")
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

        match file_type:
            case "svg":
                mime = "image/svg+xml"
            case "jpeg":
                mime = "image/jpeg"
            case "png":
                mime = "image/png"

    is_disabled = not (file_name and content)

    st.download_button(
        label="Download",
        data=img_byte_arr if not is_disabled else b"",  # Provide empty data if disabled
        file_name=f"{file_name}.{file_type}" if not is_disabled else "",
        mime=f"{mime}" if not is_disabled else "",
        disabled=is_disabled,  # Disable the button if fields are not filled
        use_container_width=True,
    )


if __name__ == "__main__":
    main()
