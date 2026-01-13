import streamlit as st
import pandas as pd
import unicodedata
from io import BytesIO

st.set_page_config(page_title="Apogée – Nettoyage Doublons", layout="wide")
st.title("📊 Analyse & Nettoyage des doublons Apogée")

uploaded_file = st.file_uploader("📂 Charger un fichier Excel (.xlsx)", type="xlsx")

# ─────────────────────────────
# FONCTIONS
# ─────────────────────────────
def clean_col_name(col):
    if not isinstance(col, str):
        return ""
    col = unicodedata.normalize('NFKD', col).encode('ascii', 'ignore').decode('ascii')
    col = col.replace('\n', ' ').replace('\r', ' ')
    return ' '.join(col.split()).strip().lower()

def is_apogee_like(val):
    if pd.isna(val):
        return False
    s = str(val).strip()
    return s.isdigit() and 7 <= len(s) <= 9

# ─────────────────────────────
# TRAITEMENT
# ─────────────────────────────
if uploaded_file is not None:
    excel = pd.ExcelFile(uploaded_file)

    cleaned_sheets = {}   # feuilles nettoyées
    has_any_duplicates = False

    for sheet in excel.sheet_names:
        with st.expander(f"📄 Feuille : {sheet}", expanded=False):

            # Lecture brute
            df_raw = pd.read_excel(excel, sheet_name=sheet, header=None, dtype=str)
            df_raw = df_raw.applymap(lambda x: str(x).strip() if pd.notna(x) else "")

            # Détection header
            header_row = None
            for i in range(min(10, len(df_raw))):
                row = [clean_col_name(x) for x in df_raw.iloc[i]]
                if any(k in " ".join(row) for k in ['nom', 'prenom', 'code', 'apoge', 'gr']):
                    header_row = i
                    break

            if header_row is None:
                st.warning("❌ En-tête non détectée – feuille ignorée")
                continue

            # Lecture complète à partir de l'en-tête
            df = pd.read_excel(excel, sheet_name=sheet, skiprows=header_row, dtype=str)
            df.columns = [clean_col_name(c) for c in df.columns]

            # Détection colonne Code Apogée
            code_col = None
            for c in df.columns:
                if 'code' in c and 'apoge' in c:
                    code_col = c
                    break

            if code_col is None:
                ratios = []
                for col in df.columns[:10]:
                    r = df[col].apply(is_apogee_like).mean()
                    if r > 0.6:
                        ratios.append((r, col))
                if ratios:
                    ratios.sort(reverse=True)
                    code_col = ratios[0][1]

            if code_col is None:
                st.error("❌ Code Apogée non détecté")
                continue

            df[code_col] = df[code_col].astype(str).str.strip()

            # Ajouter le numéro de ligne Excel réel
            df['ligne_excel'] = df.index + header_row + 2

            # Colonnes nom et prénom
            nom_col = next((c for c in df.columns if 'nom' in c), None)
            prenom_col = next((c for c in df.columns if 'prenom' in c or 'prnom' in c), None)

            # Filtrer les codes valides
            df_valid = df[df[code_col].apply(is_apogee_like)].copy()

            # 🔴 LIGNES DOUBLANTES À SUPPRIMER (DERNIÈRES OCCURRENCES)
            codes_dupliques = df_valid[df_valid.duplicated(subset=[code_col], keep=False)][code_col].unique()
            last_occurrences = pd.DataFrame()
            for code in codes_dupliques:
                rows = df_valid[df_valid[code_col] == code]
                last_occurrences = pd.concat([last_occurrences, rows.tail(1)])

            if last_occurrences.empty:
                st.success("✅ Aucun doublon détecté")
            else:
                has_any_duplicates = True
                st.error("⚠️ Doublons détectés (dernières occurrences seulement)")

                # Colonnes à afficher
                display_cols = [code_col, 'ligne_excel']
                if nom_col:
                    display_cols.append(nom_col)
                if prenom_col:
                    display_cols.append(prenom_col)

                st.dataframe(
                    last_occurrences[display_cols].sort_values('ligne_excel'),
                    use_container_width=True,
                    hide_index=True
                )

            # Nettoyage réel : supprimer uniquement les dernières occurrences
            cleaned_df = df_valid.drop(last_occurrences.index)

            cleaned_sheets[sheet] = cleaned_df

            st.divider()

    # ─────────────────────────────
    # BOUTON GLOBAL
    # ─────────────────────────────
    if has_any_duplicates:
        st.markdown("## 🧹 Nettoyage global")

        if st.button("🔥 Supprimer les doublons et générer le fichier final"):
            output = BytesIO()

            with pd.ExcelWriter(output, engine="xlsxwriter") as writer:
                for sheet_name, df_clean in cleaned_sheets.items():
                    df_clean.to_excel(
                        writer,
                        sheet_name=sheet_name,
                        index=False
                    )

            output.seek(0)

            st.success("✅ Doublons supprimés dans toutes les feuilles")
            st.download_button(
                label="📥 Télécharger le fichier nettoyé",
                data=output,
                file_name=uploaded_file.name,
                mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
            )
    else:
        st.success("🎉 Aucun doublon trouvé dans tout le fichier")
