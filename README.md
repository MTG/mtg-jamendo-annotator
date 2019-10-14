# The MTG-Jamendo-Annotator

## Install dependencies
```shell
virtualenv venv
source venv/bin/activate
pip install -r requirements.txt
```

## Configure
Open `app.py` and set the `PATH_TO_FILE_WITH_SOUND_IDS` variable to the path of the json file containing a list of track filenames you have to annotate.
e.g.: `PATH_TO_FILE_WITH_SOUND_IDS = 'static/jamendo_split_0_test_stratified_subset_0.json'`

Copy your audio files in `static/tracks/`

## Start server
`python app.py`

## Annotate
With your browser go to:
`http://localhost:5000/`

Choose a task and start annotating!
