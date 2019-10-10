from flask import Flask, render_template, request, abort
import json


app = Flask(__name__, static_url_path='/static')

# Sets the number of audio track per page. 
# You should not change that after having started annotating!
NUM_SOUNDS_PER_PAGE = 5

# Enter here the path to the file containing the path of the sound track you have to annotate.
# e.g. 'static/track_paths.json'
PATH_TO_FILE_WITH_SOUND_IDS = 'static/example_track_paths.json'

# There are three different annotation tasks
ANNOTATION_TASKS = [
    'genre',
    'mood',
    'miscellaneous'
]


@app.route('/')
def home():
    return render_template("home.html", annotation_tasks=ANNOTATION_TASKS)


@app.route('/<annotation_task>', methods = ['GET', 'POST'])
def annotator(annotation_task):
    if annotation_task not in ANNOTATION_TASKS:
        abort(404)

    if request.method == 'POST':
        # save annotations to json file
        data = request.get_json()
        print(data)
        # TODO: save data in on json per audio track and per annotation task
        # json.dump(data['answers'], open('annotations/page-{}.json'.format(data['page']), 'w'))
        return json.dumps({'success':True}), 200, {'ContentType':'application/json'} 

    page = int(request.args.get('p', 1))

    all_sound_tracks = json.load(open(PATH_TO_FILE_WITH_SOUND_IDS, 'rb'))

    # get a chunk of sound tracks according to the requested page number
    sound_tracks = all_sound_tracks[(page-1)*NUM_SOUNDS_PER_PAGE:page*NUM_SOUNDS_PER_PAGE]

    return render_template("index.html", sound_tracks=sound_tracks, page=page, annotation_task=annotation_task)


if __name__ == '__main__':
    app.run(debug=True)