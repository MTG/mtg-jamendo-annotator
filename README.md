# The MTG-Jamendo-Annotator

## Installation with Docker

Install [Docker desktop](https://docs.docker.com/install/) (Mac, Windows) or Docker server and Docker-compose (Linux)

### Configuration

The application is configured by editing the `docker-compose.yml` file.

In the section `environment`, set `CHUNK_NUMBER` to the chunk that you are editing

    environment:
      - SOUNDS_PER_PAGE=10
      - ANNOTATION_TASKS=mood,miscellaneous
      - CHUNK_NUMBER=5
      
In the section `volumes`, add the full path to the location of your audio 

    volumes:
      - .:/app
      - <path to your audio here>:/app/static/tracks


### Startup

Run

    docker-compose up
    
and go to http://localhost:5000


## Manual installation

If you prefer to not use Docker, you can set up the application manually

### MAC OS and Linux

#### Install dependencies

    virtualenv venv
    source venv/bin/activate
    pip install -r requirements.txt


#### Configure

Export environment variables for settings:

    export SOUNDS_PER_PAGE=10
    export ANNOTATION_TASKS=mood,miscellaneous
    export CHUNK_NUMBER=5

Copy your audio files to `static/tracks/`

#### Start server
Run 

    flask run

and go to: http://localhost:5000/

Choose a task and start annotating!

### Windows

#### Install Anaconda and dependencies

Install Anaconda, following the instructions in [here](https://docs.anaconda.com/anaconda/install/windows/)

Open Anaconda prompt and run:

    conda create --name mtg-jamendo
    conda activate mtg-jamendo
    conda install flask


#### Configure

Export environment variables for settings:

    SET SOUNDS_PER_PAGE=10
    SET ANNOTATION_TASKS=mood,miscellaneous
    SET CHUNK_NUMBER=5

Copy your audio files to `static/tracks/`

#### Start server
Run 

    flask run

and go to: http://localhost:5000/

Choose a task and start annotating!

## License
This application has been made available under the Apache-2.0 license.
See the LICENSE file for more information
