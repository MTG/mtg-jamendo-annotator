from flask import Flask, render_template, request
import json


app = Flask(__name__, static_url_path='/static')

# Sets the number of audio track per page. 
# You should not change that after having started annotating!
NUM_SOUNDS_PER_PAGE = 5

# Enter here the path to the file containing the path of the sound track you have to annotate.
# e.g. 'static/track_paths.json'
PATH_TO_FILE_WITH_SOUND_IDS = 'static/example_track_paths.json'


@app.route('/', methods = ['GET', 'POST'])
def annotator():
    if request.method == 'POST':
        # save annotations to json file
        data = request.get_json()
        print(data)
        # TODO: save data in on json per audio track
        # json.dump(data['answers'], open('annotations/page-{}.json'.format(data['page']), 'w'))
        return json.dumps({'success':True}), 200, {'ContentType':'application/json'} 

    page = int(request.args.get('p', 1))

    all_sound_tracks = json.load(open(PATH_TO_FILE_WITH_SOUND_IDS, 'rb'))

    # get a chunk of sounds according to the requested page number
    sound_tracks = all_sound_tracks[(page-1)*NUM_SOUNDS_PER_PAGE:page*NUM_SOUNDS_PER_PAGE]

    return render_template("index.html", sound_tracks=sound_tracks, page=page)


if __name__ == '__main__':
    app.run(debug=True)
