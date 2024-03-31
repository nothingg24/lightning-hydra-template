from typing import Any, Optional, Sequence, Union

import torch
from torch import Tensor, tensor
import math
import numpy as np
from torchmetrics.metric import Metric
from torchmetrics.utilities.checks import _check_same_shape

class NME(Metric):
    is_differentiable = True
    higher_is_better = False
    full_state_update = False
    distances: Tensor
    total: Tensor

    def __init__(self, keypoint_indices: Optional[Sequence[int]]=[36, 45], **kwargs: Any)->None:
        super().__init__(**kwargs)
        self.keypoint_indices = keypoint_indices
        self.add_state("distances", default=tensor(0.0), dist_reduce_fx="sum")
        self.add_state("total", default=tensor(0), dist_reduce_fx="sum")

    def update(self, preds: Tensor, target: Tensor)->None:
        _check_same_shape(preds, target)
        interoccular = torch.linalg.norm(target[:, self.keypoint_indices[0], :] - target[:, self.keypoint_indices[1], :], axis=1, keepdims=True) #np
        normalize_factor = np.tile(interoccular, [1, 2])
        distances = torch.linalg.norm(((preds - target) / normalize_factor[:, None, :]), axis=-1) #np
     #    distances = distances.T
     #    distances = torch.tensor(distances)
        self.distances+=distances.sum()
        self.total+=distances.numel()#len(distances)


    def compute(self)->Tensor:
        return self.distances / self.total
    
if __name__ == "__main__":
    metric=NME()
    target = tensor([[[0.9614, 0.2838],
         [0.2185, 0.3047],
         [0.6726, 0.1329],
         [0.7926, 0.1437],
         [0.4463, 0.9751],
         [0.6588, 0.8209],
         [0.2456, 0.6555],
         [0.0580, 0.3021],
         [0.6802, 0.4180],
         [0.2344, 0.6784],
         [0.2152, 0.3074],
         [0.8820, 0.9573],
         [0.3396, 0.4468],
         [0.1353, 0.5800],
         [0.0351, 0.4772],
         [0.3858, 0.9891],
         [0.3932, 0.2954],
         [0.2511, 0.5131],
         [0.3014, 0.2529],
         [0.1255, 0.4333],
         [0.0441, 0.1119],
         [0.3948, 0.6807],
         [0.5310, 0.9815],
         [0.1832, 0.1169],
         [0.6388, 0.5347],
         [0.2211, 0.0535],
         [0.2720, 0.1838],
         [0.9123, 0.8188],
         [0.4454, 0.0609],
         [0.9550, 0.9215],
         [0.5811, 0.7546],
         [0.7139, 0.0103],
         [0.2195, 0.9486],
         [0.3071, 0.4329],
         [0.3703, 0.2143],
         [0.7297, 0.8948],
         [0.2854, 0.1812],
         [0.5030, 0.4822],
         [0.0561, 0.6455],
         [0.0931, 0.3585],
         [0.8148, 0.7245],
         [0.3490, 0.2868],
         [0.3641, 0.3683],
         [0.6421, 0.8764],
         [0.2008, 0.3512],
         [0.3476, 0.8247],
         [0.9598, 0.6287],
         [0.1344, 0.1863],
         [0.9312, 0.1182],
         [0.0614, 0.7696],
         [0.3216, 0.6194],
         [0.7903, 0.9665],
         [0.0501, 0.3180],
         [0.4080, 0.2306],
         [0.3914, 0.1035],
         [0.4911, 0.8431],
         [0.4558, 0.5043],
         [0.1497, 0.1940],
         [0.4643, 0.9415],
         [0.1590, 0.6235],
         [0.9082, 0.4942],
         [0.0658, 0.3599],
         [0.2008, 0.2649],
         [0.0391, 0.6066],
         [0.4232, 0.4085],
         [0.5935, 0.3881],
         [0.9466, 0.3007],
         [0.1592, 0.1194]]])
    preds = tensor([[[0.3435, 0.8085],
         [0.3020, 0.4894],
         [0.0555, 0.7209],
         [0.3476, 0.5060],
         [0.9885, 0.2364],
         [0.2767, 0.2293],
         [0.4649, 0.2591],
         [0.9610, 0.3295],
         [0.1928, 0.9190],
         [0.1185, 0.7904],
         [0.7436, 0.4187],
         [0.1538, 0.9748],
         [0.0878, 0.5446],
         [0.2700, 0.4833],
         [0.1362, 0.2149],
         [0.1636, 0.2485],
         [0.0106, 0.4620],
         [0.0653, 0.7562],
         [0.1043, 0.4130],
         [0.5185, 0.8119],
         [0.1862, 0.0775],
         [0.6273, 0.8686],
         [0.6833, 0.8262],
         [0.4925, 0.6941],
         [0.9786, 0.1327],
         [0.3392, 0.4742],
         [0.7614, 0.9601],
         [0.4817, 0.5462],
         [0.5988, 0.3866],
         [0.4489, 0.2456],
         [0.4434, 0.6425],
         [0.2996, 0.1519],
         [0.0853, 0.4976],
         [0.4579, 0.0291],
         [0.7501, 0.2644],
         [0.6522, 0.9938],
         [0.0289, 0.3818],
         [0.8784, 0.5722],
         [0.5738, 0.2861],
         [0.5193, 0.2310],
         [0.6013, 0.9277],
         [0.0285, 0.7803],
         [0.7668, 0.8046],
         [0.4857, 0.7006],
         [0.8979, 0.3417],
         [0.1012, 0.7778],
         [0.8354, 0.1278],
         [0.7344, 0.7442],
         [0.3345, 0.6145],
         [0.5173, 0.0526],
         [0.5736, 0.9827],
         [0.9434, 0.7175],
         [0.4186, 0.5059],
         [0.3929, 0.5217],
         [0.8186, 0.1759],
         [0.8854, 0.9537],
         [0.0569, 0.9636],
         [0.9606, 0.7413],
         [0.7625, 0.3314],
         [0.5282, 0.8585],
         [0.1822, 0.5586],
         [0.0568, 0.1925],
         [0.5876, 0.3007],
         [0.3004, 0.1094],
         [0.5129, 0.1056],
         [0.6536, 0.8018],
         [0.9067, 0.7094],
         [0.7724, 0.5506]]])
    print("{:.10f}".format(metric(preds, target)))
    target=tensor([[[0.3940, 0.4120],
         [0.5349, 0.1031],
         [0.7704, 0.1679],
         [0.8431, 0.4078],
         [0.6638, 0.3705],
         [0.6933, 0.2729],
         [0.8136, 0.9683],
         [0.9164, 0.1784],
         [0.7672, 0.6941],
         [0.4054, 0.7056],
         [0.6374, 0.0772],
         [0.8067, 0.6999],
         [0.7919, 0.4348],
         [0.6349, 0.8466],
         [0.7567, 0.5539],
         [0.3897, 0.5699],
         [0.0760, 0.7210],
         [0.0343, 0.7396],
         [0.3831, 0.5522],
         [0.4501, 0.6904],
         [0.7607, 0.0043],
         [0.5653, 0.0930],
         [0.8742, 0.5506],
         [0.7548, 0.6398],
         [0.3746, 0.0674],
         [0.3373, 0.1983],
         [0.6079, 0.4156],
         [0.3852, 0.1868],
         [0.1844, 0.5433],
         [0.7582, 0.4628],
         [0.3317, 0.8808],
         [0.9874, 0.4320],
         [0.4499, 0.2178],
         [0.7902, 0.4842],
         [0.5399, 0.3484],
         [0.1056, 0.6137],
         [0.5276, 0.2098],
         [0.7210, 0.3582],
         [0.6884, 0.0322],
         [0.3580, 0.7127],
         [0.0763, 0.8375],
         [0.9614, 0.4402],
         [0.6572, 0.2740],
         [0.9182, 0.7610],
         [0.3087, 0.1978],
         [0.8081, 0.4446],
         [0.9013, 0.7760],
         [0.8043, 0.0205],
         [0.8834, 0.0850],
         [0.7923, 0.5813],
         [0.6410, 0.2915],
         [0.4642, 0.7652],
         [0.2180, 0.7314],
         [0.2333, 0.6058],
         [0.2994, 0.9917],
         [0.8491, 0.3405],
         [0.5526, 0.4091],
         [0.6396, 0.0726],
         [0.9165, 0.8435],
         [0.0226, 0.1405],
         [0.7573, 0.7883],
         [0.4958, 0.6847],
         [0.9437, 0.5094],
         [0.8002, 0.6416],
         [0.4859, 0.1555],
         [0.5703, 0.5810],
         [0.5865, 0.9760],
         [0.9822, 0.5580]],

        [[0.7914, 0.3765],
         [0.6868, 0.5623],
         [0.3515, 0.1354],
         [0.5600, 0.5677],
         [0.3014, 0.0655],
         [0.7379, 0.4417],
         [0.7842, 0.0946],
         [0.2980, 0.7563],
         [0.1225, 0.8573],
         [0.7868, 0.6197],
         [0.8659, 0.2983],
         [0.5528, 0.9928],
         [0.8033, 0.7598],
         [0.1729, 0.8954],
         [0.7224, 0.5035],
         [0.6944, 0.3334],
         [0.3059, 0.7594],
         [0.2582, 0.3622],
         [0.8671, 0.5106],
         [0.4521, 0.5912],
         [0.9938, 0.5536],
         [0.0714, 0.4062],
         [0.4237, 0.1009],
         [0.4834, 0.4821],
         [0.1278, 0.2209],
         [0.3593, 0.0312],
         [0.1949, 0.7679],
         [0.4718, 0.3537],
         [0.1887, 0.7577],
         [0.4052, 0.0837],
         [0.1275, 0.1403],
         [0.0478, 0.2644],
         [0.2464, 0.4428],
         [0.0269, 0.7247],
         [0.8381, 0.1128],
         [0.0027, 0.1949],
         [0.9686, 0.2516],
         [0.7630, 0.7321],
         [0.1705, 0.2484],
         [0.6002, 0.3921],
         [0.6410, 0.1996],
         [0.5708, 0.8724],
         [0.3344, 0.8986],
         [0.8801, 0.9749],
         [0.6641, 0.0893],
         [0.6771, 0.4118],
         [0.7195, 0.5741],
         [0.4429, 0.5441],
         [0.4489, 0.1249],
         [0.4466, 0.9876],
         [0.8235, 0.0455],
         [0.3740, 0.5552],
         [0.7245, 0.8336],
         [0.5024, 0.7632],
         [0.6510, 0.7443],
         [0.3299, 0.7344],
         [0.3555, 0.1108],
         [0.7769, 0.6925],
         [0.2839, 0.9232],
         [0.3693, 0.6089],
         [0.0968, 0.5938],
         [0.8412, 0.4310],
         [0.3753, 0.3891],
         [0.9828, 0.2977],
         [0.3885, 0.6554],
         [0.7634, 0.9861],
         [0.2729, 0.9952],
         [0.8761, 0.5300]],

        [[0.1824, 0.8531],
         [0.2027, 0.1475],
         [0.4399, 0.5023],
         [0.7481, 0.7407],
         [0.7549, 0.0501],
         [0.6636, 0.7249],
         [0.7303, 0.0572],
         [0.2618, 0.8307],
         [0.4022, 0.1072],
         [0.4213, 0.9147],
         [0.5470, 0.0261],
         [0.5899, 0.3837],
         [0.4098, 0.0882],
         [0.6198, 0.4659],
         [0.0216, 0.5400],
         [0.1323, 0.1031],
         [0.3831, 0.4222],
         [0.7965, 0.9341],
         [0.0986, 0.5110],
         [0.0506, 0.6951],
         [0.3115, 0.9560],
         [0.4765, 0.4561],
         [0.4354, 0.5741],
         [0.4101, 0.9059],
         [0.0081, 0.4320],
         [0.8282, 0.4163],
         [0.8841, 0.1332],
         [0.6455, 0.9650],
         [0.7182, 0.6279],
         [0.0599, 0.6260],
         [0.8060, 0.0365],
         [0.2494, 0.9081],
         [0.5096, 0.3738],
         [0.3092, 0.9820],
         [0.2373, 0.1400],
         [0.4945, 0.6910],
         [0.9188, 0.5573],
         [0.1178, 0.6446],
         [0.9373, 0.9719],
         [0.2565, 0.7035],
         [0.6569, 0.9963],
         [0.3059, 0.8872],
         [0.9186, 0.6045],
         [0.8064, 0.7287],
         [0.7457, 0.5936],
         [0.6889, 0.5423],
         [0.0864, 0.1654],
         [0.1942, 0.2462],
         [0.4959, 0.4175],
         [0.4665, 0.3627],
         [0.0232, 0.4757],
         [0.0992, 0.5172],
         [0.7511, 0.0753],
         [0.3088, 0.0667],
         [0.6174, 0.1301],
         [0.0214, 0.8949],
         [0.0528, 0.4993],
         [0.9309, 0.1358],
         [0.1057, 0.9462],
         [0.4474, 0.6677],
         [0.4097, 0.7110],
         [0.4497, 0.9725],
         [0.5446, 0.7856],
         [0.6448, 0.9388],
         [0.1883, 0.7880],
         [0.2093, 0.5846],
         [0.4540, 0.8537],
         [0.5310, 0.5235]]])
    preds=tensor([[[1.6737e-01, 6.6037e-01],
         [7.9939e-01, 4.5272e-01],
         [5.7032e-01, 1.6177e-01],
         [2.8074e-01, 2.9683e-01],
         [8.6498e-01, 2.4660e-01],
         [6.3552e-01, 8.8866e-01],
         [3.0755e-01, 4.6117e-01],
         [8.3273e-01, 4.8250e-01],
         [1.9359e-01, 4.7545e-02],
         [8.3007e-01, 7.2972e-01],
         [3.2787e-01, 9.6819e-01],
         [1.1606e-01, 6.9773e-01],
         [7.8190e-01, 3.7584e-01],
         [3.0790e-01, 7.3585e-01],
         [9.7632e-01, 7.9882e-01],
         [6.2084e-01, 3.2528e-01],
         [1.5099e-01, 2.7184e-01],
         [7.7818e-01, 1.1891e-01],
         [5.4724e-01, 7.7339e-01],
         [5.1700e-01, 4.2891e-01],
         [3.0237e-01, 6.2823e-01],
         [8.2459e-01, 7.4541e-01],
         [4.7071e-01, 4.9487e-02],
         [3.8408e-01, 4.6107e-01],
         [6.0307e-02, 2.4962e-01],
         [4.2850e-01, 2.1690e-01],
         [9.7312e-01, 3.6504e-01],
         [7.7723e-01, 9.7555e-01],
         [1.3679e-01, 8.3098e-01],
         [7.5268e-01, 5.8473e-01],
         [5.0055e-01, 1.9739e-01],
         [4.4293e-01, 1.5049e-01],
         [6.8194e-03, 4.8161e-01],
         [2.4493e-02, 9.8621e-01],
         [5.3572e-01, 8.8590e-01],
         [8.8693e-01, 9.7871e-02],
         [7.6294e-01, 6.5005e-01],
         [3.4087e-01, 1.0817e-02],
         [4.3132e-02, 2.8711e-01],
         [5.7143e-01, 2.4636e-01],
         [1.3430e-01, 1.2789e-02],
         [9.0775e-01, 2.2933e-01],
         [6.4299e-01, 6.9551e-01],
         [2.5724e-01, 2.0720e-01],
         [9.1362e-01, 3.7165e-01],
         [4.6603e-01, 1.2041e-01],
         [3.7737e-01, 7.2735e-02],
         [4.3807e-01, 7.8318e-01],
         [4.0861e-01, 1.5075e-01],
         [1.6734e-01, 5.3276e-01],
         [2.4117e-01, 4.4331e-01],
         [2.2098e-01, 9.9975e-01],
         [8.4171e-01, 7.7849e-01],
         [9.3413e-02, 9.7479e-01],
         [5.7328e-01, 8.2639e-01],
         [8.8278e-01, 9.8935e-01],
         [2.3934e-01, 4.2940e-01],
         [5.9031e-01, 7.7582e-02],
         [9.0466e-01, 2.6834e-01],
         [6.3510e-01, 5.4088e-01],
         [9.1520e-02, 1.3464e-01],
         [8.4427e-01, 9.4671e-01],
         [4.5177e-01, 6.0090e-01],
         [5.3650e-02, 6.1681e-01],
         [9.3118e-01, 7.6041e-01],
         [3.2487e-01, 1.9094e-01],
         [5.1036e-01, 2.7835e-02],
         [2.8808e-01, 4.5482e-01]],

        [[8.6936e-01, 2.4133e-01],
         [8.4564e-02, 9.0522e-01],
         [9.9840e-03, 3.0229e-02],
         [7.5804e-01, 2.9006e-01],
         [8.1981e-01, 9.7538e-01],
         [1.3594e-01, 8.2281e-01],
         [4.1612e-01, 9.4840e-01],
         [4.3645e-01, 8.1956e-02],
         [7.2758e-01, 6.0104e-01],
         [9.6839e-01, 9.0493e-01],
         [1.9829e-01, 3.5381e-02],
         [9.9525e-01, 8.4257e-01],
         [3.7535e-01, 4.7969e-01],
         [5.7187e-01, 3.1030e-01],
         [1.8465e-01, 7.3673e-01],
         [1.5648e-01, 3.8927e-01],
         [4.9686e-01, 9.1677e-01],
         [2.3237e-01, 4.0412e-01],
         [1.7510e-02, 9.1364e-01],
         [7.1109e-01, 6.0403e-01],
         [3.0860e-01, 3.8064e-02],
         [9.5072e-01, 4.3245e-01],
         [5.1817e-01, 1.9804e-01],
         [9.0122e-01, 8.3430e-01],
         [1.7912e-01, 9.4140e-01],
         [9.0455e-01, 2.4028e-01],
         [9.8313e-01, 8.8758e-01],
         [9.4615e-01, 9.4350e-01],
         [3.3234e-01, 7.9818e-01],
         [1.8338e-01, 1.3215e-01],
         [7.1844e-01, 6.1940e-03],
         [4.4937e-01, 6.0576e-01],
         [4.5728e-01, 6.8310e-01],
         [7.4654e-01, 8.5070e-02],
         [1.5587e-01, 5.5968e-01],
         [9.6617e-01, 9.0119e-02],
         [8.8769e-01, 4.4089e-01],
         [1.1011e-01, 3.1632e-01],
         [3.2699e-01, 4.7225e-01],
         [9.6189e-01, 7.5850e-01],
         [3.0250e-01, 5.3835e-01],
         [5.1601e-01, 6.4118e-01],
         [1.9893e-01, 2.7643e-01],
         [2.3270e-01, 6.1181e-01],
         [1.9994e-01, 5.9325e-02],
         [3.8410e-01, 7.5580e-01],
         [3.2420e-01, 4.6458e-01],
         [6.1224e-01, 4.9877e-01],
         [4.7241e-01, 2.4364e-02],
         [5.3575e-01, 2.3308e-01],
         [5.7020e-01, 2.7048e-01],
         [2.5325e-01, 2.7246e-01],
         [6.7946e-01, 9.8201e-01],
         [3.7509e-01, 1.8990e-01],
         [3.5532e-01, 4.7859e-01],
         [1.8006e-01, 2.7178e-01],
         [7.4431e-02, 2.2458e-01],
         [4.3009e-01, 7.1046e-01],
         [6.1496e-01, 5.5459e-01],
         [2.7070e-01, 7.2406e-01],
         [9.1974e-01, 5.5902e-01],
         [5.3739e-01, 2.8183e-01],
         [8.9366e-01, 9.5207e-01],
         [9.8890e-01, 2.3137e-01],
         [1.6824e-01, 5.6736e-01],
         [3.4185e-01, 2.7859e-01],
         [2.9109e-01, 5.2046e-01],
         [7.0895e-01, 7.3242e-01]],

        [[9.4637e-01, 2.6713e-01],
         [2.9530e-01, 7.3130e-01],
         [4.7909e-01, 5.1242e-01],
         [7.2562e-01, 5.8148e-01],
         [6.9728e-01, 2.7030e-01],
         [4.9304e-01, 8.6147e-03],
         [5.7428e-01, 2.4208e-01],
         [9.0459e-01, 3.6898e-01],
         [5.0103e-01, 6.0337e-01],
         [4.4989e-01, 3.1581e-01],
         [2.6088e-01, 4.4147e-01],
         [5.3600e-01, 3.2915e-01],
         [1.1429e-01, 7.5556e-01],
         [5.4990e-01, 3.3010e-02],
         [7.2938e-01, 6.3417e-01],
         [7.7678e-01, 4.1042e-01],
         [5.6919e-01, 8.9258e-01],
         [1.0064e-01, 1.3062e-01],
         [8.6986e-01, 6.0035e-01],
         [2.2922e-01, 4.3556e-02],
         [1.3278e-01, 5.9282e-01],
         [1.3246e-01, 8.0027e-01],
         [3.6385e-01, 4.2743e-01],
         [2.4621e-01, 3.3971e-01],
         [7.5359e-01, 8.4487e-01],
         [7.2278e-01, 2.1859e-01],
         [3.8357e-01, 4.4144e-02],
         [8.9992e-01, 1.4305e-01],
         [1.2789e-01, 4.9351e-01],
         [3.2840e-01, 9.5564e-04],
         [3.8158e-01, 2.2411e-05],
         [7.1295e-01, 1.0248e-01],
         [3.8013e-01, 8.0077e-01],
         [2.8726e-01, 6.6043e-01],
         [6.2999e-01, 3.7838e-02],
         [8.0845e-01, 7.8092e-01],
         [3.8300e-01, 4.5196e-02],
         [4.8163e-01, 4.1805e-01],
         [6.6318e-01, 7.0847e-01],
         [6.0076e-01, 4.7540e-02],
         [6.4335e-01, 8.0892e-01],
         [1.4887e-01, 2.1084e-01],
         [5.1931e-01, 1.1413e-01],
         [3.0160e-01, 9.8615e-01],
         [2.5472e-01, 1.9575e-01],
         [3.9540e-01, 1.6314e-01],
         [9.4383e-01, 8.9881e-01],
         [6.1999e-02, 2.3478e-01],
         [9.2862e-01, 6.7135e-01],
         [3.9495e-01, 3.5517e-01],
         [5.5469e-01, 5.4770e-01],
         [3.5175e-01, 2.1766e-01],
         [2.1590e-01, 8.9396e-01],
         [7.0576e-01, 2.8207e-01],
         [5.2249e-01, 7.0435e-02],
         [6.5805e-01, 8.1069e-01],
         [8.3019e-01, 9.9059e-01],
         [2.0836e-01, 4.4572e-01],
         [7.0474e-01, 2.7901e-01],
         [1.8209e-01, 3.6434e-01],
         [4.1994e-01, 4.6291e-01],
         [3.0390e-01, 9.8653e-01],
         [6.1660e-01, 7.8405e-01],
         [1.6956e-01, 7.0767e-01],
         [4.1993e-01, 6.8103e-02],
         [8.5310e-01, 6.8209e-01],
         [1.5904e-01, 6.1956e-01],
         [9.3775e-01, 6.7911e-01]]])
    print("{:.10f}".format(metric(preds, target)))
    target = torch.rand(64,68,2)
    preds = torch.rand(64,68,2)
    print("{:.10f}".format(metric(preds, target)))