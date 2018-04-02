import os

import numpy as np

from threading import Thread
from Queue import Empty

from config.config import config, update_config
from utils.image import resize, transform

os.environ['PYTHONUNBUFFERED'] = '1'
os.environ['MXNET_CUDNN_AUTOTUNE_DEFAULT'] = '0'
os.environ['MXNET_ENABLE_GPU_P2P'] = '0'

# path to symbol current file
cur_path = os.path.abspath(os.path.dirname(__file__))
# update config with experiment config yaml
update_config(os.path.join(cur_path, '..', 'conf', "spot_resnet_v1_101_rfcn_dcn_end2end_ohem.yaml"))

import mxnet as mx
from core.tester import im_detect, Predictor
from symbols import *
from utils.load_model import load_param
from nms.nms import py_nms_wrapper, cpu_nms_wrapper, gpu_nms_wrapper

import logging

logger = logging.getLogger(__name__)


class DeformableDetector(object):
    def __init__(self):
        sym_instance = eval(config.symbol + '.' + config.symbol)()
        self.symbol = sym_instance.get_symbol(config, is_train=False)
        self.classes = ['box', 'robot']
        logging.debug("Classes: {}".format(self.classes))
        self.scales = config.SCALES[0]
        logging.debug("Scales: {}".format(self.scales))
        self.data_shape_conf = [[('data', (1, 3, self.scales[0], self.scales[1])), ('im_info', (1, 3))]]
        self.arg_params, self.aux_params = load_param(os.path.join(cur_path, '..', 'models', "rfcn_voc"), 0, process=True)

        self.data_names = ['data', 'im_info']
        self.predictor = Predictor(self.symbol, ['data', 'im_info'], [],
                context=[mx.gpu(0)], max_data_shapes=self.data_shape_conf,
                provide_data=self.data_shape_conf,
                provide_label=[None],
                arg_params=self.arg_params, aux_params=self.aux_params
                )
        self.nms = gpu_nms_wrapper(config.TEST.NMS, 0)
        logging.info("Deformable detector initialized")

    def predict(self, im):
        im, im_scale = resize(im, self.scales[0], self.scales[1],
                stride=config.network.IMAGE_STRIDE)
        im_tensor = transform(im, config.network.PIXEL_MEANS)
        im_info = np.array([[im_tensor.shape[2], im_tensor.shape[3], im_scale]], dtype=np.float32)
        data = {'data': im_tensor, 'im_info': im_info}
        data = [[mx.nd.array(data[self.data_names[0]]), mx.nd.array(data[self.data_names[1]])]]
        data_batch = mx.io.DataBatch(data=data, label=[], pad=0, index=0,
            provide_data=[[(k, v.shape) for k, v in zip(self.data_names, data[0])]], provide_label=[None])

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

        res = {}
        for idx, cls in enumerate(self.classes):
            res['{}'.format(cls)] = dets_nms[idx].tolist()
        logging.debug("Predictions: {}".format(res))
        return res


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

