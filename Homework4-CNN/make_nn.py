import tensorflow as tf
import os
import sys
import pathlib
import random as rng

# variables that cannot be tinkered with
NUM_CLASSES = 2
IMG_SIZE = (100,100)
NUM_EPOCHS = 1

# variables that can be tinkered with
VALIDATION_SPLIT = 0.2
BATCH_SIZE = 32

def __createDataSets(dir: str):
    # load directory
    data_dir = pathlib.Path(dir).with_suffix('')

    # errors
    if (not pathlib.Path(data_dir).is_dir()):
        print("ERROR: Path does not exist")
        sys.exit(9)
    if (len(os.listdir(data_dir)) == 0):
        print("ERROR: No files found in directory")
        sys.exit(9)

    rng_seed = rng.randint(1,1000)

    # create training set
    training_set = tf.keras.utils.image_dataset_from_directory(
        data_dir,
        validation_split=VALIDATION_SPLIT,
        # create labels; since training data is read in ascii order, all cat data 
        # will be read first, then all dog data. basically, we have 0 label (cats)
        # however many many times a "c*.jpg" file shows up in that directory.
        # of note: this breaks if any images are not either c* or d*.
        labels=[0 for i in range(len(list(data_dir.glob('c*.jpg'))))] + [1 for i in range(len(list(data_dir.glob('d*.jpg'))))],
        subset="training",
        seed=rng_seed,
        image_size=IMG_SIZE,
        batch_size=BATCH_SIZE)
    
    # create validation set
    validation_set = tf.keras.utils.image_dataset_from_directory(
        data_dir,
        validation_split=VALIDATION_SPLIT,
        labels=[0 for i in range(len(list(data_dir.glob('c*.jpg'))))] + [1 for i in range(len(list(data_dir.glob('d*.jpg'))))],
        subset="validation",
        seed=rng_seed,
        image_size=IMG_SIZE,
        batch_size=BATCH_SIZE)
    
    # tune data
    training_set = training_set.cache().prefetch(buffer_size=tf.data.AUTOTUNE)
    validation_set = validation_set.cache().prefetch(buffer_size=tf.data.AUTOTUNE)

    return (training_set, validation_set)

def train(dataset: tuple):
    # this was my best architecture; i found it relatively early and spent many
    # long hours trying to beat it, but nothing did quite as well on my test set
    model = tf.keras.Sequential([
        tf.keras.layers.Rescaling(1./255),
        tf.keras.layers.Conv2D(16, 5, activation='relu'),
        tf.keras.layers.MaxPooling2D(),
        tf.keras.layers.Conv2D(32, 5, activation='relu'),
        tf.keras.layers.MaxPooling2D(),
        tf.keras.layers.Conv2D(64, 3, activation='relu'),
        tf.keras.layers.MaxPooling2D(),
        tf.keras.layers.Conv2D(128, 3, activation='relu'),
        tf.keras.layers.MaxPooling2D(),
        tf.keras.layers.Flatten(),
        tf.keras.layers.Dense(32, activation='relu'),
        tf.keras.layers.Dropout(0.5),
        tf.keras.layers.Dense(NUM_CLASSES)
    ])

    # define model compilation things
    model.compile(
        optimizer='adam', # this was almost a constant, but I only messed with non-adam ones like twice
        loss=tf.keras.losses.SparseCategoricalCrossentropy(from_logits=True),
        metrics=['accuracy']
    )

    # actually train the model
    model.fit(
        dataset[0], # training set
        validation_data=dataset[1], # validation set
        epochs=NUM_EPOCHS
    )

    return model

if __name__ == "__main__":
    if (len(sys.argv) != 3):
        print("INVALID USAGE; python make_nn.py <training directory> <model name to save>")
        sys.exit(9)
    datasets = __createDataSets(sys.argv[1])
    model = train(datasets)
    model.save(sys.argv[2], include_optimizer = False)