I decided to use fast api for the api with celery as a standard approach for distributed tasks.
celery is configured to use rabbitMQ as a message broker and redis as a result store.

job is split into multiple celery tasks.
celery tasks are queued and linked after the creation of the task in db.
celery tasks are independent from api server.
I did implement callback_url
i did not implement restarting of tasks in case of network errors, but it should be easy to do using celery build-in mechanisms.




I also use redis as a database for the api. 

app is set up and ready to use. all you have to do is :
```docker compose up```
or ```docker-compose up```
deppending on your version of docker.

than go to :
```http://localhost:8080/docs```


I also added echo server on http://echoserver so it can be used to test callback_url
also you can check dask tasks in this tool: ```http://localhost:5555/tasks```

I added vscode configuration, so you can connect anytime with debugger from vscode.
also, I added configuration for development in remote containers. 


I created one integration test, to run it :
```./CI.sh```