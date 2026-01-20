import streamlit as st
import pandas as pd
import unicodedata
from io import BytesIO

st.set_page_config(page_title="Outils Apogée – Comparaison & Nettoyage", layout="wide")
st.title("🛠️ Outils Apogée : Comparaison & Nettoyage Doublons")

# ─────────────────────────────────────────────
# Sélecteur de fonctionnalité (tabs ou radio)
# ─────────────────────────────────────────────
fonction = st.radio(
    "Choisissez la fonctionnalité :",
    ["1. Comparaison Listes (Manquants)", "2. Nettoyage Doublons Apogée"],
    horizontal=True,
    key="fonction_select"
)

st.markdown("---")

# ─────────────────────────────────────────────
# FONCTIONS COMMUNES DE NORMALISATION
# ─────────────────────────────────────────────
def normalize_name(text):
    if pd.isna(text):
        return ""
    text = str(text).strip().upper()
    text = unicodedata.normalize('NFKD', text).encode('ascii', 'ignore').decode('ascii')
    text = ' '.join(text.split())
    return text

def normalize_full_name(nom, prenom):
    return f"{normalize_name(nom)} {normalize_name(prenom)}".strip()

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

# ─────────────────────────────────────────────
# FONCTIONNALITÉ 1 : COMPARAISON LISTES
# ─────────────────────────────────────────────
if fonction == "1. Comparaison Listes (Manquants)":
    st.subheader("🔍 Comparaison : Trouver les étudiants manquants")

    col1, col2 = st.columns(2)

    with col1:
        st.caption("Fichier 1 – Avec Code Apogée")
        file1 = st.file_uploader("Fichier complet (Apogée + Nom + Prénom)", type=["xlsx", "xls"], key="file1_comp")

    with col2:
        st.caption("Fichier 2 – Noms/Prénoms seulement")
        file2 = st.file_uploader("Liste de référence (Nom + Prénom)", type=["xlsx", "xls"], key="file2_comp")

    if file1 and file2:
        try:
            df1 = pd.read_excel(file1, dtype=str)
            original_columns = list(df1.columns)
            st.info(f"Colonnes Fichier 1 : {original_columns}")

            df1.columns = [normalize_name(c) for c in original_columns]

            code_candidates = [c for c in df1.columns if any(k in c for k in ['code', 'apoge', 'etu', 'matricule', 'cod', 'n°'])]
            nom_candidates   = [c for c in df1.columns if 'nom' in c or 'family' in c or 'pat' in c]
            prenom_candidates = [c for c in df1.columns if 'prenom' in c or 'first' in c or 'prnom' in c or 'given' in c]

            st.write("**Suggestions :**")
            st.write("- Code :", code_candidates)
            st.write("- Nom :", nom_candidates)
            st.write("- Prénom :", prenom_candidates)

            code_col = st.selectbox("Colonne Code Apogée", ["--- Choisir ---"] + list(df1.columns), index=0 if not code_candidates else df1.columns.get_loc(code_candidates[0])+1, key="code1")
            nom_col  = st.selectbox("Colonne Nom",         ["--- Choisir ---"] + list(df1.columns), index=0 if not nom_candidates   else df1.columns.get_loc(nom_candidates[0])+1,   key="nom1")
            prenom_col = st.selectbox("Colonne Prénom",    ["--- Choisir ---"] + list(df1.columns), index=0 if not prenom_candidates else df1.columns.get_loc(prenom_candidates[0])+1, key="prenom1")

            if code_col != "--- Choisir ---" and nom_col != "--- Choisir ---" and prenom_col != "--- Choisir ---":
                df1 = df1[[code_col, nom_col, prenom_col]].dropna(subset=[code_col])
                df1[code_col] = df1[code_col].astype(str).str.strip()
                df1['cle_norm'] = df1.apply(lambda r: normalize_full_name(r[nom_col], r[prenom_col]), axis=1)

                # Fichier 2
                df2 = pd.read_excel(file2, dtype=str)
                df2.columns = [normalize_name(c) for c in df2.columns]

                nom_col2    = st.selectbox("Nom (Fichier 2)",    list(df2.columns), key="nom2")
                prenom_col2 = st.selectbox("Prénom (Fichier 2)", list(df2.columns), key="prenom2")

                df2 = df2[[nom_col2, prenom_col2]].dropna()
                df2['cle_norm'] = df2.apply(lambda r: normalize_full_name(r[nom_col2], r[prenom_col2]), axis=1)

                if st.button("🔎 Comparer", type="primary", key="btn_comp"):
                    manquants = df1[~df1['cle_norm'].isin(df2['cle_norm'])].copy()

                    if manquants.empty:
                        st.success("Tous les étudiants sont présents !")
                    else:
                        st.warning(f"{len(manquants)} étudiants manquent dans la liste de référence")

                        result_df = manquants[[code_col, nom_col, prenom_col]].rename(columns={
                            code_col: "Code Apogée",
                            nom_col: "Nom",
                            prenom_col: "Prénom"
                        }).sort_values("Nom")

                        st.dataframe(result_df, use_container_width=True, height=400)

                        output = BytesIO()
                        with pd.ExcelWriter(output, engine="xlsxwriter") as writer:
                            result_df.to_excel(writer, sheet_name="Manquants", index=False)
                        output.seek(0)

                        st.download_button(
                            "📥 Télécharger les manquants",
                            data=output,
                            file_name="manquants.xlsx",
                            mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
                        )

        except Exception as e:
            st.error(f"Erreur : {e}")

# ─────────────────────────────────────────────
# FONCTIONNALITÉ 2 : NETTOYAGE DOUBLONS
# ─────────────────────────────────────────────
elif fonction == "2. Nettoyage Doublons Apogée":
    st.subheader("🧹 Nettoyage des doublons sur Code Apogée")

    uploaded_file = st.file_uploader("📂 Charger fichier Excel (.xlsx)", type="xlsx", key="file_doublons")

    if uploaded_file is not None:
        excel = pd.ExcelFile(uploaded_file)
        cleaned_sheets = {}
        has_any_duplicates = False

        for sheet in excel.sheet_names:
            with st.expander(f"Feuille : {sheet}", expanded=False):
                df_raw = pd.read_excel(excel, sheet_name=sheet, header=None, dtype=str)
                df_raw = df_raw.applymap(lambda x: str(x).strip() if pd.notna(x) else "")

                header_row = None
                for i in range(min(10, len(df_raw))):
                    row = [clean_col_name(x) for x in df_raw.iloc[i]]
                    if any(k in " ".join(row) for k in ['nom', 'prenom', 'code', 'apoge', 'gr']):
                        header_row = i
                        break

                if header_row is None:
                    st.warning("En-tête non détectée")
                    continue

                df = pd.read_excel(excel, sheet_name=sheet, skiprows=header_row, dtype=str)
                df.columns = [clean_col_name(c) for c in df.columns]

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
                    st.error("Code Apogée non détecté")
                    continue

                df[code_col] = df[code_col].astype(str).str.strip()
                df['ligne_excel'] = df.index + header_row + 2

                nom_col = next((c for c in df.columns if 'nom' in c), None)
                prenom_col = next((c for c in df.columns if 'prenom' in c or 'prnom' in c), None)

                df_valid = df[df[code_col].apply(is_apogee_like)].copy()

                codes_dupliques = df_valid[df_valid.duplicated(subset=[code_col], keep=False)][code_col].unique()
                last_occurrences = pd.DataFrame()
                for code in codes_dupliques:
                    rows = df_valid[df_valid[code_col] == code]
                    last_occurrences = pd.concat([last_occurrences, rows.tail(1)])

                if last_occurrences.empty:
                    st.success("Aucun doublon")
                else:
                    has_any_duplicates = True
                    st.error(f"Doublons détectés ({len(last_occurrences)})")

                    display_cols = [code_col, 'ligne_excel']
                    if nom_col: display_cols.append(nom_col)
                    if prenom_col: display_cols.append(prenom_col)

                    st.dataframe(
                        last_occurrences[display_cols].sort_values('ligne_excel'),
                        use_container_width=True,
                        height=300
                    )

                cleaned_df = df_valid.drop(last_occurrences.index)
                cleaned_sheets[sheet] = cleaned_df

        if has_any_duplicates:
            if st.button("🔥 Supprimer doublons et télécharger"):
                output = BytesIO()
                with pd.ExcelWriter(output, engine="xlsxwriter") as writer:
                    for sheet_name, df_clean in cleaned_sheets.items():
                        df_clean.to_excel(writer, sheet_name=sheet_name, index=False)
                output.seek(0)

                st.success("Fichier nettoyé généré")
                st.download_button(
                    "📥 Télécharger fichier nettoyé",
                    data=output,
                    file_name=f"nettoye_{uploaded_file.name}",
                    mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
                )
        else:
            st.success("Aucun doublon trouvé")