import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import scipy.stats as stats

class EDA:
    
    def __init__(self):
         logging.basicConfig(filename="../logs/keep_track.log", level=logging.INFO, format="time: %(asctime)s, function: %(funcName)s, module: %(name)s, message: %(message)s \n")
    
    def unique_col(df):
        """
        A function to return unique columns
        """
        logging.info("successfully returned unique cols")
        return(df.apply(lambda x: len(x.unique())).sort_values(ascending=False).head(10))
    
    def duplicate(df):
        """
        A function to return duplicates
        """
        dups = df.duplicated()
        print("There are duplicates: {}".format(dups.any()))
        logging.info("successfully returned duplicates")
        return(df[dups])
    
    def df_info(df):
        """
        A function to return dataset info
        """
        logging.info("successfully displayed info")
        return (df.describe().T.style.bar(subset=['mean'], color='#205ff2').background_gradient(subset=['std'], cmap='Reds').background_gradient(subset=['50%'], cmap='coolwarm'))
    
    