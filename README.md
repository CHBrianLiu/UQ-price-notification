# UQ-price-notification

## Use cases



## Deployment

To deploy FAST API app to Azure Web App, configure the service with the following settings

* Startup command: `gunicorn -w 4 -k uvicorn.workers.UvicornWorker app.main:app`
