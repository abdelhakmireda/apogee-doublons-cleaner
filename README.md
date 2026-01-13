
---

# 📊 Apogée Doublons Cleaner

Bienvenue dans **Apogée Doublons Cleaner** ! 🧹

Cette petite application **Streamlit** a été conçue pour t’aider à gérer les fichiers Excel Apogée et à résoudre facilement le problème des doublons. Si tu as déjà eu des codes Apogée répétés dans tes fichiers, tu sais combien cela peut poser des problèmes lors des traitements ou des exports. Ce projet te permet de :

* 🔍 **Identifier tous les codes Apogée dupliqués** dans tes fichiers
* 📄 **Afficher uniquement la dernière occurrence** de chaque code dupliqué
* 🧾 **Voir le numéro exact de la ligne Excel**, ainsi que le **Nom** et le **Prénom** de l’étudiant
* ✨ **Supprimer automatiquement les doublons** lors de l’export, tout en conservant les autres lignes intactes
* 💾 **Générer un fichier Excel nettoyé** prêt à l’emploi, avec le même nom que ton fichier original

---

## ⚡ Fonctionnalités principales

1. 💻 **Charger un fichier Excel `.xlsx`** directement depuis l’interface Streamlit.
2. 🔍 **Détection automatique de l’en-tête** et des colonnes importantes comme Code Apogée, Nom et Prénom.
3. 📊 **Affichage clair des doublons** avec le numéro de ligne dans Excel pour un suivi précis.
4. 🗑️ **Nettoyage sécurisé des doublons** : seule la dernière occurrence de chaque code est supprimée.
5. 📥 **Export facile** du fichier nettoyé tout en conservant toutes les autres données intactes.

---

## 🚀 Comment l’utiliser

1. **Cloner le dépôt** sur ton ordinateur :

```
git clone https://github.com/<votre-utilisateur>/apogee-doublons-cleaner.git
cd apogee-doublons-cleaner
```

2. **Installer les dépendances** nécessaires :

```
pip install -r requirements.txt
```

3. **Lancer l’application** :

```
streamlit run app.py
```

4. **Charger ton fichier Excel** et suivre les instructions à l’écran.
   L’application détectera automatiquement les doublons et te proposera de les supprimer si nécessaire.

---

## 🛠️ Technologies utilisées

* **Python 🐍** pour la logique et le traitement des données
* **Streamlit ✨** pour créer une interface web simple et interactive
* **Pandas 📊** pour la manipulation des fichiers Excel
* **XlsxWriter 💾** pour exporter facilement les fichiers nettoyés

---

## 💡 Notes importantes

* L’application **ne touche pas aux autres données** de ton fichier, elle supprime uniquement la dernière ligne d’un code dupliqué.
* Tu peux visualiser **le numéro exact de ligne Excel** pour chaque doublon, ce qui te permet de savoir exactement où intervenir.
* Compatible avec **tous les fichiers Apogée `.xlsx`**.

---

## 📬 Contact

Pour toute question, suggestion ou rapport de bug, tu peux créer une **issue** dans ce dépôt GitHub.
Ton retour est toujours le bienvenu pour améliorer l’outil ! 🚀

---


Veux‑tu que je fasse ça ?
