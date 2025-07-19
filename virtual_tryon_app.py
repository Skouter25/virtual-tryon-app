import streamlit as st
from PIL import Image
import tempfile
import os
import shutil
import io

st.set_page_config(page_title="Virtual Try-On", layout="centered")
st.title("👕 AI Virtual Try-On")
st.markdown("Upload a model image and a clothing image. The app will generate a new image of the model wearing the clothes.")

model_img = st.file_uploader("Upload model image", type=["jpg", "jpeg", "png"], key="model")
cloth_img = st.file_uploader("Upload clothing image", type=["jpg", "jpeg", "png"], key="cloth")

if model_img and cloth_img:
    with tempfile.TemporaryDirectory() as tmpdir:
        model_path = os.path.join(tmpdir, "model.jpg")
        cloth_path = os.path.join(tmpdir, "cloth.jpg")
        result_path = os.path.join(tmpdir, "result.jpg")

        with open(model_path, "wb") as f:
            f.write(model_img.read())
        with open(cloth_path, "wb") as f:
            f.write(cloth_img.read())

        st.image(Image.open(model_path), caption="Model Image", use_column_width=True)
        st.image(Image.open(cloth_path), caption="Clothing Image", use_column_width=True)

        if st.button("👕 Try On"):
            try:
                # Run the naive try-on logic inline (no subprocess)
                from PIL import Image as PILImage
                model_pil = PILImage.open(model_path).convert("RGB").resize((256, 256))
                cloth_pil = PILImage.open(cloth_path).convert("RGB").resize((256, 256))

                blended = PILImage.blend(model_pil, cloth_pil, alpha=0.5)
                blended.save(result_path)

                st.success("Try-on complete!")
                st.image(blended, caption="Result", use_column_width=True)
                with open(result_path, "rb") as f:
                    st.download_button("Download Result", f, file_name="tryon_result.jpg")

            except Exception as e:
                st.error("Error during try-on: " + str(e))
else:
    st.info("Please upload both model and clothing images.")
