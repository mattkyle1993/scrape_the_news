import requests
import psutil    
import os
import glob
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.tree import DecisionTreeClassifier
from sklearn.metrics import accuracy_score
from datetime import datetime
import time
import math
import codecs
import pathlib
import sys
import re
import random
import requests
from bs4 import BeautifulSoup
import joblib
from sklearn.datasets import make_hastie_10_2
from sklearn.ensemble import GradientBoostingClassifier

class ArticleURLGuesserModel():

    def __init__(self,new_joblib=False):
        self.new_joblib = new_joblib
        pass

    def article_guesser_model_builder(self,max_depth=10,new_joblib=False,save_csv=False):
        data = pd.read_csv("article_urls_model/test_url_parts_count.csv")

        X = data.drop(['URL', 'is_article','Unnamed: 0'], axis=1)
        y = data['is_article']

        X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.15, random_state=42,)

        model = GradientBoostingClassifier(n_estimators=250, learning_rate=1, max_depth=5, random_state=0).fit(X_train, y_train)

        # model = DecisionTreeClassifier(max_depth=max_depth)
        # model.fit(X_train, y_train)

        y_pred = model.predict(X_test)

        accuracy = accuracy_score(y_test, y_pred)
        print(f'Accuracy: {accuracy:.2f}')

        # Compare y_pred to y_test
        comparison_df = pd.DataFrame({
            'Actual': y_test.values,
            'Predicted': y_pred
        })

        timestamp = datetime.now().strftime('%Y-%m-%d_%H-%M-%S')
        comparison_df_filename = f'article_urls_model/model_output_y_test_y_pred/y_true_y_pred_{timestamp}.csv'
        if save_csv == True:
            comparison_df.to_csv(comparison_df_filename, index=True)

        true_pos = 0
        true_neg = 0
        false_pos = 0
        false_neg = 0
        for true, pred in zip(y_test.values,y_pred):
            if true == 1:
                if true == pred:
                    true_pos+=1
                if true > pred:
                    false_neg+=1
            if true == 0:
                if true == pred:
                    true_neg+=1
                if true < pred:
                    false_pos+=1
        
        print("true pos:",true_pos)
        print("true neg:",true_neg)
        print("false pos:",false_pos)
        print("false neg:", false_neg)

        feature_importances = model.feature_importances_
        feature_names = X.columns
        important_features = sorted(zip(feature_names, feature_importances), key=lambda x: x[1], reverse=True)
        print('\nMost important features:')
        for feature, importance in important_features:
            print(f'{feature}: {importance:.4f}')

        # timestamp = datetime.now().strftime('%Y-%m-%d_%H-%M-%S')

        output_filename = f'article_urls_model/model_output_important_features/important_features_{timestamp}.csv'
        important_features_df = pd.DataFrame(important_features, columns=['Feature', 'Importance'])
        if save_csv == True:
            important_features_df.to_csv(output_filename, index=False)

        print(f'\nImportant features saved to {output_filename}')

        if new_joblib == True:

            # Train and save the model
            model = DecisionTreeClassifier(max_depth=max_depth)
            model.fit(X_train, y_train)
            joblib.dump(model, 'article_urls_model/joblibs/ALPHA_trained_article_url_guesser_model.joblib')
        
    def prepare_url_data_for_model(self,urls_list=[],save_csv=False,return_data=False,model_guess=False):


        """
        how to make new training data: take a list of urls in a txt file, some articles and some not, and go down the list and put ",1" next to articles and leave the rest alone. then feed that into this model builder.
        """

        # Initialize data lists
        website_format_counts = []
        section_counts = []
        hyphen_counts = []
        slash_counts = []
        twitter_format_counts = []
        non_alphabetic_counts = []
        url_len = []
        is_article = []
        number_of_alpha = []

        if len(urls_list) == 0:
            urls_list = []
            with open("article_urls_model/testing_urls_with_dummy.txt","r",encoding="utf-8") as file:
                for line in file:
                    if line not in urls_list:
                        urls_list.append(line)
        else:
            urls_list = urls_list
        for i in range(len(urls_list)):
                url = urls_list[i]
                url = url.strip() # remove trailing white space
                if url.endswith(", 1") or url.endswith(",1"):
                    is_article.append(1)
                    url = url[:-3] # remove ", 1" from url string
                else:
                    is_article.append(0)
                try:
                    website_format_counts.append(len(re.findall(r"https://[^\s]+", url)))
                except:
                    website_format_counts.append(0)
                try:
                    section_counts.append(len(re.findall(r"/\w+/", url)))
                except:
                    section_counts.append(0)
                try:
                    hyphen_counts.append(url.count("-"))
                except:
                    hyphen_counts.append(0)
                try:
                    slash_counts.append(url.count("/"))
                except:
                    slash_counts.append(0)
                try:
                    twitter_format_counts.append(url.count("twitter.com"))
                except:
                    website_format_counts.append(0)
                try:
                    non_alphabetic_counts.append(len(re.findall(r"[&%]", url)))
                except:
                    non_alphabetic_counts.append(0)
                try:
                    url_len.append(len(url))
                except:
                    url_len.append(0)
                try:
                    alpha_ct = len([ele for ele in url if ele.isalpha()])
                    number_of_alpha.append(alpha_ct)
                except:
                    number_of_alpha.append(0)
        # Create a DataFrame
        if model_guess == True:
            df = pd.DataFrame({
                "Website Format Count": website_format_counts,
                "Entertainment Section Count": section_counts,
                "Hyphen Count": hyphen_counts,
                "Slash Count": slash_counts,
                "Twitter Count": twitter_format_counts,
                "Non-Alphabetic Count": non_alphabetic_counts,
                "url_len":url_len,
                "alpha_ct":number_of_alpha
            })
        if model_guess == False:
            df = pd.DataFrame({
                "URL": urls_list,
                "is_article":is_article,
                "Website Format Count": website_format_counts,
                "Entertainment Section Count": section_counts,
                "Hyphen Count": hyphen_counts,
                "Slash Count": slash_counts,
                "Twitter Count": twitter_format_counts,
                "Non-Alphabetic Count": non_alphabetic_counts,
                "url_len":url_len,
                "alpha_ct":number_of_alpha
            })
        if save_csv == True:
            df.to_csv("article_urls_model/test_url_parts_count.csv")
        if return_data == True:
            return df

    def run_article_guesser_model(self,url,save_article_guesses=False,print_results=False,print_both_results=False,print_only_neg_results=False):
        """
        takes a given URL and predicts if it's an article or not, then returns the answer: 1 or 0.
        """
        model = joblib.load('article_urls_model/joblibs/ALPHA_trained_article_url_guesser_model.joblib')
        new_features = self.prepare_url_data_for_model(urls_list=[url],return_data=True,model_guess=True)
        try:
            prediction = model.predict(new_features)
        except Exception as error:
            print("error:",str(error))
        if save_article_guesses == True:
            with open('article_urls_model/model_guesses_output/model_guesses.txt', 'a') as file:
                if prediction == 1:
                    text_to_append = f"{url},1\n"
                if prediction == 0:
                    text_to_append = f"{url}\n"
                file.write(text_to_append)
        if print_results==True:
            if prediction == 1:
                pred = "Guess: is an article"
            if prediction == 0:
                pred = "Guess: is not an article"
            if True:
                if print_only_neg_results == True:
                    print_both_results = True
                    skip = True
                if print_both_results == True:
                    if skip == False:
                        print("article-guess-model prediction:",(url,pred))
                    if print_only_neg_results == True:
                        if prediction == 0:
                            print("article-guess-model prediction:",(url,pred))
                else:
                    if prediction == 1:
                        print("article-guess-model prediction:",(url,pred))

        

        return prediction
    
# GUESS = ArticleURLGuesserModel()
# GUESS.prepare_url_data_for_model(save_csv=True)
# GUESS.article_guesser_model_builder(new_joblib=True)