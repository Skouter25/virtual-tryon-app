
import streamlit as st
from PIL import Image
import tempfile
import subprocess
import os
import shutil

st.set_page_config(page_title="Virtual Try-On", layout="centered")
st.title("👕 AI Virtual Try-On")
st.markdown("Upload a model image and a clothing image. The app will generate a new image of the model wearing the clothes.")

model_img = st.file_uploader("Upload model image", type=["jpg", "jpeg", "png"], key="model")
cloth_img = st.file_uploader("Upload clothing image", type=["jpg", "jpeg", "png"], key="cloth")

if model_img and cloth_img:
    with tempfile.TemporaryDirectory() as tmpdir:
        model_path = os.path.join(tmpdir, "model.jpg")
        cloth_path = os.path.join(tmpdir, "cloth.jpg")

        with open(model_path, "wb") as f:
            f.write(model_img.read())
        with open(cloth_path, "wb") as f:
            f.write(cloth_img.read())

        st.image(Image.open(model_path), caption="Model Image", use_column_width=True)
        st.image(Image.open(cloth_path), caption="Clothing Image", use_column_width=True)

        if st.button("👕 Try On"):
            result_path = os.path.join(tmpdir, "result.jpg")

            # Write viton_infer.py code inline here for testing
            viton_script = f"""
import cv2
import numpy as np
from PIL import Image
import sys

model_path = sys.argv[sys.argv.index('--model_img') + 1]
cloth_path = sys.argv[sys.argv.index('--cloth_img') + 1]
output_path = sys.argv[sys.argv.index('--output') + 1]

model_img = Image.open(model_path).convert("RGB").resize((256, 256))
cloth_img = Image.open(cloth_path).convert("RGB").resize((256, 256))

# Naive overlay: blend cloth on model
blended = Image.blend(model_img, cloth_img, alpha=0.5)
blended.save(output_path)
"""
            viton_py_path = os.path.join(tmpdir, "viton_infer.py")
            with open(viton_py_path, "w") as f:
                f.write(viton_script)

            try:
                subprocess.run([
                    "python", viton_py_path,
                    "--model_img", model_path,
                    "--cloth_img", cloth_path,
                    "--output", result_path
                ], check=True)

                if os.path.exists(result_path):
                    st.success("Try-on complete!")
                    st.image(Image.open(result_path), caption="Result", use_column_width=True)
                    with open(result_path, "rb") as f:
                        st.download_button("Download Result", f, file_name="tryon_result.jpg")
                else:
                    st.error("Result not generated. Check the model script.")

            except subprocess.CalledProcessError as e:
                st.error("Error running model inference: " + str(e))
else:
    st.info("Please upload both model and clothing images.")
