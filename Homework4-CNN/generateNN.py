import tensorflow as tf
import os
import numpy as np
import PIL
import PIL.Image
import pathlib
import matplotlib.pyplot as plt
import random as rng

def showSampleImages(dataset):
    plt.figure(figsize=(10, 10))
    for images, labels in dataset.take(1):
        for i in range(9):
            ax = plt.subplot(3, 3, i + 1)
            plt.imshow(images[i].numpy().astype("uint8"))
            plt.axis("off")
        print(labels)
    plt.show()

if __name__ == "__main__":
    DATASET_PATH = "D:/GitHub/CS431/Homework4-CNN/cats-and-dogs"

    data_dir = pathlib.Path(DATASET_PATH).with_suffix('')
    print(f"dogs: {len(list(data_dir.glob('d*.jpg')))} cats: {len(list(data_dir.glob('c*.jpg')))}")

    batch_size = 9
    img_height = 100
    img_width = 100

    seed = rng.randrange(1,1000)

    train_ds = tf.keras.utils.image_dataset_from_directory(
        data_dir,
        validation_split=0.2,
        labels=[0 for i in range(len(list(data_dir.glob('c*.jpg'))))] + [1 for i in range(len(list(data_dir.glob('d*.jpg'))))], # jank
        subset="training",
        seed=seed,
        image_size=(img_height, img_width),
        batch_size=batch_size)
    
    val_ds = tf.keras.utils.image_dataset_from_directory(
        data_dir,
        validation_split=0.2,
        labels=[0 for i in range(len(list(data_dir.glob('c*.jpg'))))] + [1 for i in range(len(list(data_dir.glob('d*.jpg'))))], # jank
        subset="validation",
        seed=seed,
        image_size=(img_height, img_width),
        batch_size=batch_size)
    
    # here's where i finished understanding everything so come back here

    normalization_layer = tf.keras.layers.Rescaling(1./255)

    normalized_ds = train_ds.map(lambda x, y: (normalization_layer(x), y))

    AUTOTUNE = tf.data.AUTOTUNE

    train_ds = train_ds.cache().prefetch(buffer_size=AUTOTUNE)
    val_ds = val_ds.cache().prefetch(buffer_size=AUTOTUNE)

    num_classes = 5

    model = tf.keras.Sequential([
        tf.keras.layers.Rescaling(1./255),
        tf.keras.layers.Conv2D(32, 3, activation='relu'),
        tf.keras.layers.MaxPooling2D(),
        tf.keras.layers.Conv2D(32, 3, activation='relu'),
        tf.keras.layers.MaxPooling2D(),
        tf.keras.layers.Conv2D(32, 3, activation='relu'),
        tf.keras.layers.MaxPooling2D(),
        tf.keras.layers.Flatten(),
        tf.keras.layers.Dense(128, activation='relu'),
        tf.keras.layers.Dense(num_classes)
        ])

    model.compile(
        optimizer='adam',
        loss=tf.keras.losses.SparseCategoricalCrossentropy(from_logits=True),
        metrics=['accuracy'])
    
    # print(train_ds.dtype)
    
    model.fit(
        train_ds,
        validation_data=val_ds,
        epochs=100
        )
    
    # showSampleImages(train_ds)

    
    

