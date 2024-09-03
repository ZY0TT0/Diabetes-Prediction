import numpy as np
import pandas as pd
import streamlit as st
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score, classification_report
from sklearn.ensemble import RandomForestClassifier
from sklearn.preprocessing import StandardScaler
from PIL import Image

# Load the diabetes dataset
diabetes_df = pd.read_csv('D:\College\Pred Projects\Pro1\diabetes.csv')

# Split the data into input and target variables
X = diabetes_df.drop('Outcome', axis=1)
y = diabetes_df['Outcome']

# Scale the input variables using StandardScaler
scaler = StandardScaler()
X = scaler.fit_transform(X)

# Split the data into training and testing sets
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=1)

# Create a Random Forest model
rf = RandomForestClassifier(n_estimators=100, random_state=1)

# Train the model on the training set
rf.fit(X_train, y_train)

# Make predictions on the training and testing sets
train_y_pred = rf.predict(X_train)
test_y_pred = rf.predict(X_test)

# Calculate the accuracy of the model on the training and testing sets
train_acc = accuracy_score(train_y_pred, y_train)
test_acc = accuracy_score(test_y_pred, y_test)

# Create the Streamlit app
def app():

    img = Image.open(r"D:\College\Pred Projects\Pro1\img.jpeg")
    img = img.resize((200,200))
    st.image(img,caption="Diabetes Image",width=200)

    st.title('Diabetes Prediction')

    # Create the input form for the user to input new data
    st.sidebar.title('Input Features')
    preg = st.sidebar.slider('Pregnancies', 0, 17, 3)
    glucose = st.sidebar.slider('Glucose', 0, 199, 117)
    bp = st.sidebar.slider('Blood Pressure', 0, 122, 72)
    skinthickness = st.sidebar.slider('Skin Thickness', 0, 99, 23)
    insulin = st.sidebar.slider('Insulin', 0, 846, 30)
    bmi = st.sidebar.slider('BMI', 0.0, 67.1, 32.0)
    dpf = st.sidebar.slider('Diabetes Pedigree Function', 0.078, 2.42, 0.3725, 0.001)
    age = st.sidebar.slider('Age', 21, 81, 29)

    # Make a prediction based on the user input
    input_data = [preg, glucose, bp, skinthickness, insulin, bmi, dpf, age]
    input_data_nparray = np.asarray(input_data)
    reshaped_input_data = input_data_nparray.reshape(1, -1)
    reshaped_input_data = scaler.transform(reshaped_input_data)
    prediction = rf.predict(reshaped_input_data)

    # Display the prediction to the user
    st.write('Based on the input features, the model predicts:')
    if prediction == 1:
        st.warning('This person has diabetes.')
    else:
        st.success('This person does not have diabetes.')

    # Display the model accuracy
    st.header('Model Accuracy')
    st.write(f'Train set accuracy: {train_acc:.2f}')
    st.write(f'Test set accuracy: {test_acc:.2f}')
    
    # Display the class distribution
    st.header('Class Distribution')
    st.write(diabetes_df['Outcome'].value_counts())
    
    # Display the classification report
    st.header('Classification Report')
    st.text(classification_report(y_test, test_y_pred))

    # Display some summary statistics about the dataset
    st.header('Dataset Summary')
    st.write(diabetes_df.describe())

    st.header('Distribution by Outcome')
    st.write(diabetes_df.groupby('Outcome').mean())

if __name__ == '__main__':
    app()
