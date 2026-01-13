
---

📊 **Apogée Doublons Cleaner**

🧹 Analyse & Nettoyage des doublons dans les fichiers Excel Apogée
Ce projet Streamlit permet de :

* 🔍 Identifier les codes Apogée dupliqués
* 📄 Afficher la dernière occurrence de chaque code
* 🧾 Voir le numéro exact de la ligne Excel, le Nom et le Prénom
* ✨ Supprimer uniquement les doublons lors de l'export
* 💾 Générer un fichier Excel nettoyé tout en conservant le reste des données

---

⚡ **Fonctionnalités principales**

1. 💻 Charger un fichier Excel `.xlsx`
2. 🔍 Détection automatique de l’en-tête et des colonnes Code, Nom et Prénom
3. 📊 Affichage des doublons avec ligne Excel et informations de l’étudiant
4. 🗑️ Suppression sécurisée des dernières occurrences des doublons
5. 📥 Export du fichier nettoyé avec le même nom

---

🚀 **Utilisation**

1. Cloner le dépôt :

```
git clone https://github.com/<votre-utilisateur>/apogee-doublons-cleaner.git
cd apogee-doublons-cleaner
```

2. Installer les dépendances :

```
pip install -r requirements.txt
```

3. Lancer l’application Streamlit :

```
streamlit run app.py
```

4. Charger votre fichier Excel et suivre les instructions à l’écran.

---

🛠️ **Tech & Librairies utilisées**

* Python 🐍
* Streamlit ✨
* Pandas 📊
* XlsxWriter 💾

---

💡 **Notes**

* L’application garde toutes les données intactes sauf les dernières occurrences des doublons
* Affiche le numéro exact de ligne Excel pour un suivi précis
* Compatible avec fichiers Apogée `.xlsx`

---

