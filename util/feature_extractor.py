import skimage.feature as skimg
import numpy as np
from sklearn.metrics.cluster import entropy
import warnings


def get_feature(comatrix, mode):
    return skimg.greycoprops(comatrix, mode)


class Features:
    def __init__(self, source_id):
        self.source_id = source_id
        self.max_coord = 0
        self.features = dict()

    def __str__(self):
        string = 'Features for ' + self.source_id

        for key, value in self.features.iteritems():
            string += '\n  ' + key + ' = ' + str(value)

        return string


def get_features(lidc_data):
    features = []

    for nodule in lidc_data:
        nodule_feature = Features(nodule.source_id)

        nodule_feature.max_coord = np.max(nodule.pixels)

        with warnings.catch_warnings():
            warnings.simplefilter("ignore")
            grey_comatrix = skimg.greycomatrix(nodule.pixels, [1], [0, np.pi / 4, np.pi / 2, 3 * np.pi / 4],
                                               nodule_feature.max_coord + 1)

        nodule_feature.features['contrast'] = skimg.greycoprops(grey_comatrix, 'contrast').flatten().astype(float)
        nodule_feature.features['dissimilarity'] = skimg.greycoprops(grey_comatrix, 'dissimilarity').flatten().astype(
            float)
        nodule_feature.features['homogeneity'] = skimg.greycoprops(grey_comatrix, 'homogeneity').flatten()
        nodule_feature.features['energy'] = skimg.greycoprops(grey_comatrix, 'energy').flatten()
        nodule_feature.features['correlation'] = skimg.greycoprops(grey_comatrix, 'correlation').flatten()
        nodule_feature.features['ASM'] = skimg.greycoprops(grey_comatrix, 'ASM').flatten().astype(float)
        nodule_feature.features['entropy'] = entropy(nodule.pixels)

        features.append(nodule_feature)

    return features


def features_to_matrix(fs):
    features_matrix = []

    for feature in fs:
        for value in feature.features.values():
            features_matrix = np.append(features_matrix, value)

    return features_matrix.reshape((len(fs), -1))