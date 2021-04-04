# Scientific Publications
This project synchronises metadata data about scientificic publications from the (Arxiv)[https://arxiv.org/] site.

## Articles Categories
Metadata synchronization is only happens for the articles that fall in the following categories:
- Psychiatry
- Therapy
- Data Science
- Machine Learning

## Initial Setup
- Seed the database with initial data: `python manage.py seed`

# Synchronization approahces
The project employs two sychronization approaches:
 - ## Initial synchronization
    - This happens when the application is setup for the first time
    - It fetches six months worth of metadata
    - It can be kick started by running the command: `python manage.py initial_articles_sync months_offset 3` :
        - If `months_offset` option is not provided to the command, the sync process will default to syncing 6 months worth of data

- ## Incremental synchronization
    - This happnes on daily basis via a background task
    - To start the background worker that does the daily sync, run the command `todo`
