from sklearn.utils import class_weight
import numpy as np


labels = train_data.classes  

class_weights = class_weight.compute_class_weight(class_weight='balanced',
                                                  classes=np.unique(labels),
                                                  y=labels)


class_weights_dict = dict(enumerate(class_weights))
print("Class Weights:", class_weights_dict)
