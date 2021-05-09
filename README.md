# Activity Recommender: A simple python machine learning REST service

## Goal

- In this pet project, I want to implement a activity recommender as a REST service.

- The goal is to learn and to get familar with the technology stacks for building a machine learning REST service, and not about the machine learning algorihtm itself.

## Description

- User can provide his/her gender, and the service will return a recommended activity, e.g., basketball, for the user. The recommendation wil be based on the conditional probability of each activity for that gender.

- User can update the activity database, that is, the number of male players and female players for each activity.

## API Documentation

- [openapi.json](openapi.json)

  - If you prefer GUI, you have two options.
  
    - First, you can copy-paste [openapi.json](openapi.json) to any  online swagger visulation tool (for example, [swagger editor](https://editor.swagger.io/)).

    - Second, you can build the serice locally, and look at the API documentation locally.

        ```bash
        # Assuming you have already clone the project locally

        # Build the service docker image
        make build

        # Run the service using docker
        make run

        # Then, you can go to 
        #             http://localhost/docs 
        # to see the API documentations.
        # Furthermore, you can test the API endpoints directly on it.
        # However, it is for lightweight exploration and should not be used for API testing. 
        # I would recommend using proper http client (e.g., Postman) for API testing.

        # Shutdown the service
        make stop
        ```

## Cost Estimation

- Total monthly cost: $40.25

- RDS

  - Monthly cost: 14.71 USD

  - Details

    - Instance type: db.t2.micro

    - Storage amount: 20 GB

    - Single AZ

    - On Demand

- ECS Service (Fargate)
  
  - Monthly cost: 8.88 USD

  - Details

    - Number of task: 1

    - 0.25 vCPU + 0.5 GB

- Application Load Balancer (ALB)

  - Monthly cost: 16.66 USD

  - Details

    - Number of ALB: 1

    - Fixed hourly charge per ALB: $0.0225 per hour

## Useful Resrouces

- [FastAPI](https://fastapi.tiangolo.com/)
