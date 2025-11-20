
import streamlit as st
import pandas as pd

# Mapping exercices -> groupes + images
exercise_data = {
    "Développé couché": {"groupe": "Pectoraux", "image": "https://i.imgur.com/ICftW9Q.jpg"},
    "Développé incliné": {"groupe": "Pectoraux", "image": "https://i.imgur.com/zDJ3BuD.jpg"},
    "Ecarté poulie": {"groupe": "Pectoraux", "image": "https://i.imgur.com/bn93ELT.jpg"},
    "Pompes": {"groupe": "Pectoraux", "image": "https://i.imgur.com/wPtJu6F.jpg"},
    "Dips": {"groupe": "Triceps", "image": "https://i.imgur.com/nQSGXfR.jpg"},
    "Tractions": {"groupe": "Dos", "image": "https://i.imgur.com/JlHbLFE.jpg"},
    "Tractions lestées": {"groupe": "Dos", "image": "https://i.imgur.com/JlHbLFE.jpg"},
    "Tirage horizontal": {"groupe": "Dos", "image": "https://i.imgur.com/BxM0urJ.jpg"},
    "Tirage vertical prise supination": {"groupe": "Dos", "image": "https://i.imgur.com/yXubZp6.jpg"},
    "Rowing barre": {"groupe": "Dos", "image": "https://i.imgur.com/UWhKDR8.jpg"},
    "Extensions sur banc à lombaires": {"groupe": "Dos", "image": "https://i.imgur.com/xAipij9.jpg"},
    "Presse": {"groupe": "Jambes", "image": "https://i.imgur.com/hTgUIVZ.jpg"},
    "Belt Squat": {"groupe": "Jambes", "image": "https://i.imgur.com/lvTDGyP.jpg"},
    "Fentes": {"groupe": "Jambes", "image": "https://i.imgur.com/NBbKcRM.jpg"},
    "Leg curl assis": {"groupe": "Jambes", "image": "https://i.imgur.com/Ulm0yMv.jpg"},
    "Leg curl allongé": {"groupe": "Jambes", "image": "https://i.imgur.com/8Hd0Znx.jpg"},
    "Extensions mollets": {"groupe": "Mollets", "image": "https://i.imgur.com/VUqpiPO.jpg"},
    "Développé militaire": {"groupe": "Épaules", "image": "https://i.imgur.com/UTvgZg4.jpg"},
    "Élévations latérales": {"groupe": "Épaules", "image": "https://i.imgur.com/KAXqWJn.jpg"},
    "Développé haltères": {"groupe": "Épaules", "image": "https://i.imgur.com/KctNSK4.jpg"},
    "Oiseau": {"groupe": "Épaules", "image": "https://i.imgur.com/tUz1D7a.jpg"},
    "Crunch": {"groupe": "Abdos", "image": "https://i.imgur.com/M2PQRE1.jpg"},
    "Crunch à la poulie": {"groupe": "Abdos", "image": "https://i.imgur.com/1LYW9rc.jpg"},
    "Relevé de jambes": {"groupe": "Abdos", "image": "https://i.imgur.com/3Y00fON.jpg"},
    "Chaise romaine": {"groupe": "Abdos", "image": "https://i.imgur.com/bCM7Gkr.jpg"},
    "Gainage": {"groupe": "Abdos", "image": "https://i.imgur.com/Wr9Oz6O.jpg"},
    "Curl barre": {"groupe": "Biceps", "image": "https://i.imgur.com/bmPVhAX.jpg"},
    "Curl haltères": {"groupe": "Biceps", "image": "https://i.imgur.com/3PhDBeY.jpg"},
    "Curl pupitre": {"groupe": "Biceps", "image": "https://i.imgur.com/Ma2XsRz.jpg"},
    "Extension poulie": {"groupe": "Triceps", "image": "https://i.imgur.com/Rr7GhAa.jpg"},
    "Barre front": {"groupe": "Triceps", "image": "https://i.imgur.com/MxJ5sEY.jpg"},
    "Mollets debout": {"groupe": "Mollets", "image": "https://i.imgur.com/9VCvjra.jpg"},
    "Mollets assis": {"groupe": "Mollets", "image": "https://i.imgur.com/sEfScKr.jpg"}
}

# Inverser pour mapping exercice -> groupe
all_exercises = list(exercise_data.keys())

# Initialisation
if "seances" not in st.session_state:
    st.session_state["seances"] = {j: [] for j in ["Lundi", "Mardi", "Mercredi", "Jeudi", "Vendredi", "Samedi", "Dimanche"]}

st.title("🏋️‍♀️ Planificateur d'Entraînement Visuel & Personnalisé")

# Choix du jour
jour = st.selectbox("📅 Choisis un jour :", list(st.session_state["seances"].keys()))

# Recherche exercice
search = st.text_input("🔍 Rechercher un exercice")
if search:
    matched = [exo for exo in all_exercises if search.lower() in exo.lower()]
else:
    matched = all_exercises

# Choix de l'exercice filtré
if matched:
    selected_exo = st.selectbox("Exercice :", matched)
    info = exercise_data[selected_exo]
    st.image(info["image"], width=400, caption=f"{selected_exo} – {info['groupe']}")
else:
    selected_exo = None

# Paramètres
if selected_exo:
    series = st.number_input("Séries", 1, 10, 3)
    reps = st.number_input("Répétitions", 1, 30, 12)
    charge = st.text_input("Charge", "Poids du corps")

    if st.button("➕ Ajouter à la séance"):
        st.session_state["seances"][jour].append({
            "Groupe": exercise_data[selected_exo]["groupe"],
            "Exercice": selected_exo,
            "Séries": series,
            "Répétitions": reps,
            "Charge": charge
        })
        st.success(f"{selected_exo} ajouté au {jour}")

# Affichage de la séance
st.subheader(f"📋 Séance du {jour}")
df = pd.DataFrame(st.session_state["seances"][jour])
if not df.empty:
    st.dataframe(df)
else:
    st.info("Aucun exercice ajouté.")

# Sauvegarde Excel
if st.button("💾 Exporter toutes les séances (Excel)"):
    all_data = []
    for j, exercices in st.session_state["seances"].items():
        for exo in exercices:
            all_data.append({"Jour": j, **exo})
    pd.DataFrame(all_data).to_excel("programme_complet.xlsx", index=False)
    st.success("Fichier Excel enregistré : programme_complet.xlsx")
