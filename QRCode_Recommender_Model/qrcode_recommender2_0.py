import json
import pandas as pd
import tensorflow as tf
import tensorflow_recommenders as tfrs
import numpy as np
from typing import Dict, Text
import os
import pprint
import tempfile
import matplotlib.pyplot as plt


with open("data_produk.JSON") as f:
    data = json.load(f)

masterdf = pd.json_normalize(data)
masterdf

masterdf[['Id_produk', 'Id_user', 'Nama_produk',
       'Nama_umkm', 'Kategori_produk','Harga', 'Bahan_baku' ]]

masterdf[['Id_user',
          'Id_produk',
         ]] = masterdf[['Id_user','Id_produk']].astype(str)

masterdf['Harga'] = masterdf['Harga'].astype(float)

interactions_dict = masterdf.groupby(['Id_user', 'Id_produk'])[ 'Harga'].sum().reset_index()

interactions_dict = {name: np.array(value) for name, value in interactions_dict.items()}
interactions = tf.data.Dataset.from_tensor_slices(interactions_dict)

items_dict = masterdf[['Id_produk']].drop_duplicates()
items_dict = {name: np.array(value) for name, value in items_dict.items()}
items = tf.data.Dataset.from_tensor_slices(items_dict)

interactions = interactions.map(lambda x: {
    'Id_user' : x['Id_user'],
    'Id_produk' : x['Id_produk'],
    'Harga' : float(x['Harga']),

})

items = items.map(lambda x: x['Id_produk'])

tf.random.set_seed(42)
shuffled = interactions.shuffle(150, seed=42, reshuffle_each_iteration=False)

train = shuffled.take(100)
test = shuffled.skip(80).take(20)

unique_item_titles = np.unique(np.concatenate(list(items.batch(20))))
unique_user_ids = np.unique(np.concatenate(list(interactions.batch(20).map(lambda x: x["Id_user"]))))

unique_item_titles[:10]

embedding_dimension = 10

class Recommendation(tfrs.Model):

    def __init__(self, user_model, item_model):
        super().__init__()
        item_model = tf.keras.Sequential([
                                        tf.keras.layers.experimental.preprocessing.StringLookup(
                                        vocabulary=unique_item_titles, mask_token=None),
                                        tf.keras.layers.Embedding(len(unique_item_titles) + 1, embedding_dimension)
                                        ])
        self.item_model: tf.keras.Model = item_model

        user_model = tf.keras.Sequential([
                                        tf.keras.layers.experimental.preprocessing.StringLookup(
                                        vocabulary=unique_user_ids, mask_token=None),

                                        tf.keras.layers.Embedding(len(unique_user_ids) + 1, embedding_dimension)
                                        ])
        self.user_model: tf.keras.Model = user_model


        metrics = tfrs.metrics.FactorizedTopK(
                                            candidates=items.batch(5).map(item_model)

                                            )
        task = tfrs.tasks.Retrieval(
                                    metrics=metrics
                                    )

        self.task: tf.keras.layers.Layer = task

    def compute_loss(self, features: Dict[Text, tf.Tensor], training=False) -> tf.Tensor:
        user_embeddings = self.user_model(features["Id_user"])
        positive_movie_embeddings = self.item_model(features["Id_produk"])

        return self.task(user_embeddings, positive_movie_embeddings)

item_model = tf.keras.Sequential([
                                tf.keras.layers.experimental.preprocessing.StringLookup(
                                vocabulary=unique_item_titles, mask_token=None),
                                tf.keras.layers.Embedding(len(unique_item_titles) + 1, embedding_dimension)
                                ])

user_model = tf.keras.Sequential([
                                tf.keras.layers.experimental.preprocessing.StringLookup(
                                vocabulary=unique_user_ids, mask_token=None),
                                # We add an additional embedding to account for unknown tokens.
                                tf.keras.layers.Embedding(len(unique_user_ids) + 1, embedding_dimension)
                                ])

model = Recommendation(user_model, item_model)

model.compile(optimizer=tf.keras.optimizers.Adagrad(learning_rate=0.1))

cached_train = train.shuffle(150).batch(30).cache()
cached_test = test.batch(30).cache()

## fit the model with ten epochs
model_hist = model.fit(cached_train, epochs=10)

model.evaluate(cached_test, return_dict=True)