# Dockerized Flask Starter App with TOTP Two-Factor Authentication

This repository is the result of my long search for a simple but versatile route from Python code to a presentable HTTPS web app that lives on a custom domain.

## Main Features

- [Demo App](https://flask.albond.xyz) - (disabled due to $$$) - a Flask app with two-factor auth and sample protected content, based on Miguel Grinberg's [blueprint](https://blog.miguelgrinberg.com/post/two-factor-authentication-with-flask)
- The whole thing is in a Docker container, extensible to multi-container apps with Docker Compose
- Direct [deployment to AWS Elastic Container Service using Docker tools](https://aws.amazon.com/about-aws/whats-new/2020/07/docker-and-aws-collaborate-to-help-deploy-applications-to-amazon-ecs-on-aws-fargate/)


## Two-Factor Auth

![image](https://user-images.githubusercontent.com/47034358/91606445-4d6dd600-e92f-11ea-885b-831f03ea1836.png)

The web app has a private section for authenticated users.  I work in biotech and healthcare sectors, where two-factor authentication is a common requirement.  Here you have what's in my view is the least annoying flavor of 2FA: TOTP tokens.  To register, you scan a QR code with a free app like Google Authenticator.  The app generates tokens that expire every 30 seconds.

![image](https://user-images.githubusercontent.com/47034358/91606735-ddac1b00-e92f-11ea-815c-b48f66a49225.png)

Here are the main features:



*Note*: At the time of writing (September 2020), standard Docker Desktop did not have the `docker ecs` feature and [Docker Desktop Edge (2.3.3.0)](https://www.docker.com/blog/from-docker-straight-to-aws/) was required.  You can use regular edition now: https://docs.docker.com/engine/context/ecs-integration/

## Development in a local Docker container

0. Set up [Docker Desktop](https://www.docker.com/products/docker-desktop) (choose Edge edition if you need AWS ECS integration)
1. Clone: `git clone https://github.com/liquidcarbon/dockerflask2fa.git && cd dockerflask2fa`
2. Build and start the application: `docker-compose up`
3. Go to `http://localhost:5000` in your address bar to connect to the application.  Unless you crash the app, the changes you will make to the application will automagically appear in your browser (hot reloading).
4. Make changes, [tag and push](https://docs.docker.com/engine/reference/commandline/push/) to a container registry.  In order to run your application in the cloud, you will need your container images to be in a registry.

## Deployment to AWS Fargate

*Update Oct 21, 2020*: these instructions will no longer work because Docker disabled `docker ecs` feature in favor of `docker context`: https://docs.docker.com/engine/context/ecs-integration/ 

*Costs*: about $1 / day (ELB + ECS)

Follow the steps below or the instructions in [docker-ecs repo](https://github.com/docker/ecs-plugin/tree/master/example).

0. Set up and configure [AWS CLI](https://aws.amazon.com/cli/)
1. Update [ECS ARN resource format](https://aws.amazon.com/blogs/compute/migrating-your-amazon-ecs-deployment-to-the-new-arn-and-resource-id-format-2)
2. Connect Docker to AWS ECS: `docker ecs setup` and set context to `aws`
3. Switch Docker context from local development to AWS: `docker context use aws` (to revert to local, say `docker context use default`)
4. Magic: `docker ecs compose up` (takes a few minutes)
5. After a few minutes, retrieve the URL for your new app with `docker ecs compose ps` - looks like this `Dockerflask2faLoadBalancer-67be8e87ec9268e4.elb.us-east-1.amazonaws.com:5000`
6. This address points to an Elastic Load Balancer (ELB).  You can register the ELB in Cloudfront for HTTPS support and attach the Cloudfront distribution to a custom domain name.
