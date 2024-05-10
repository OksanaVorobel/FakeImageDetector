from matplotlib import pyplot as plt
import tensorflow as tf
from sklearn.model_selection import train_test_split
import keras


from app.cnn_model.model import model
from app.cnn_model.data_preprocessing import get_ela_split_data
from app.core.config import model_config

XX, YY = get_ela_split_data()
X_train, X_val, Y_train, Y_val = train_test_split(XX, YY, test_size=0.2, random_state=5)
del XX, YY

early_stop = tf.keras.callbacks.EarlyStopping(monitor='accuracy', patience=5)
check_point = tf.keras.callbacks.ModelCheckpoint('model_{}.keras'.format('new_ela'),
                                                 monitor='accuracy',
                                                 save_best_only=True)

optimizer = keras.optimizers.Adam(learning_rate=0.0001)
model.compile(optimizer=optimizer,
              loss=tf.keras.losses.CategoricalCrossentropy(),
              metrics=['accuracy'])


def train_model(model, epochs=model_config.epochs, batch_size=model_config.batch_size):
    history = model.fit(
        X_train, Y_train,
        batch_size=batch_size,
        epochs=epochs,
        validation_data=(X_val, Y_val),
        verbose=2,
        callbacks=[early_stop, check_point],
    )

    fig, ax = plt.subplots(2, 1)
    ax[0].plot(history.history['loss'], color='b', label="Training loss")
    ax[0].plot(history.history['val_loss'], color='r', label="Validation loss")
    legend = ax[0].legend(loc='best', shadow=True)

    ax[1].plot(history.history['accuracy'], color='b', label="Training accuracy")
    ax[1].plot(history.history['val_accuracy'], color='r', label="Validation accuracy")
    legend = ax[1].legend(loc='best', shadow=True)

    plt.show()


# train_model(model)
