# Scientific Publications
This project synchronises metadata data about scientificic publications from the (Arxiv)[https://arxiv.org/] site.

## Articles Categories
Metadata synchronization is only happens for the articles that fall in the following categories:
- Psychiatry
- Therapy
- Data Science
- Machine Learning

# Synchronization approahces
The project employs two sychronization approaches:
 - ## Initial synchronization
    - This happens when the application is setup for the first time
    - It fetches six months worth of metadata
    - It can be kick started by running the command: `python manage.py initial_sync`

- ## Incremental synchronization
    - This happnes on daily basis via a background task
    - To start the background worker that does the daily sync, run the command `todo`
