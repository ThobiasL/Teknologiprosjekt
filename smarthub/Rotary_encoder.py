import Encoder
import time

encoder = Encoder.Encoder(14, 15)

def read_encoder(encoder,slutt):
    previous_position = -1
    position = encoder.read()
    while position != previous_position:
        position = encoder.read()


        previous_position = position
        time.sleep(0.1)

    return position