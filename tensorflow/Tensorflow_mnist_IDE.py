#import tensorflow into program
import tensorflow as tf
import numpy as np
#Check tensorflow version
print("TensorFlow version:", tf.__version__)

#load mnist practice dataset
mnist = tf.keras.datasets.mnist

# View(mnist) #if you want to view the defined variable / dataset
(x_train, y_train), (x_test, y_test) = mnist.load_data() #load in the data array
x_train, x_test = x_train / 255.0, x_test / 255.0

#### Build Machine Learning Model ####
# Layers are functions with a known mathematical structure that
#can be reused and have trainable variables.
model = tf.keras.models.Sequential([
  tf.keras.layers.Flatten(input_shape=(28, 28)),
  tf.keras.layers.Dense(128, activation='relu'),
  tf.keras.layers.Dropout(0.2),
  tf.keras.layers.Dense(10)
])
# View(model)

#For each example, the model returns a vector of logits (vector of raw non normalized predictions) or log-odds (logarithm of odds of some event) scores for each class
predictions = model(x_train[:1]).numpy()
predictions

#tf.nn.softmax function converts logits to probabilities
tf.nn.softmax(predictions).numpy()

#Define loss function (maps an event of values of one or more variables to a real number) for training
loss_fn = tf.keras.losses.SparseCategoricalCrossentropy(from_logits=True)
#This untrained model gives probabilities close to random (1/10 for each class)
loss_fn(y_train[:1], predictions).numpy()

#Before you start training, configure and compile the model using Keras Model.compile.
#Set the optimizer class to adam, set the loss to the loss_fn function you defined earlier,
#and specify a metric to be evaluated for the model by setting the metrics parameter to accuracy.
model.compile(optimizer='adam',
              loss=loss_fn,
              metrics=['accuracy'])

#### Train and evaluate model ####
x_train= np.asarray(x_train)
y_train = np.asarray(y_train)
#Model.fit adjusts model parameters and minimize loss
model.fit(x_train, y_train, epochs=5)

#Model.evaluate checks the model's performance, usually on a validation or test set
model.evaluate(x_test,  y_test, verbose=2)

#If you want your model to return a probability, you can wrap the trained model, and attach the softmax to it:
probability_model = tf.keras.Sequential([
  model,
  tf.keras.layers.Softmax()
])

probability_model(x_test[:5])

tf.keras.models.save_model(model, 'tensorflow/cnn-mnist') #Save the model as cnn-mist
