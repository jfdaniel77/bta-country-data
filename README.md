# Building REST API using AWS Chalice (under development) :hammer:

![GitHub last commit](https://img.shields.io/github/last-commit/jfdaniel77/bta-country-data)
![GitHub](https://img.shields.io/github/license/jfdaniel77/bta-country-data)
![Status](https://img.shields.io/badge/status-in%20progress-blue)


This is a simple workshop to build REST API using [AWS Chalice](https://aws.github.io/chalice/). AWS Chalice is a framework for writing serverless apps in Python.  It provides:

* A command line tool for creating, deploying, and managing your app
* A decorator based API for integrating with [Amazon API Gateway](https://aws.amazon.com/api-gateway/), [Amazon S3](https://aws.amazon.com/s3/), [Amazon SNS](https://aws.amazon.com/sns/), [Amazon SQS](https://aws.amazon.com/sqs/), and other AWS services.
* Automatic IAM policy generation
* CI/CD pipeline generation
* Local testing support
* Native Python packaging
* [AWS SAM](https://docs.aws.amazon.com/serverless-application-model/latest/developerguide/what-is-sam.html) and [Terraform](https://www.terraform.io/) integration

In this workshop, we are going to build simple REST APIs to list all countries in the world and get currency name for a particular country. In highlevel overview, you will do these thngs to complete this workshop:
* Setting working environment
* Build two simple functions to return list of countries and currency name
* Perform unit test for both functions to verify if those are working as expected
* Adding authentication feature
* Deploy application using simple CI/CD pipeline

You can use browser or any REST client tool (e.g. [Postman](https://www.postman.com/), [Insomnia](https://insomnia.rest/), etc) to test your REST APIs.

This repository contains final solution for this workshop. You can clone it to your local machine and deploy it to see the result. However, I recommend you to make your hands dirty with trying it from scratch after reading this guideline :smile:

> Note: Repository for CI/CD pipeline in this workshop uses [AWS Code Commit](). If you clone the workshop from this GitHub repository and want to run deployment provided in this workshop, you need to follow this [guideline](https://docs.aws.amazon.com/codecommit/latest/userguide/how-to-mirror-repo-pushes.html)

## Pre-requisites
These are pre-requisite for this workshop.
+ You need to have an AWS account.
  If you do not have an AWS account, you can follow following steps:
  - Go to [https://aws.amazon.com/](https://aws.amazon.com/)
  - Choose Sign In to the Console.
  - Choose Create a new AWS account.
  - Complete the process by following the on-screen directions. This includes giving AWS your email address and credit card information. You must also use your phone to enter a code that AWS gives you.

  After you finish creating the account, AWS will send you a confirmation email. Do not go to the next step until you get this confirmation.
  
  To watch a 4-minute video related to the following procedure, see [Creating an Amazon Web Services Account](https://www.youtube.com/watch?v=WviHsoz8yHk) on the YouTube website.

+ You can use any text editor or IDE to follow this workshop.

+ To start working with AWS Chalice, there are some requirements your development environment must have:

  - Python 3.7
  
    This workshop requires Python 3.7 for developing and running your Chalice application. 
    First, you need check to see if Python is already installed on your development environment:
    
    ```
    $ python --version
    Python 3.7.9
    ```
    
  - Virtualenv

    It is a tool for creating isolated Python environments containing their own copy of python , pip , and their own place to keep libraries installed from PyPI. It's designed to allow you to work on multiple projects with different dependencies at the same time on the same machine. 
    
  - AWS credentials
  
    To use AWS Chalice, you will need AWS credentials. If you currently use one of the AWS SDKs or the AWS CLI on your development environment, you should already have AWS credentials set up. There are 2 ways to check if you have already it.
    
    * Checking if you have either a `~/.aws/credentials` or `~/.aws/config` file on your machine.
    * Run this syntax

      ```
      $ aws --version
      aws-cli/1.19.79 Python/2.7.18 Linux/4.14.232-176.381.amzn2.x86_64 botocore/1.20.79
      ```
    
  - git
    
    You need git to clone and deploy this workshop in your own AWS account. To check if you have git in your machine, you can run this syntax
    
    ```
     $ git --version
     git version 2.23.4
    ```
    
    If you choose to build REST APIs in this workshop from scratch, you do not need to do clone. git will be required at the time when you build CI/CD pipeline to automate deployment process.

## Disclaimer

All AWS services created in this workshop may incurre a cost. If you just created an AWS account, all AWS services in this workshop are mostly covered by AWS Free Tier. You will be only charged when your usage is beyond AWS Free Tier limit. For more detail, please refer to this [AWS FreeTier FAQs](https://aws.amazon.com/free/free-tier-faqs/). No upfront investments are required and you only pay only for the resources you use.

## Architecture
![Architecture Diagram](https://github.com/jfdaniel77/bta-country-data/blob/main/docs/images/architecture.JPG)


### REST APis
This is REST APIs that we are going to build:

| HTTP Method | URI Path            | Description       |
|-------------|---------------------|-------------------|
| GET         | /country            | List of countries |
| GET         | /currency/{country} | Get currency name |

## Code Walkthrough

### Environment Setup

a. Create new Chalice projects

```
$ chalice new-project country-data
Your project has been generated in ./country-data
```

To ensure that the project was created correctly, list the contents of the newly created ```country-data``` directory.
Please make sure that ```country-data``` directory contains ```app.py``` and ```requirements.txt```.

```
$ ls -la
total 8
drwxrwxr-x 3 ec2-user ec2-user  78 Jun  8 13:07 .
drwxrwxr-x 3 ec2-user ec2-user  26 Jun  8 13:07 ..
-rw-rw-r-- 1 ec2-user ec2-user 737 Jun  8 13:07 app.py
drwxrwxr-x 2 ec2-user ec2-user  25 Jun  8 13:07 .chalice
-rw-rw-r-- 1 ec2-user ec2-user  37 Jun  8 13:07 .gitignore
-rw-rw-r-- 1 ec2-user ec2-user   0 Jun  8 13:07 requirements.txt
```

Let's verify that our new application is working. Run ```chalice local``` to spin up a version of the application running locally:
```
$ chalice local
Serving on http://127.0.0.1:8000
Restarting local dev server.
Serving on http://127.0.0.1:8000
```

Open another terminal and make an HTTP request to application running the ```localhost```:

```
$ pip install httpie
```

```
 $ http http://127.0.0.1:8000
HTTP/1.1 200 OK
Content-Length: 17
Content-Type: application/json
Date: Tue, 08 Jun 2021 13:17:23 GMT
Server: BaseHTTP/0.6 Python/3.7.9

{
    "hello": "world"
}
```

If we looked at our original terminal, our HTTP request is logged on console.

```
127.0.0.1 - - [08/Jun/2021 13:17:23] "GET / HTTP/1.1" 200 -
```

b. Install Dependencies



```python
@app.route('/')
def index():
    return {'hello': 'world'}
```

```python
@app.route('/country-list', methods=['GET'], cors=True)
def get_country_list():
    """
    This function returns all countries.
    
    Args: N/A
    
    Returns: List of country in JSON format.
    """
    data = []

    for country in pycountry.countries:
        record = {}
        record["code"] = country.alpha_2
        
        name = country.name
        record["name"] = name
        
        data.append(record)

    return data
```

```python
@app.route('/currency/{country}', methods=['GET'], cors=True)
def get_currency(country):
    """
    This function returns currency based on country.
    
    Args: country
    
    Returns: Currency name in JSON format
    """
    
    if country is None or len(country) == 0:
        raise BadRequestError("Country is required in this REST APi")
        
    result = pycountry.countries.search_fuzzy(country)
    
    data = []
    
    if result is None or len(result) == 0:
        raise BadRequestError("Country {} is not availalbe".format(country))
    else:
        for country in result:
            currency = {}
            value = pycountry.currencies.get(numeric=country.numeric)
            if value:
                currency['currency'] = value.name
                data.append(currency)
    
    return data
```

## Deployment
Chalice is equipped with basic CI/CD pipeline especially when you are working in a team. Using this pipeline, you can perform testing on code changes, build test stage and promote build to production stage automatically. Behind the scene, Chalice will generate a CloudFormation template that is used to build intial CI/CD pipeline. By default, it contains an AWS CodeCommit repo, an AWS CodeBuild stage for packaging your chalice app, and an AWS CodePipeline stage to deploy your application using CloudFormation.

## Testing

## Cleaning Up
Deleting resources that are not actively being used reduces costs and is a best practice. Not deleting your resources will result in charges to your account.

## Next Steps
Now, that you understand how to build a simple application using AWS Chalice, you can use this workshop as starting point for building your own. You can find more application samples at [here](https://chalice-workshop.readthedocs.io/en/latest/)

## Feedbacks
If you have any feedback or encounter an issue, please open an issue or describe the proposed changes in your pull request.
