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
    
    def plot_graph(x, data):
        """
        A function to plot bargraph
        """
        logging.info("successfully plotted")
        plt.figure(figsize=(12, 6))
        sns.countplot(x=x, data=data, palette='rocket')
        
    def plot_violin(df, y):
        """
        A function to plot violin plot
        """
        df_n_2 = (df - df.mean()) / (df.std())
        df = pd.concat([y,df_n_2.iloc[:,0:15]],axis=1)
        df = pd.melt(df,id_vars="diagnosis", var_name="features", value_name="value")

        plt.figure(figsize=(10,10))
        sns.violinplot(x="features", y="value", hue="diagnosis", data=df,split=True, inner="quart",palette ="Set2")
        plt.xticks(rotation=90)

        df = pd.concat([y,df_n_2.iloc[:,15:30]],axis=1)
        df = pd.melt(df,id_vars="diagnosis", var_name="features", value_name='value')
        plt.figure(figsize=(10,10))
        sns.violinplot(x="features", y="value", hue="diagnosis", data=df,split=True, inner="quart",palette ="Set2")
        plt.xticks(rotation=90)
        logging.info("succesfully ploted violin plot")
        
    def check_outliers(df, y):
        """
        A function to check outliers
        """
        df_std = (df - df.mean()) / (df.std()) 
        df = pd.concat([y,df_std.iloc[:,0:10]],axis=1)
        df = pd.melt(df,id_vars="diagnosis", var_name="features", value_name='value')
        plt.figure(figsize=(17,5))
        sns.boxplot(x="features", y="value", hue="diagnosis", data=df)

        df = pd.concat([y,df_std.iloc[:,10:20]],axis=1)
        df = pd.melt(df,id_vars="diagnosis", var_name="features", value_name='value')
        plt.figure(figsize=(17,5))
        sns.boxplot(x="features", y="value", hue="diagnosis", data=df)

        df = pd.concat([y,df_std.iloc[:,20:30]],axis=1)
        df = pd.melt(df,id_vars="diagnosis", var_name="features", value_name='value')
        plt.figure(figsize=(20,5))
        sns.boxplot(x="features", y="value", hue="diagnosis", data=df)
        logging.info("plot outliers")
        
    def joint_plot(df, col1, col2):
        """
        A function to plot joint plot
        """
        sns.set(style="white", color_codes=True)
        jp=sns.jointplot(df.loc[:,col1], df.loc[:,col2], kind="reg",color="b")
        r, p = stats.pearsonr(df.loc[:,col1], df.loc[:,col2])
        jp.ax_joint.annotate(f'$\\rho = {r:.3f}, p = {p:.3f}$',
                        xy=(0.1, 0.9), xycoords='axes fraction',
                        ha='left', va='center',
                        bbox={'boxstyle': 'round', 'fc': 'powderblue', 'ec': 'navy'})
        logging.info("successfully plotted joint plot")