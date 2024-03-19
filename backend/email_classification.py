import nltk
import pandas as pd
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
from sklearn.metrics import classification_report
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.preprocessing import LabelEncoder
from sklearn.model_selection import train_test_split
from sklearn.model_selection import cross_validate
from sklearn.naive_bayes import MultinomialNB
from imblearn.over_sampling import SMOTE
import joblib

class MultinomialNB_EmailClassification:
    def __init__(self, path):
        self.path = path
        self.df = None
        self.selected_df = None
        self.encoder = LabelEncoder()
        # Initialize the TfidfVectorizer
        self.tfidf_vectorizer = TfidfVectorizer()
        self.train_data = None
        self.test_data = None
        self.X_train_tfidf = None
        self.X_test_tfidf = None
        self.model = None
        self.y_res_pred = None
        self.y_red = None
    
    @staticmethod
    def remove_stopwords(text):
        stop_words = set(stopwords.words('english'))
        word_tokens = word_tokenize(text)
        filtered_text = [word for word in word_tokens if word not in stop_words]
        return ' '.join(filtered_text)
    
    @staticmethod
    def remove_punctuation(text):
        tokens = word_tokenize(text)
        tokens_without_punctuation = [token for token in tokens if token.isalnum()]
        return ' '.join(tokens_without_punctuation)

    @staticmethod
    def remove_stopwords_and_punctuation(text):
        return MultinomialNB_EmailClassification.remove_stopwords(MultinomialNB_EmailClassification.remove_punctuation(text))        
        
    def is_imbalance(self):
        # Calculate class proportions
        value_counts = self.selected_df['Target_Encode'].value_counts()
        min = value_counts.min()
        max = value_counts.max()
        return min/max < 0.8
    
    def load(self):
        self.df = pd.read_csv(self.path)
        return self
    
    def clean(self):
        # Selecting useful features from dataset
        self.selected_df = self.df[['Subject', 'Body', 'Targets']].copy()
        self.selected_df = self.selected_df.dropna()
        return self
    
    def preprocess(self):
        # combining Subject and Body into one column and lowercase all selected features
        self.selected_df['Subject_Body'] = self.selected_df['Subject'].str.lower() + ' ' + self.selected_df['Body'].str.lower()
        self.selected_df['Targets'] = self.selected_df['Targets'].str.lower()
        # Numerize the label
        self.selected_df['Target_Encode'] = self.encoder.fit_transform(self.selected_df['Targets'])
        # removing all useless words and punctuations
        self.selected_df['Subject_Body'].apply(MultinomialNB_EmailClassification.remove_stopwords_and_punctuation)
        # shuffling data helps to improve the performance, fairness, and robustness 
        # ensuring randomness and reducing biases in the dataset.
        self.selected_df = self.selected_df.sample(frac=1, random_state=42)
        # spliting dataset into training and testing
        self.train_data, self.test_data = train_test_split(self.selected_df[['Subject_Body', 'Target_Encode']], random_state=100)
        # applying TF-IDF
        self.X_train_tfidf = self.tfidf_vectorizer.fit_transform(self.train_data['Subject_Body'])
        self.X_test_tfidf = self.tfidf_vectorizer.transform(self.test_data['Subject_Body'])
        # Because the labels are imbalance, applying over-sampling to make them balance
        if self.is_imbalance():
            sm = SMOTE(random_state=42)
            self.X_res, self.y_res = sm.fit_resample(self.X_train_tfidf, self.train_data['Target_Encode'])
        else:
            self.X_res, self.y_res = self.X_train_tfidf, self.train_data['Target_Encode']
        
        return self
    
    def build_model(self):
        self.model = MultinomialNB(alpha= 0.1, fit_prior=True)
        self.model.fit(self.X_res, self.y_res)
        self.y_res_pred = self.model.predict(self.X_res)
        self.y_pred = self.model.predict(self.X_test_tfidf)
        
        return self
    
    def save(self, path):
        # Save the model to a file
        joblib.dump(self.model, path)
        joblib.dump(self.tfidf_vectorizer, path + 'tfidf')
        joblib.dump(self.encoder, path + 'label')
        return self
    
    def load_model(self, path):
        self.model = loaded_model = joblib.load(path)
        self.tfidf_vectorizer = joblib.load(path + 'tfidf')
        self.encoder = joblib.load(path + 'label')
        
    def predict(self, email_content):
        email = email_content[0] + ' ' + email_content[1]
        email = MultinomialNB_EmailClassification.remove_stopwords_and_punctuation(email)
        arr = self.tfidf_vectorizer.transform(pd.Series(email))
        pred = self.model.predict(arr)
        return self.encoder.classes_[pred[0]]
    
    def report(self):
        print('Training Classification Report:')
        print('******************************************************************')
        print(classification_report(self.y_res, self.y_res_pred, target_names=self.encoder.classes_))
        print('******************************************************************')
        print('Testing Classification Report:')
        print('******************************************************************')
        print(classification_report(self.test_data['Target_Encode'], self.y_pred, target_names=self.encoder.classes_))
        
        return self
        
    