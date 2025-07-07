import streamlit as st
import os
import tempfile
from fusion.fusion import fusionner_pdfs

st.set_page_config(page_title="Fusion PDF", layout="centered")

st.markdown(
    """
    <style>
    .title { font-size: 2.5em; font-weight: bold; margin-bottom: 10px; }
    .subtitle { font-size: 1.2em; color: #6b7280; margin-bottom: 30px; }
    </style>
    """,
    unsafe_allow_html=True
)

st.markdown('<div class="title">📎 Fusion de PDF</div>', unsafe_allow_html=True)
st.markdown('<div class="subtitle">Importe jusqu/’à 150 fichiers PDF à fusionner (max 1 Go au total)</div>', unsafe_allow_html=True)

if "uploader_key" not in st.session_state:
    st.session_state.uploader_key = 0
if "fusion_ok" not in st.session_state:
    st.session_state.fusion_ok = False
if "output_path" not in st.session_state:
    st.session_state.output_path = ""
if "tmpdir" not in st.session_state:
    st.session_state.tmpdir = ""

uploaded_files = st.file_uploader(
    "Glisse tes fichiers ici ou clique pour les sélectionner",
    type="pdf",
    accept_multiple_files=True,
    key=st.session_state.uploader_key
)

if uploaded_files:
    total_size = sum([len(file.getbuffer()) for file in uploaded_files])
    nb_files = len(uploaded_files)
    size_in_mb = total_size / (1024 * 1024)
    st.info(f"**{nb_files} fichiers sélectionnés** – Poids total : {size_in_mb:.2f} Mo")

if uploaded_files and len(uploaded_files) > 150:
    st.error("Limite : 150 fichiers maximum.")

if uploaded_files and st.button("Fusionner les PDF"):
    with st.spinner("Fusion en cours..."):
        tmpdir = tempfile.TemporaryDirectory()
        import re
        from datetime import datetime

        def extract_date(filename):
            patterns = [
                r'(\d{2})[_\-](\d{2})[_\-](\d{4})',   # 12_06_2025 ou 12-06-2025
                r'(\d{2})[_\-](\d{4})',               # 06_2025 ou 06-2025
                r'(\d{4})[_\-](\d{2})[_\-](\d{2})',   # 2025_06_12 ou 2025-06-12
                r'(\d{4})[_\-](\d{2})',               # 2025_06 ou 2025-06
                r'(\d{4})',                           # 2025
            ]
            for pat in patterns:
                match = re.search(pat, filename)
                if match:
                    parts = match.groups()
                    try:
                        if len(parts) == 3:
                            return datetime.strptime('_'.join(parts), '%d_%m_%Y')
                        elif len(parts) == 2:
                            p1, p2 = parts
                            if int(p1) > 1000:
                                return datetime.strptime(f'{p1}_{p2}', '%Y_%m')
                            else:
                                return datetime.strptime(f'{p2}_{p1}', '%Y_%m')
                        elif len(parts) == 1:
                            return datetime.strptime(parts[0], '%Y')
                    except Exception:
                        continue
            return None  

        file_info = []
        for idx, file in enumerate(uploaded_files):
            date = extract_date(file.name)
            file_info.append((file, date, file.name))

        file_info_sorted = sorted(file_info, key=lambda x: (x[1] is None, x[1] or datetime.min, x[2]))

        pdf_paths = []
        for info in file_info_sorted:
            file = info[0]
            path = os.path.join(tmpdir.name, file.name)
            with open(path, "wb") as f:
                f.write(file.read())
            pdf_paths.append(path)

        output_path = os.path.join(tmpdir.name, "fusionné.pdf")
        fusionner_pdfs(pdf_paths, output_path)

        st.markdown("**Ordre de fusion final :**")
        for i, info in enumerate(file_info_sorted, 1):
            st.markdown(f"{i}. {info[2]} {'(date: '+str(info[1].date())+')' if info[1] else ''}")

        st.session_state.fusion_ok = True
        st.session_state.output_path = output_path
        st.session_state.tmpdir = tmpdir

if st.session_state.fusion_ok:
    st.success(" Fusion terminée !")
    nom_fichier = st.text_input("Nom du fichier de sortie :", value="fusionné.pdf")

    if os.path.exists(st.session_state.output_path):
        with open(st.session_state.output_path, "rb") as f:
            st.download_button(
                "Télécharger le PDF fusionné",
                f,
                nom_fichier if nom_fichier.endswith(".pdf") else nom_fichier + ".pdf"
            )

    if st.button("Réinitialiser"):
        st.session_state.fusion_ok = False
        st.session_state.output_path = ""
        st.session_state.tmpdir = ""
        st.session_state.uploader_key += 1
        st.rerun()
