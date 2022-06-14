# Full-stack challenge

Hi! It's nice to see you here and all the best luck solving the challenge!
It based on simplified version of one of the day-to-day tasks we encounter

To make the coding more pleasant for you, we've taken care of basic app bootstrap, please see `docker-compose.yaml` for details.
Feel free to use different setup, add additional packages, libraries, images as you wish.

We're interested in a clean solution for the problems described in the requirements list. Besides that, we'd be looking at your whole approach to applications development: performance, code & file structure, architecture & API design, etc.

The task is supposed to take around 8 hours to complete. Do not hesitate to prioritize functionality and/or adjust the complexity of your solution. We expect you to cover all the requirements.

Please publish your solution as a github repository and send us a link.

## Running the app
In order to start the example application please use `docker-compose up` and visit http://localhost:8000 in your browser.

As we like Docker and simplicity, it would be great if your solution could be started with the same `docker-compose up`.

However, if you chose not to use Docker or running your app requires extra steps like running scripts, installing extra dependencies etc. please make sure to include clear instructions and requirements. **Please keep it as simple as possible.**

## App requirements

We would like you to create a simple application that would allow the users to upload, enrich and preview `.csv` files. 
The requirements are kept simple but please feel free to extend them and show us your skill as you please. 
You are given a freedom in structuring the UI and the number of views you develop - we love creativity!

---
### Requirement #1

*As a user I need to upload `.csv` file and be able to preview its content in a table*

Please use `users_posts_audience.csv` file for testing, it contains users' posts views data

### Requirement #2

*As a user I would like to see the list of all files I've uploaded, so I can choose the file I want to preview*

### Requirement #3

*As a user I would like to enrich my data file with additional details fetched from API endpoint*

- User should be able to input API endpoint for fetching external data, you can use following endpoints for testing:
https://jsonplaceholder.typicode.com/posts/, https://jsonplaceholder.typicode.com/users/
- User should be able to select key column name from data file that would be used for joining data, by default first column should be pre-selected
- User should be able to input key name for API response that would be used for the other side of join
- Based on selected keys, enriching should add all keys from the API response for each matching row as new columns  
- Enriching existing file should create a new file accessible in the listing from **Requirement #2**, original file should not be modified

## Extra hints
- We've prepared a basic setup including Django, Celery, Postgres and Redis but feel free to use different stack that you are more familiar with
- We encourage you to use a frontend framework of your choice, i.e. React, Vue
- How to start new React app: https://reactjs.org/docs/create-a-new-react-app.html
- How to start new Vue app: https://cli.vuejs.org/guide/creating-a-project.html#vue-create