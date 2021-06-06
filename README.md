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

In this workshop, we are going to build simple REST APIs to list all countries in the world and get currency name for a particular country. 

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

## Code Walkthrough

### Environment Setup

### Install Dependencies

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

## Testing

## Cleaning Up
Deleting resources that are not actively being used reduces costs and is a best practice. Not deleting your resources will result in charges to your account.

## Next Steps

## Feedbacks
If you have any feedback or encounter an issue, please open issues or describe the proposed changes in your pull request.
