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
    - It fetches six months worth of metadata by default
    - Initiating the initial data sync:
        - To see topic/categories from which you sync the data, run the command: `python manage.py initial_articles_sync -h`
        - To initiate the data sync, run the command: `python manage.py initial_articles_sync --months 1 --topics 1,2 `
        - If `--months` option is not specified, we willd default to synci'ng for 6 months

- ## Incremental synchronization
    - This happnes on daily basis via a background task
    - To start the background worker that does the daily sync, run the command `todo`
