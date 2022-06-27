for task description, click [HERE](./Tech_lead__take-home_assignment_1_.pdf)

I decided to use fast api for the api with celery as a standard approach for distributed tasks.
celery is configured to use rabbitMQ as a message broker and redis as a result store.

job is split into multiple celery tasks.
celery tasks are queued and linked after the creation of the task in db.
celery tasks are independent from api server.
I did implement callback_url
I did not implement restarting of tasks in case of network errors, but it should be easy to do using celery build-in mechanisms.

Few choices that I had to make, mostly to save some time:
- if anything fails, the whole job fails. But job status should be updated and if webhook was provided, it should be called with updated status
- Use of redis as the main database - it is ok for this POC, but if I would design a real application, I would probably use postgress. 
- Celery - I'm not a big fan and would change it for anything else compatible with asyncio, but it is the most common way to implement the distributed tasks, so I decided to use it.
- I would love to use airflow for the whole task, but It wouldn't show what I want to show in this task.




I also use redis as a database for the api. 

app is set up and ready to use. all you have to do is :
```docker compose build```
and
```docker compose up```
or ```docker-compose up```
deppending on your version of docker.

than go to :
```http://localhost:8080/docs```


I also added echo server on http://echoserver so it can be used to test callback_url

also you can check dask tasks in this tool: ```http://localhost:5555/tasks```

I added vscode configuration, so you can connect anytime with debugger from vscode.
also, I added configuration for development in remote containers. 
configuration for linters , etc (black, flake8 and pyright) is also there.

I did my best to make my code typed, and this is a really important part for me.

I created one integration test, to run it :
```./CI.sh```
