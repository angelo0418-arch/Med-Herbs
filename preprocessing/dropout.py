from tensorflow.keras.layers import Dropout

def add_dropout(rate):
    """Function para sa Dropout layer"""
    return Dropout(rate)
