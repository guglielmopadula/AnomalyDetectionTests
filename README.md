A short example of outlier detection on triangular mesh.

|Model                             |AUC Train|AUC Test|
|----------------------------------|---------|--------|
|InfinityNormRatio+EllipticFeatures|0.999    |0.9     |
|InfinityNormRatio+IsolationForest |0.999    |0.9     |
|InfinityNormRatio+SVM             |0.489    |0.49    |
|Ratio+SVM                         |0.49     |0.49    | 
|Ratio+IsolationForest             |0.489    |0.52    | 
|Ratio+Isomap+EllipticFeatures     |0.489    |0.54    |
|SVM                               |0.541    |0.475   |
|IsolationForest                   |0.489    |0.48    |
|Isomap+EllipticFeatures           |0.489    |0.49    |



