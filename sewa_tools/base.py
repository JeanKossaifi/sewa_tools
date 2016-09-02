from pathlib import Path
import sys
import zipfile


def extract_from_glob(path_glob, extraction_path, mendatory=False):
    """Assumes there there are 0 or 1 results in the glob
    if 1, this is extracted, if 0 raises if mendatory, otherwise passes
    """
    try:
        path = next(path_glob)
    except StopIteration:
        if mendatory:
            raise
        else:
            return
        
    zip_ref = zipfile.ZipFile(path.as_posix(), "r")
    zip_ref.extractall(extraction_path.as_posix())



def extract_zips(sewa_path):
    """Extracts the zipfiles in each video of the SEWA data
           
           for valence, arousal, liking and LLD

    Parameters
    ----------
    sewa_path : `pathlib.Path`
        path to the SEWA data as downloaded from the database
    """
    for video_path in sewa_path.iterdir():
        # print current folder
        sys.stdout.write('\rprocessing folder {}'.format(video_path))
        sys.stdout.flush()
        
        # Ignore non directories.
        if not video_path.is_dir():
            continue

        data = dict()

        # Extract valence
        extract_from_glob(video_path.glob('*Valence.zip'), video_path.joinpath('valence'), mendatory=True)

        # Extract arousal
        extract_from_glob(video_path.glob('*Arousal.zip'), video_path.joinpath('arousal'), mendatory=True)

        # Extract landmarks
        extract_from_glob(video_path.glob('*Landmarks.zip'), video_path.joinpath('landmarks'), mendatory=True)

        # Extract LLD
        extract_from_glob(video_path.glob('*LLD.zip'), video_path.joinpath('lld'), mendatory=True)

        # Extract Liking if present
        extract_from_glob(video_path.glob('*Liking.zip'), video_path.joinpath('liking'), mendatory=False)


def read_landmarks(landmark_file):
    """Read a landmarks file from the SEWA dataset
    
    Parameters
    ----------
    landmark_file : str
        path to the file (.txt)
    
    Returns
    -------
    dict
        Keys are:
        * pitch, yaw, roll : float
        * eyes : ndarray of shape (10, 2)
        * shape : ndarray of shape (49, 2)
    """
    f = open(landmark_file, 'r')
    # Read pitch, yaw and roll
    pitch, yaw, roll =  [float(i) for i in f.readline().split()]
    
    # Read the eye coordinates
    eye_coordinates = [float(i) for i in f.readline().split()]
    eyes = []
    for i in range(0, len(eye_coordinates), 2):
        eyes.append([eye_coordinates[i], eye_coordinates[i+1]])
    eyes = np.array(eyes)
    
    # Read the 49 facial landmarks
    shape_coordinates = [float(i) for i in f.readline().split()]
    shape = []
    for i in range(0, len(shape_coordinates), 2):
        shape.append([shape_coordinates[i], shape_coordinates[i+1]])
    shape = np.array(shape)
    
    return {'pitch':pitch, 'yaw':yaw, 'roll':roll,
            'eyes':eyes, 'shape':shape}
