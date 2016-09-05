from pathlib import Path
import numpy as np
import pandas as pd

def interpolate_annotations(annotation_paths, target_path):
    """Loads the annotations and interpolate them
    
    Parameters
    ----------
    annotation_paths : pathlib.Path list
        list of paths to csv files containing one column for the time and a second one 
        for the corresponding annotations
    target_path : pathlib.Path, optional
        if provided, the resulting DataFrame is save as a csv file in that path
        
    Returns
    -------
    pd.DataFrame : 
        a data frame with as many columns as annotators + 1
        (the first column contains the times)
        
        The times range from the minimum of all annotated times to the maximum
    """
    data = []
    column_names = ['time']
    for annotation_path in annotation_paths:
        # 1) read the data into a matrix
        # the matrix is of shape (n_times, 2), with 
        # the first columns being times and the second the corresponding annotations
        annotator = annotation_path.stem.split('_')[-1]
        pd_data = pd.read_csv(annotation_path.as_posix())
        data.append(pd_data.as_matrix())
        
        # add corresponding dtype: the column will have the name of the annotator + original name
        column_names.append(pd_data.columns[1] + '_' + annotator)
    
    # Next, before we interpolate, we need the first time recorded and the last time recorded
    xmin = min([np.min(d[:, 0]) for d in data])
    xmax = max([np.max(d[:, 0]) for d in data])
    
    # interpolate all annotations
    n_annotators = len(data)
    interpolated_times = np.arange(xmin, xmax, 0.01)
    interpolated = np.zeros((len(interpolated_times), n_annotators+1))
    interpolated[:, 0] = interpolated_times
    for i in range(n_annotators):
        times = data[i][:, 0]
        values = data[i][:, 1]
        interpolated_values = np.interp(interpolated_times, times, values)
        # first column is times!
        interpolated[:, i+1] = interpolated_values
    
    # convert into a pandas data frame
    result = pd.DataFrame(interpolated, columns=column_names)
    if target_path:
        result.to_csv(target_path.as_posix())
        
    return result
