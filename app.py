# Copyright 2020 Music Technology Group, Universitat Pompeu Fabra
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

from flask import Flask, render_template, request, abort, redirect, url_for
import json
import os


app = Flask(__name__, static_url_path='/static')


# The number of audio track per page.
# You should not change this after having started annotating!
CONFIG_SOUNDS_PER_PAGE = os.getenv('SOUNDS_PER_PAGE', '5')
CONFIG_CHUNK = os.getenv('CHUNK_NUMBER')
CONFIG_ANNOTATION_TASKS = os.getenv('ANNOTATION_TASKS', 'mood,miscellaneous,mood-miscellaneous,all')

# The location that annotations are written to
ANNOTATION_FOLDER = 'annotations'

# There are three different annotation tasks
VALID_ANNOTATION_TASKS = {
    'genre',
    'mood',
    'miscellaneous',
    'mood-miscellaneous',
    'all',
}


# Enter here the path to the file containing the path of the sound track you have to annotate.
# e.g. 'static/track_paths.json'
PATH_TO_FILE_WITH_SOUND_IDS = 'static/stratified_test_elements_fold_{}.json'.format(CONFIG_CHUNK)
if not os.path.exists(PATH_TO_FILE_WITH_SOUND_IDS):
    raise ValueError("No such data file with chunk {}".format(CONFIG_CHUNK))


FOLDER_WITH_AUDIO_FILES = 'static/tracks/'


ANNOTATION_TASKS = []
for ann_task in CONFIG_ANNOTATION_TASKS.split(","):
    if ann_task not in VALID_ANNOTATION_TASKS:
        raise ValueError("{} is not a valid annotation task".format(ann_task))
    ANNOTATION_TASKS.append(ann_task)

try:
    NUM_SOUNDS_PER_PAGE = int(CONFIG_SOUNDS_PER_PAGE)
except ValueError:
    raise ValueError("{} is not a valid number of sounds per page".format(CONFIG_SOUNDS_PER_PAGE))


def find_missing_integer(lst):
    """Returns the first missing integer in an ordered list.
    If not found, returns the next integer.
    """
    try:
        return sorted(set(range(lst[0], lst[-1])) - set(lst))[0]
    except:
        return max(lst) + 1



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
        page = data['page']
        for track_name, answers in data['answers'].items():
            track_name_without_folder = track_name.replace('/', '_')

            annotation_file = '{}-page-{}-{}.json'.format(annotation_task, page, track_name_without_folder)
            with open(os.path.join(ANNOTATION_FOLDER, annotation_file), 'w') as fp:
                json.dump(answers, fp)
        return json.dumps({'success': True}), 200, {'ContentType': 'application/json'}

    page = request.args.get('p', None)
    page_already_annotated = False

    # check completion
    annotation_files = [file for file in os.listdir('annotations') if file.endswith('.json')]
    annotated_pages_set = set([int(annotation_file.split('-')[-2]) for annotation_file in annotation_files if annotation_file.startswith(annotation_task)])
    annotated_pages = sorted(list(annotated_pages_set))

    # set page automatically according to their completion
    if not page:
        if annotated_pages:
            redirect_page = find_missing_integer(annotated_pages)
        else:
            redirect_page = 1
        return redirect(url_for('annotator', annotation_task=annotation_task, p=redirect_page))

    else:
        # check if page was already annotated
        page = int(page)
        if page in annotated_pages_set:
            page_already_annotated = True

    all_sound_tracks = json.load(open(PATH_TO_FILE_WITH_SOUND_IDS, 'rb'))

    # get a chunk of sound tracks according to the requested page number
    sound_tracks = all_sound_tracks[(page-1)*NUM_SOUNDS_PER_PAGE:page*NUM_SOUNDS_PER_PAGE]

    # Load annotations for any sounds already annotated on this page
    page_annotations = {}
    for tr in sound_tracks:
        track_name_without_folder = tr.replace('/', '_')
        annotation_file = '{}-page-{}-{}.json'.format(annotation_task, page, track_name_without_folder)
        full_filename = os.path.join(ANNOTATION_FOLDER, annotation_file)
        if os.path.exists(full_filename):
            with open(full_filename, 'r') as fp:
                data = json.load(fp)
                page_annotations[tr] = data

    return render_template("index.html",
                           folder_with_audio_files=FOLDER_WITH_AUDIO_FILES,
                           sound_tracks=sound_tracks,
                           page=page,
                           annotation_task=annotation_task,
                           page_already_annotated=page_already_annotated,
                           page_annotations=page_annotations)


if __name__ == '__main__':
    app.run(debug=True)
