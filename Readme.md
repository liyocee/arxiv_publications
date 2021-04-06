# Scientific Publications
This project synchronises metadata data about scientificic publications from the [Arxix](https://arxiv.org/) site.

## Articles Categories
Metadata synchronization will only happens for the articles that fall in the following categories:
- Psychiatry
- Therapy
- Data Science
- Machine Learning

## Initial Setup
- Ensure you have switched to the `app` dir: `cd app`
- Ensure you have redis running, you can spin one on docker: `docker run -d -p 6379:6379 redis`
- Create a python3 virtual env and activate it:
    -  `python3 -m venv .venv`
    - `source .venv/bin/activate`
    - Install project dependencies:  `pip install -r requirements.txt`

- Seed the database with initial data: `python manage.py seed` . The project uses the default sqlite database:
    - We have two seeders:
        - One for creating categories/topcis from Arxiv from this endpoint: http://export.arxiv.org/oai2?verb=ListSets
        - One for creating topic/articles classifications outlined here:  https://arxiv.org/help/api/user-manual 
- Start the server: `python manage.py runserver`

# Synchronization approahces
The project employs two sychronization approaches:
 - ## Initial synchronization
    - This happens when the application is setup for the first time
    - It fetches six months worth of metadata by default on specified topics/categories
    - Initiating the initial data sync:
        - To see topic/categories from which you can sync the data, run the command: `python manage.py initial_articles_sync -h`
        - To initiate the data sync, run the command: `python manage.py initial_articles_sync --months 1 --topics 1,2 `
        - If `--months` option is not specified, we will default to synci'ng for 6 months

- ## Incremental synchronization
    - This happnes on daily basis via a background task
    - To start the background worker that does the daily sync, run the commands:
        - Start the scheduler:  `./celery_beat.sh`
        - Start the workers:  `./celery_worker.sh`
    - Ensure to run the above commands on an activated virtual env that we've created above
    - You might want to add execute flag on the shell scripts before running them: `sudo chmod +x celery_beat.sh`


# Running unit tests
- Use the command: `pytest --cov`

# Feature Enhancements:
- Improve unit tests coverage. Righ now, only "users" app has been tested
- Add a page for logged in users to see all the articles / authors that they have favorited
- Add error handling with retriex when we are throttled by Arxiv
- Allow users to browse articles by categories/topics and sub-categories
