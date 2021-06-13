# Development

## Requirements

1. Docker Desktop
1. Python 3.8
1. Azure blob storage service  
   We plan to support SQL service in the future.

## Tools

1. Use a [LINE simulator](https://github.com/kenakamu/LINESimulator) developed by kenakamu san.

    1. Clone the repository.
    1. Build the Docker image.

        ```bash
        docker image build --tag=linesimulator .
        ```

    1. Run the container on port `8080`.

        ```bash
        docker container run -d --rm -p 8080:8080 linesimulator
        ```

### Test with the LINE simulator

Once the LINE simulator and LINE bot service are running, you can test the service by using browser to visit [http://localhost:8080/](http://localhost:8080/). Fill the field with your LINE bot info, the **Bot API Server Address** is `http://host.docker.internal/line/webhook`.

![bot config](../pics/bot_config.jpg)
