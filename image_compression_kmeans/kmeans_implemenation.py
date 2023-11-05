import numpy as np

### Kmeans algorithm implementation
def kmeans(k, data, limit):
    
    np.random.seed(42)
    idx = np.random.choice(data.shape[0], k, replace=False)
    centers = data[idx, :] # initialize the centers
    
    labeled = None
    labels = np.arange(len(centers))
    distances = np.zeros((len(labels), len(data))) # initialize the distances
    
    for itr in range(limit):
        
        for label in labels:
            # calculate the distances
            distances[label] = np.linalg.norm(data - centers[label], axis=1)
        
        # assign the labels
        labeled = np.argmin(distances, axis=0)

        # update the centers
        for label in labels:
            di = data[np.where(labeled == label)]
            if di.any():
                centers[label] = np.mean(di, axis=0)
          
    return centers, labeled