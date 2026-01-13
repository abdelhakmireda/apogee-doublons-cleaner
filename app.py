import streamlit as st
import http.client
import json
from docx import Document
import io
import plotly.express as px
import matplotlib.pyplot as plt
import tempfile
import pdfplumber
import pandas as pd

# Configuration de la page
st.set_page_config(page_title="💖 FSJES Chatbot 💖", page_icon="🎓", layout="centered")

# CSS stylisé
st.markdown("""
    <style>
        .title {
            font-size: 42px;
            text-align: center;
            color: #9b59b6;
            font-weight: bold;
            margin-bottom: 20px;
        }
        .footer {
            text-align: center;
            color: #8e44ad;
            font-size: 13px;
            margin-top: 40px;
        }
        body {
            background-color: #fdf1f4;
            font-family: "Arial", sans-serif;
        }
    </style>
""", unsafe_allow_html=True)

# Titre
st.markdown('<div class="title">🎓 Chatbot IA - FSJES d\'Ain Chock 🎓</div>', unsafe_allow_html=True)

# Barre de navigation
menu = st.sidebar.radio(
    "Naviguez entre les sections 💡",
    ["Accueil", "Impact de l'IA au Maroc", "Calculs pratiques économiques", "Correcteur d'orthographe", "Chatbot", "Extraction PDF"],
    index=0
)

# Fonction d’appel API
def ask_question(question):
    conn = http.client.HTTPSConnection("chatgpt-42.p.rapidapi.com")
    payload = json.dumps({
        "messages": [{"role": "user", "content": question}],
        "web_access": True
    })
    headers = {
        "x-rapidapi-host": "chatgpt-42.p.rapidapi.com",
        "x-rapidapi-key": "bbb99267eemshe5907c54a7f6e0bp10a546jsn5a43041bc82b",
        "Content-Type": "application/json"
    }
    try:
        conn.request("POST", "/chatgpt", payload, headers)
        res = conn.getresponse()
        data = res.read()
        response_json = json.loads(data.decode("utf-8"))
        return response_json.get("result", "Pas de réponse.")
    except Exception as e:
        return f"Erreur : {e}"

# Export Word
def export_to_word(content, filename="resultat.docx"):
    try:
        doc = Document()
        doc.add_paragraph(content)
        buffer = io.BytesIO()
        doc.save(buffer)
        buffer.seek(0)
        st.download_button("📥 Télécharger en Word", buffer, file_name=filename,
                           mime="application/vnd.openxmlformats-officedocument.wordprocessingml.document")
    except Exception as e:
        st.error(f"❌ Erreur lors de l’export : {e}")
# Extraction de données depuis PDF
def extract_data_from_pdf(pdf_file):
    with tempfile.NamedTemporaryFile(delete=False) as tmp_file:
        tmp_file.write(pdf_file.read())
        tmp_filename = tmp_file.name

    with pdfplumber.open(tmp_filename) as pdf:
        page = pdf.pages[0]
        table = page.extract_table()

    if table:
        df = pd.DataFrame(table[1:], columns=table[0])
        return df
    else:
        return None

# Sauvegarder en Excel
def save_to_excel(df, output_file="FSJES.xlsx"):
    df.to_excel(output_file, index=False, engine="openpyxl")
# Accueil
if menu == "Accueil":
    st.header("👩‍🎓 Présentation du projet")
    st.write("""
        Ce projet a été réalisé par les étudiants de la **Faculté des Sciences Juridiques, Économiques et Sociales (FSJES) d'Aïn Chock**, Casablanca.
        Il vise à démontrer comment l'intelligence artificielle peut être utilisée pour simplifier les processus économiques et améliorer l'accès à l'information.
    """)
    st.image("https://upload.wikimedia.org/wikipedia/commons/thumb/e/e5/Logo_fsjes.png/480px-Logo_fsjes.png", use_container_width=True)
    st.write("""
        **À propos du projet :**
        - Conçu pour faciliter les calculs économiques pratiques.
        - Explore l'impact de l'IA sur l'économie marocaine.
        - Fournit un chatbot interactif pour répondre à vos questions liées à l'économie, l'éducation et plus encore.
    """)

    # Graphique avec Matplotlib
    st.subheader("📊 Graphique : Impact de l'IA sur différents domaines")
    domains = ['Agriculture', 'Industrie', 'Services', 'Startups']
    impact = [80, 90, 70, 85]  # Exemples de valeurs pour le taux d'impact
    plt.figure(figsize=(8, 5))
    plt.bar(domains, impact, color=['green', 'blue', 'orange', 'red'])
    plt.xlabel('Domaines')
    plt.ylabel('Impact (%)')
    plt.title("Taux d'impact de l'IA dans les différents domaines")
    st.pyplot(plt)

# Impact de l'IA au Maroc
elif menu == "Impact de l'IA au Maroc":
    st.header("🌍 Impact de l'IA au Maroc")
    st.write("Voici quelques sujets clés liés à l'IA dans l'économie marocaine :")
    topics = [
        "L'impact de l'IA sur l'agriculture au Maroc",
        "L'industrie et l'automatisation grâce à l'IA",
        "Les services financiers modernisés par l'IA",
        "Les startups marocaines dans le domaine de l'IA"
    ]
    for topic in topics:
        st.write(f"- {topic}")
    question_ia = st.text_input("Posez votre question :", placeholder="Exemple : Quel est l'impact de l'IA sur les startups au Maroc ?")
    if st.button("Analyser avec l'IA 🌟"):
        if question_ia.strip():
            with st.spinner("L'IA analyse votre question..."):
                response = ask_question(question_ia)
            if response == "Pas de réponse.":
                st.warning("Aucune réponse disponible.")
            else:
                st.success("📖 Réponse de l'IA :")
                st.write(response)
                export_to_word(response, filename="reponse_ia_maroc.docx")
        else:
            st.error("Veuillez entrer une question.")
# Extraction PDF vers Excel
elif menu == "Extraction PDF":
    st.header("📄 Extraction de données depuis un PDF")
    uploaded_pdf = st.file_uploader("Choisis un fichier PDF", type=["pdf", "application/pdf"])
    
    if uploaded_pdf:
        df = extract_data_from_pdf(uploaded_pdf)
        
        if df is not None:
            st.write("Données extraites avec succès ! Voici un aperçu :")
            st.dataframe(df)
            
            if st.button("Exporter vers Excel"):
                save_to_excel(df)
                st.success("Fichier Excel généré avec succès ! Téléchargez-le ci-dessous.")
                
                with open("FSJES.xlsx", "rb") as f:
                    st.download_button(
                        label="Télécharger le fichier Excel",
                        data=f,
                        file_name="FSJES.xlsx",
                        mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
                    )
        else:
            st.error("Aucune donnée valide trouvée dans le PDF. Vérifie que le format du tableau est correct.")

# Calculs pratiques économiques
elif menu == "Calculs pratiques économiques":
    st.header("📊 Outils de calcul économique")
    st.write("Saisissez vos données pour effectuer des calculs liés à l'économie marocaine.")

    # Calcul de TVA
    st.subheader("🧮 Calcul de la TVA")
    price = st.number_input("Entrez le prix HT (hors taxe) :", min_value=0.0, value=100.0)
    tva_rate = st.slider("Choisissez le taux de TVA (%) :", 0, 20, 20)
    if st.button("Calculer la TVA"):
        tva = price * tva_rate / 100
        price_ttc = price + tva
        st.success(f"💰 Montant TVA : {tva:.2f} MAD")
        st.success(f"💰 Prix TTC : {price_ttc:.2f} MAD")

    # Calcul des bénéfices
    st.subheader("📈 Calcul des bénéfices")
    revenue = st.number_input("Entrez le revenu total :", min_value=0.0, value=1000.0)
    costs = st.number_input("Entrez le coût total :", min_value=0.0, value=700.0)
    if st.button("Calculer les bénéfices"):
        profit = revenue - costs
        st.success(f"📊 Bénéfice net : {profit:.2f} MAD")

    # Comparaison entre méthodes
    st.subheader("📊 Comparaison : Méthodes statiques vs IA")
    methods = ['Méthodes Statique', 'IA (projet actuel)']
    values = [60, 85]  # Exemples pour la comparaison
    plt.figure(figsize=(8, 5))
    plt.bar(methods, values, color=['gray', 'cyan'])
    plt.ylabel('Efficacité (%)')
    plt.title("Comparaison des méthodes")
    st.pyplot(plt)

    # Nouvel outil : Conversion devise
    st.subheader("💱 Convertisseur de devise (MAD -> EUR)")
    mad = st.number_input("Montant en MAD :", min_value=0.0, value=100.0)
    exchange_rate = 0.093  # Exemple de taux de conversion MAD vers EUR
    if st.button("Convertir"):
        eur = mad * exchange_rate
        st.success(f"💶 Montant en EUR : {eur:.2f}")

# Correcteur d'orthographe
elif menu == "Correcteur d'orthographe":
    st.header("📝 Correcteur d'Orthographe")
    report_text = st.text_area("Collez votre texte ici :", placeholder="Exemple : Mon raport parle des entreprisse au maroc.")
    if st.button("Corriger avec l'IA ✍️"):
        if report_text.strip():
            header_message = f"Corrige le texte suivant sans ajouter de texte inutile :\n{report_text}"
            with st.spinner("🔍 Correction en cours..."):
                corrected_text = ask_question(header_message)
            if corrected_text == "Pas de réponse.":
                st.warning("🌷 L'IA n'a pas pu corriger ce texte.")
            else:
                st.success("✅ Texte corrigé :")
                st.write(corrected_text)
                export_to_word(corrected_text, filename="rapport_corrige_ia.docx")
        else:
            st.error("🚨 Veuillez coller un texte à corriger.")

# Chatbot toujours affiché
# Chatbot toujours affiché
elif menu == "Chatbot":
    st.header("🤖 Chatbot FSJES d'Ain Chock")
    chat_input = st.text_input("Posez votre question ici :", placeholder="Exemple : Quelle est la capitale du Maroc ? 🌍")
    if st.button("Envoyer 🚀"):
        if chat_input.strip():
            with st.spinner("🔍 L'IA réfléchit à votre question..."):
                response = ask_question(chat_input)
            if response == "Pas de réponse.":
                st.warning("🌷 Oups ! L'IA n'a pas trouvé de réponse.")
            else:
                st.success("📜 Réponse de l'IA :")
                st.write(response)
                export_to_word(response, filename="reponse_chatbot.docx")
        else:
            st.error("🚨 Veuillez entrer une question.")
            
# Pied de page
st.markdown('<div class="footer">🎓 © 2025 - FSJES d\'Ain Chock 💖</div>', unsafe_allow_html=True)