from pyspark.ml.clustering import KMeansModel
from pyspark.ml.linalg import Vectors
from pyspark.ml.feature import PCAModel
from pyspark.ml.functions import vector_to_array
from pyspark.sql import SparkSession
from pyspark.sql.types import IntegerType
from pyspark.sql import Row
from math import inf
import pandas as pd
import pickle
import json
import os
import sys
from functools import reduce

# def get_json_file(load_dict):
#     with open('audio_test.json', 'w') as f:
#         json.dump(load_dict, f)
spark = SparkSession.builder.appName("KMeansClusters").config("setMaster", "local[2]").getOrCreate()
cur_dir_path = os.path.dirname(os.path.realpath(__file__))
print(cur_dir_path)
temp_path = f"{cur_dir_path}/Saved_S3/"
# Load PCA model
modelPath = temp_path + "/pca-model"
loadedModel = PCAModel.load(modelPath)

modelPath_kmeans = temp_path + "/kmeans-model"
load_kmeans_model = KMeansModel.load(modelPath_kmeans)



def get_user_audio_features(audio_features):
    # get_json_file(audio_features_dict)
    # file_name = 'audio_test.json'

    # Location of saved models
    # path = "dataset_construction/dataset/"

    # def get_user_audio_features(filenames):
    # filename = filenames # change accordingly

    # get_user_audio_features(os.listdir(path)) # change accordingly


    # Test data procedure
    test_df = spark.createDataFrame([Row(**audio_features)]) # change accordingly
    
    ids_of_users = test_df.select('id')
    test_df = test_df.drop('id','duration_ms','time_signature')
    test_dataset = test_df.rdd.map(lambda x:(Vectors.dense(x), 0)).toDF(["features"])
    test_dataset = test_dataset.drop('_2')

    pca_test_dataset = loadedModel.transform(test_dataset)
    count_of_rows = pca_test_dataset.count()

    # Getting cluster centers of KMeans 
    centers = load_kmeans_model.clusterCenters()

    pca_test_dataset = pca_test_dataset.drop('features')
    pca_test_dataset = pca_test_dataset.withColumn('pca_output', vector_to_array('pca_output'))

    # Predicting new cluster ids for incoming audio features
    cluster_ids = []
    min_square = inf
    for i in range(count_of_rows):
        list1 = pca_test_dataset.select('pca_output').collect()[i][0]
        for j in range(len(centers)):
            list2 = centers[j].tolist()
            squares = [(p-q) ** 2 for p, q in zip(list1, list2)]
            squares = sum(squares) ** .5
            if squares < min_square :
                cluster_id = j
                min_square = squares
        cluster_ids.append(cluster_id)
    cluster_ids = spark.createDataFrame(cluster_ids, IntegerType())
    return generate_cluster_ids(cluster_ids,ids_of_users)

def generate_cluster_ids(cluster_ids,ids_of_users): 
    cluster_ids = cluster_ids.toPandas()
    cluster_ids = cluster_ids.rename(columns={"value":"cluster_id"})
    final_df = pd.concat([cluster_ids,ids_of_users.toPandas()],axis=1)
    final = final_df.to_json(orient='index')
    final = json.loads(final)
    load_dict = {}
    for f in final:
        return final[f]['cluster_id']
        # load_dict[final[f]["id"]] = final[f]["cluster_id"]
    # with open('user_cluster_ids.pkl', 'rb') as f:
    #     data = pickle.load(f)
    # return load_dict



# if __name__ == '__main__':
#     # with open("audio_test.json", "r") as f:
#     #     load_dict = json.load(f)

#     # get_json_file(load_dict)
#     cluster_ids,ids_of_users = get_user_audio_features_working('audio_test.json')
#     cluster_ids = cluster_ids.toPandas()
#     cluster_ids = cluster_ids.rename(columns={"value":"cluster_id"})
#     final_df = pd.concat([cluster_ids,ids_of_users.toPandas()],axis=1)
#     final = final_df.to_json(orient='index')
#     final = json.loads(final)
#     load_dict = {}
#     for f in final: 
#         load_dict[final[f]["id"]] = final[f]["cluster_id"]
#     with open('user_cluster_ids.pkl', 'wb') as f:
#         pickle.dump(load_dict, f)
#     with open('user_cluster_ids.pkl', 'rb') as f:
#         data = pickle.load(f)
#     print(data)
    