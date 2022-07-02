import causalnex
import pandas as pd
import numpy as np
import logging

#for splitting, scaling and encoding
from sklearn.preprocessing import LabelEncoder
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import MinMaxScaler
from pandas import DataFrame

#for drawing causal graph
from causalnex.structure.notears import from_pandas
from causalnex.plots import plot_structure, NODE_STYLE, EDGE_STYLE
from IPython.display import Image
from causalnex.network import BayesianNetwork
from causalnex.discretiser import Discretiser
from causalnex.discretiser.discretiser_strategy import ( DecisionTreeSupervisedDiscretiserMethod )

class CausalLearning():
    
    def __init__(self):
        logging.basicConfig(filename="../logs/causal.log", level=logging.INFO, format="time: %(asctime)s, function: %(funcName)s, module: %(name)s, message: %(message)s \n")
    
    
    def labeler(self, df, col):
        """
        A function that change categorical to numerical
        """
        le = LabelEncoder()
        df[col] = le.fit_transform(df[col])
        logging.info("successfully labeled")
        
        return(df)
    
    def splitter(self, df, rand=20, test=.2, split='t'):
        """
        A function to split the dataset to test and holdout set
        """
        train_df, valid_df = train_test_split(df, random_state=rand, test_size=test)
        if(split=='t'):
            logging.info("sucessfully returned trained dataset")
            return (train_df)
        
        elif(split=='v'):
            logging.info("successfully returned holdout dataset")
            return(valid_df)
        
        else:
            logging.info("wrong data slice")
            
    def scaler(self, df):
        """
        A function that scale a dataset
        """
        scaler = MinMaxScaler()
        # transform data
        scaled = scaler.fit_transform(df)
        print(df.shape)
        
        logging.info("scaled dataset successfully")
        return (scaled)
    
    def rename_col(self, sc, df2):
        """
        A function that rename scaled columns
        to their original name
        """
        df = DataFrame(sc)
        dic={}
        for i in range(len(df.columns.to_list())):
            dic[i]=df2.columns.to_list()[i]
        df.rename(columns = dic, inplace=True)
        
        logging.info("successfully renamed columns back to original name!")
        return df
    
    def causal_graph(self, df, sm):
        """
        A function to draw causal graph
        """
        viz = plot_structure(
            sm,
            graph_attributes={"scale": "0.8", "size": 2},
            all_node_attributes=NODE_STYLE.WEAK,
            all_edge_attributes=EDGE_STYLE.WEAK,)
        
        logging.info("successfully drawn causal graph")
        return(Image(viz.draw(format='png')))

    def jaccard_set(self, list1, list2):
        """Define Jaccard Similarity function for two sets
        """
        intersection = len(list(set(list1).intersection(list2)))
        union = (len(list1) + len(list2)) - intersection
        
        logging.info("successfully calculated jaccard index")
        return float(intersection) / union
    
    def check_edges(self,sm_lis):
        """
        A function that return edges, to know the consistent edges
        """
        i = 1

        for s in sm_lis:
            blanket = s.get_markov_blanket('diagnosis')
            print(i)
            print(blanket.edges)
            i = i+1
        logging.info("successfully returned number of edges for sm!")

    def var_parents(self):
        """
        A function to return the lists directly pointing at the target
        """
        selected = set()
        for item in blanket.edges:
            for val in item:
                if(val != "diagnosis"):
                    selected.add(val)
        selected = list(selected)
        
        logging.info("successfully returned list with variables pointing to target!")
        return(selected)
    
    def descreter(self, df, feat):
        """
        A function that changes df to discrete to be accecpted
        by Bayseian network
        """
        from causalnex.discretiser.discretiser_strategy import (
            DecisionTreeSupervisedDiscretiserMethod,
        )
        tree_discretiser = DecisionTreeSupervisedDiscretiserMethod(
            mode="single", 
            tree_params={"max_depth": 2, "random_state": 2022},
        )
        tree_discretiser.fit(
            feat_names=feat, 
            dataframe=df, 
            target_continuous=True,
            target="diagnosis",
        )
        desc_df = df.copy()
        for col in df.columns.to_list():
            desc_df[col] = tree_discretiser.transform(desc_df[[col]])
        
        logging.info("successfully returned discrete dataset!")
        return(desc_df)
    
    def bayseian(self, df, bn):
        """
        A function to create Bayesian Network
        """
    
        bn = bn.fit_node_states(df)
        bn = bn.fit_cpds(
            df, 
            method="BayesianEstimator", 
            bayes_prior="K2",
        )
        
        logging.info("successfully returned bayesian modeled dataset!")
        return df

    def view_predictions(self, bn, holdout):
        """
        A function to help viewing how the outcomes look like manually
        """
        predictions = bn.predict(holdout, "diagnosis");
        pred=pd.DataFrame()
        pred['predictions']=[i for i in predictions['diagnosis_prediction']]
        pred['true'] = [i for i in holdout['diagnosis']]
        
        logging.info("successfully returned prediction of model and holdout set!")
        return pred
    
if __name__=="__main__":
    
    cl = CausalLearning()