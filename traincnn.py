
from keras.utils import plot_model
from keras.models import Sequential
from keras.layers import Convolution2D, Dropout, Dense, Flatten, MaxPooling2D
from keras.preprocessing.image import ImageDataGenerator, load_img
from numpy import array
from keras import regularizers
import cv2
model= Sequential()
model.add(Convolution2D(32,3,3, input_shape=(200,200,1),activation='relu'))
model.add(MaxPooling2D(pool_size=(2,2)))
model.add(Convolution2D(64,3,3, input_shape=(200,200,1),activation='relu'))
model.add(MaxPooling2D(pool_size=(2,2)))

model.add(Dropout(0.5)) 

model.add(Flatten())
model.add(Dense(output_dim = 150, activation = 'relu',
                kernel_regularizer=regularizers.l2(0.01)))

model.add(Dropout(0.5))

model.add(Dense(output_dim = 150, activation = 'relu',
                kernel_regularizer=regularizers.l2(0.01)))


model.add(Dropout(0.5))

model.add(Dense(output_dim = 150, activation = 'relu',
                kernel_regularizer=regularizers.l2(0.01)))

model.add(Dense(output_dim = 6, activation = 'softmax'))

model.compile(optimizer='adam', loss='categorical_crossentropy', metrics=['accuracy'])

traindata=ImageDataGenerator(
                                   rescale = 1./255,
                                   shear_range = 0.2,
                                   zoom_range = 0.,
                                   horizontal_flip = False
                                 )



train=traindata.flow_from_directory("Dataset/training_set",
                                               target_size = (200,200),
                                               color_mode='grayscale',
                                               batch_size=10,
                                               class_mode='categorical')





model.fit_generator(train,
                         samples_per_epoch = 1956,
                         nb_epoch = 10,
                         validation_data = test,
                         nb_val_samples = 320)

model.save_weights("weights.hdf5",overwrite=True)
model_json = model.to_json()
with open("model.json", "w") as model_file:
    model_file.write(model_json)
print("Model has been saved.")







