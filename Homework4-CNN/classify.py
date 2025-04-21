import tensorflow as tf
import sys

def classify(model, image_dir: str) -> tuple:
    """
    takes model and an image directory and classifies the 
    image using the model, returning the classification tuple
    """
    img = tf.keras.utils.load_img(image_dir, target_size=(100,100))

    # convert image to tensor
    img_array = tf.expand_dims(tf.keras.utils.img_to_array(img), 0)

    # run image through model and return result
    return model.predict(img_array, verbose=0)[0]

def classifyAndPrint(model, image_dir: str) -> None:
    """
    classify and print calls the classify method and prints 
    f"{image_dir} is a {cat/dog}" depending on the classify
    method
    """
    classification = classify(model, image_dir)

    if classification[0] >  classification[1]:
        print(f"{image_dir} is a picture of a cat")
    else:
        print(f"{image_dir} is a picture of a dog")

if __name__ == "__main__":
    # check arg count
    if (len(sys.argv) < 3):
        print("INVALID USAGE; python classify.py <model> <img1> ... <imgN>")
    
    # get images from args
    images = sys.argv[2:]

    # load model
    model = tf.keras.models.load_model(sys.argv[1])

    # classify each image and print result
    for image in images:
        classifyAndPrint(model, image)