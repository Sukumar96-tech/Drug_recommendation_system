import streamlit as st
import pandas as pd
import pickle

# load model
model = pickle.load(open("drug_model.pkl","rb"))

st.title("💊 Drug Recommendation System")

st.write("Enter Patient Symptoms")

# -------- INPUT FIELDS --------
name = st.text_input("Enter Patient Name")

age = st.number_input("Age", 1, 100, 25)

gender = st.selectbox("Gender", ["Male","Female"])

fever = st.selectbox("Fever", ["No","Yes"])
cough = st.selectbox("Cough", ["No","Yes"])
cold = st.selectbox("Cold", ["No","Yes"])
headache = st.selectbox("Headache", ["No","Yes"])
fatigue = st.selectbox("Fatigue", ["No","Yes"])
sore_throat = st.selectbox("Sore Throat", ["No","Yes"])
runny_nose = st.selectbox("Runny Nose", ["No","Yes"])
nausea = st.selectbox("Nausea", ["No","Yes"])
vomiting = st.selectbox("Vomiting", ["No","Yes"])
body_pain = st.selectbox("Body Pain", ["No","Yes"])


# -------- CONVERT VALUES --------

gender = 1 if gender == "Male" else 0

def convert(val):
    return 1 if val == "Yes" else 0

fever = convert(fever)
cough = convert(cough)
cold = convert(cold)
headache = convert(headache)
fatigue = convert(fatigue)
sore_throat = convert(sore_throat)
runny_nose = convert(runny_nose)
nausea = convert(nausea)
vomiting = convert(vomiting)
body_pain = convert(body_pain)


# -------- PREDICT --------
if st.button("Predict Drug"):

    # check if name is empty
    if name.strip() == "":
        st.warning("Please enter patient name")

    else:

        patient = pd.DataFrame([[

            age,
            gender,
            fever,
            cough,
            cold,
            headache,
            fatigue,
            sore_throat,
            runny_nose,
            nausea,
            vomiting,
            body_pain

        ]], columns=[
            'age','gender','fever','cough','cold','headache','fatigue',
            'sore_throat','runny_nose','nausea','vomiting','body_pain'
        ])

        # -------- CHECK IF ALL SYMPTOMS ARE 0 --------

        symptoms_sum = fever + cough + cold + headache + fatigue + sore_throat + runny_nose + nausea + vomiting + body_pain

        if symptoms_sum == 0:

            st.warning(f"{name}, no symptoms detected. No medication recommended.")

        else:

            prediction = model.predict(patient)[0]

            st.success(f"💊 {name}, the recommended drug for your symptoms is: {prediction}")

            # -------- USER INPUT SUMMARY --------
            st.subheader("🧾 Patient Information")

            st.write(f"Age: {age}")
            st.write(f"Gender: {'Male' if gender == 1 else 'Female'}")

            st.write("### Symptoms Selected")

            symptoms = {
                "Fever": fever,
                "Cough": cough,
                "Cold": cold,
                "Headache": headache,
                "Fatigue": fatigue,
                "Sore Throat": sore_throat,
                "Runny Nose": runny_nose,
                "Nausea": nausea,
                "Vomiting": vomiting,
                "Body Pain": body_pain
            }

            for key, value in symptoms.items():
                if value == 1:
                    st.write(f"✔ {key}")

            # -------- MEDICINE INFO --------
            st.subheader("💊 Medicine Information")

            st.write(f"{prediction} is commonly used to relieve symptoms such as fever, pain, and mild infections depending on the condition.")

            # -------- BLINKIT LINK --------
            blinkit_link = f"https://blinkit.com/s/?q={prediction}"

            st.markdown(f"⚡ [Order {prediction} on Blinkit]( {blinkit_link} )")

            # -------- DISCLAIMER --------
            st.warning("⚠ This AI system is for educational purposes only. Always consult a doctor before taking medication.")