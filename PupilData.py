"""
Using ZMQ, receive gaze data from Pupil, publish/subscribe detected objects in world camera (using darkflow)
"""
import zmq
from msgpack import loads
import time
from  multiprocessing import Process

def getGazeData():
    context = zmq.Context()
    # open a req port to talk to pupil
    addr = '127.0.0.1'  # remote ip or localhost
    req_port = "50020"  # same as in the pupil remote gui
    req = context.socket(zmq.REQ)
    req.connect("tcp://{}:{}".format(addr, req_port))
    # ask for the sub port
    req.send_string('SUB_PORT')
    sub_port = req.recv_string()

    # open a sub port to listen to pupil
    sub = context.socket(zmq.SUB)
    sub.connect("tcp://{}:{}".format(addr, sub_port))

    # set subscriptions to topics
    # recv just pupil/gaze/notifications
    # sub.setsockopt_string(zmq.SUBSCRIBE, 'pupil.')
    try:
        sub.setsockopt_string(zmq.SUBSCRIBE, 'gaze')
    except TypeError:
        sub.setsockopt(zmq.SUBSCRIBE, 'gaze')
    # sub.setsockopt_string(zmq.SUBSCRIBE, 'notify.')
    # sub.setsockopt_string(zmq.SUBSCRIBE, 'logging.')
    # or everything:
    # sub.setsockopt_string(zmq.SUBSCRIBE, '')

    while True:
        try:
            topic = sub.recv_string()
            msg = sub.recv()
            msg = loads(msg, encoding='utf-8')
            gaze_coord = msg['norm_pos']
            confidence = msg['confidence']
            gaze_data = {'gaze_coord': gaze_coord, 'confidence': confidence}
            #print ('x,y: ', gaze_coord,'\n', 'confidence: ', confidence,'\n')
            #print("\n{}: {}".format(topic, msg))
            return gaze_data
        except KeyboardInterrupt:
            break
            return None


# def publish_detected_object(label):
#     context = zmq.Context()
#     socket = context.socket(zmq.PUB)
#     addr = '127.0.0.1'  # remote ip or localhost
#     port = "5556"  # same as in the pupil remote gui
#     socket.bind("tcp://{}:{}".format(addr, port))

#     while True:
#         topic = 'detected_object'
#         print ('%s %s' % (topic, label))
#         try:
#             socket.send_string('%s %s' % (topic, label))
#         except TypeError:
#             socket.send('%s %s' % (topic, label))
#         # socket.send_string('%s %s' % (topic, label))
#         time.sleep(2)
#         # return label


def subscribe_detected_object():
    context = zmq.Context()
    socket = context.socket(zmq.SUB)
    addr = '127.0.0.1'  # remote ip or localhost
    port = "5556"  # same as in the pupil remote gui
    print('retrieving objects...')
    socket.connect("tcp://{}:{}".format(addr, port))

    #subscribe to detected_objects topic
    while True:
        try:
            socket.setsockopt_string(zmq.SUBSCRIBE, 'detected_object')
        except TypeError:
            socket.setsockopt(zmq.SUBSCRIBE, 'detected_object')
        obj = socket.recv_string()
        print(obj)
        return obj