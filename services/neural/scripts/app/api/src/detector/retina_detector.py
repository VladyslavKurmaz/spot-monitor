import os
from threading import Thread
from Queue import Empty

import numpy as np
import logging
import cv2
import tensorflow as tf


logger = logging.getLogger(__name__)

max_len = 1000.0

cur_path = os.path.abspath(os.path.dirname(__file__))
model_path = os.path.join(cur_path, '..', 'models', 'resnet50_pascal_05.pb')


def load_graph(frozen_graph_filename):
    # We load the protobuf file from the disk and parse it to retrieve the
    # unserialized graph_def
    with tf.gfile.GFile(frozen_graph_filename, "rb") as f:
        graph_def = tf.GraphDef()
        graph_def.ParseFromString(f.read())

    # Then, we import the graph_def into a new Graph and returns it
    with tf.Graph().as_default() as graph:
        # The name var will prefix every op/nodes in your graph
        # Since we load everything in a new graph, this is not needed
        tf.import_graph_def(graph_def, name="prefix")
    return graph


class RetinaDetector(object):
    def __init__(self):
        graph = load_graph(model_path)
        self.x = graph.get_tensor_by_name('prefix/input_1:0')
        self.y_label = graph.get_tensor_by_name('prefix/nms/ExpandDims_2:0')
        with tf.Session(graph=graph) as sess:
            self.model = sess

        logger.debug("RetinaNet loaded")

    def predict(self, im):
        alpha = max_len / max(im.shape)
        im = cv2.resize(im, None, fx=alpha, fy=alpha)

        detections = self.model.run(self.y_label, feed_dict={self.x: im[None]})
        det = detections[0]
        new_det = []
        for k, i in enumerate(det):
            if i[4:].max() > 0.5:
                new_det.append(i)

        result = {'box': [], 'robot': []}
        name_map = ['box', 'robot']
        for i in new_det:
            name = name_map[np.argmax(i[4:])]
            detect = [float(i) for i in ((i[:4] / alpha).tolist() + [i[4:].max()])]
            result[name].append(detect)

        return result


class DetectorWrapper(Thread):
    def __init__(self, q_task, q_result):
        super(DetectorWrapper, self).__init__()
        self.q_task = q_task
        self.q_result = q_result
        self.detector = RetinaDetector()
        self.stopped = False

    def run(self):
        while True:
            try:
                im = self.q_task.get(True, 1)
                result = self.detector.predict(im)
                self.q_task.task_done()
                self.q_result.put(result)
            except Empty:
                if self.stopped:
                    return
            except:
                raise

    def stop(self):
        self.stopped = True

