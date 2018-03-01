import os
import cv2
import numpy as np
import pprint

import sys

def add_path(path):
    if path not in sys.path:
        sys.path.insert(0, path)

this_dir = os.path.dirname(__file__)

lib_path = os.path.join(this_dir, '..', 'libs', 'DeformableConvNet', 'lib')
add_path(lib_path)

lib_path = os.path.join(this_dir, '..', 'libs', 'DeformableConvNet', 'src')
add_path(lib_path)

from config.config import config, update_config
from utils.image import resize, transform

os.environ['PYTHONUNBUFFERED'] = '1'
os.environ['MXNET_CUDNN_AUTOTUNE_DEFAULT'] = '0'
os.environ['MXNET_ENABLE_GPU_P2P'] = '0'

# path to symbol current file
cur_path = os.path.abspath(os.path.dirname(__file__))
# update config with experiment config yaml
update_config(os.path.join(cur_path, '..', 'conf', 'detectors', 'DeformableDetector', "rfcn_coco_demo.yaml"))

import mxnet as mx
from core.tester import im_detect, Predictor
from symbols import *
from utils.load_model import load_param
from utils.show_boxes import show_boxes
from utils.tictoc import tic, toc
from nms.nms import py_nms_wrapper, cpu_nms_wrapper, gpu_nms_wrapper

import signal
import sys
signal.signal(signal.SIGTERM, signal.SIG_DFL)


class DeformableDetector(object):
    def __init__(self):
        pprint.pprint(config)
        sym_instance = eval(config.symbol + '.' + config.symbol)()
        self.symbol = sym_instance.get_symbol(config, is_train=False)

        self.scales = config.SCALES[0]
        self.data_shape_conf = [[('data', (1, 3, self.scales[0], self.scales[1])), ('im_info', (1, 3))]]
        self.arg_params, self.aux_params = load_param(os.path.join(cur_path, '..', 'conf', 'detectors', 'DeformableDetector', "rfcn_dcn_coco"), 0, process=True)

        self.data_names = ['data', 'im_info']
        self.predictor = Predictor(self.symbol, ['data', 'im_info'], [],
                context=[mx.gpu(0)], max_data_shapes=self.data_shape_conf,
                provide_data=self.data_shape_conf,
                provide_label=[None],
                arg_params=self.arg_params, aux_params=self.aux_params
                )
        self.nms = gpu_nms_wrapper(config.TEST.NMS, 0)

    def predict(self, im):
        data = []
        im, im_scale = resize(im, self.scales[0], self.scales[1],
                stride=config.network.IMAGE_STRIDE)
        im_tensor = transform(im, config.network.PIXEL_MEANS)
        im_info = np.array([[im_tensor.shape[2], im_tensor.shape[3], im_scale]], dtype=np.float32)
        data = {'data': im_tensor, 'im_info': im_info}
        data = [[mx.nd.array(data[self.data_names[0]]), mx.nd.array(data[self.data_names[1]])]]
        data_batch = mx.io.DataBatch(data=data, label=[], pad=0, index=0,
            provide_data=[[(k, v.shape) for k, v in zip(self.data_names, data[0])]], provide_label=[None])
        tic()
        scores, boxes, data_dict = im_detect(self.predictor, data_batch, self.data_names, [im_scale], config)
        boxes = boxes[0].astype('f')
        scores = scores[0].astype('f')
        dets_nms = []
        for j in range(1, scores.shape[1]):
            cls_scores = scores[:, j, np.newaxis]
            cls_boxes = boxes[:, 4:8] if config.CLASS_AGNOSTIC else boxes[:, j * 4:(j + 1) * 4]
            cls_dets = np.hstack((cls_boxes, cls_scores))
            keep = self.nms(cls_dets)
            cls_dets = cls_dets[keep, :]
            cls_dets = cls_dets[cls_dets[:, -1] > 0.7, :]
            dets_nms.append(cls_dets)
        print 'testing {:.4f}s'.format(toc())
        return 0


from threading import Thread
from Queue import Queue, Empty


class DetectorWrapper(Thread):
    def __init__(self, q_task, q_result):
        super(DetectorWrapper, self).__init__()
        self.q_task = q_task
        self.q_result = q_result
        self.detector = DeformableDetector()
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


if __name__ == "__main__":
    # dd = DeformableDetector()
    image_names = ['COCO_test2015_000000000891.jpg', 'COCO_test2015_000000001669.jpg'] * 10
    # for im_name in image_names:
    #     assert os.path.exists(cur_path + '/../demo/' + im_name), ('%s does not exist'.format('../demo/' + im_name))
    #     im = cv2.imread(cur_path + '/../demo/' + im_name, cv2.IMREAD_COLOR | print "del3"cv2.IMREAD_IGNORE_ORIENTATION)
    #     dd.predict(im)

    q_tasks = Queue()
    q_result = Queue()

    a = DetectorWrapper(q_tasks, q_result)
    # b = DetectorWrapper(q_tasks, q_result)

    a.start()
    # b.start()


    for im_name in image_names:
        p = os.path.join(cur_path, im_name)
        assert os.path.exists(p), ('%s does not exist'.format('../demo/' + im_name))
        im = cv2.imread(p, cv2.IMREAD_COLOR | cv2.IMREAD_IGNORE_ORIENTATION)
        q_tasks.put(im)

    for im_name in image_names:
        print q_result.get()
        q_result.task_done()

    a.stop()
    # b.stop()

    a.join()
    # b.join()

    q_tasks.join()
    q_result.join()

    print "Done!"
