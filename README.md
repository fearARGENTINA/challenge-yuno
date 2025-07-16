# Challenge Yuno

## Requirements:
1. docker available and running.
2. docker-compose available.

## To start project
1. Clone repository: `git clone https://github.com/fearARGENTINA/challenge-yuno`
2. Go into root folder: `cd challenge-yuno`
3. Build project images: `docker-compose build`
4. Run docker services: `docker-compose up`
5. Elasticsearch, Kibana, Postgres and lastly API services will run in order. Once all service are up and running you can interact with the API.

## Methods
**Due to time constraints I were unable to create an OpenAPI or Swagger documents, so below you will find most important methods documented**

### OAuth Methods
**Basically, all the API is JWT and role protected. To obtain a JWT one needs to authenticate through OAuth2 against Google, at final step we will obtain a JWT token. If the user joins for first time he will obtain the default role which is GUEST role, for other roles one needs to be upgraded by admin account that is specified in the environment variable DEFAULT_ADMIN_EMAIL**
- GET /oauth/login : It will return a URL which needs to be followed by the frontend or manually by the client to authenticate against Google services. Once the user approves the OAuth2 flow against Google he is redirected back to the callback API endpoint.

- GET /oauth/callback : It expects parameters associated to OAuth2 flow like authorization code. This method, using this previous authorization code, will obtain an access token and userinfo from Google Services, and lastly build a JWT using symetric HS256 algorithm.

## Users
**This methods allow to do CRUD operations against user objects. IMPORTANT: users are not the main objective of the challenge, they are only the users that authenticate against OAuth2 service and so later they can obtain a role and interact against API methods like Employees**

- GET /user/<id> (Roles allowed: USER, ADMIN): It retrieves a user by its id.

- GET /users (Roles allowed: USER, ADMIN): Allows searching for multiple users using fields like username

- POST /user (Roles allowed: ADMIN): Allows to create a user. Expects JSON user object in body.

- PUT /user/<id> (Roles allowed: ADMIN): Allow to update a user by id. Expects JSON user object in body.

## Employees
- GET /employee/<id> (Roles allowed: USER, ADMIN): It retrieves a employee by its id.

- GET /employees (Roles allowed: USER, ADMIN): Allows searching for multiple employees using fields like firstName, lastName, address, phone, minAge, maxAge.

- POST /employee (Roles allowed: ADMIN): Allows to create a employee. Expects JSON employee object in body.

- PUT /employee/<id> (Roles allowed: ADMIN): Allow to update a employee by id. Expects JSON employee object in body.

# Questions

## What services would you use?
I would use Amazon EKS, maybe deployed through AWS CloudFormation or Terraform, just for creating and updating cluster, control plane, ingress, ingress controllers, etc. I would use an Application Load Balancer placed in front of the EKS services.
For security purposes would leverage multiple VPC's like following:
- Workload VPC used for containing EKS loads, like pods inside a specified namespace for production loads. Use this VPC only for production services.
- Inspection VPC to place a firewall endpoint, that acts as a middleware or sniffer to be able to limit reachability and be capable of creating dynamic rules if needed.
- Ingress VPC: used to place the application load balancer facing internet through internet gateway. In this step we could integrate AWS WAF or a 3rd party WAF like Cloudflare, which are facing to internet and inspect ingress traffic.
**All this VPC's would be connected through Transit Gateway routing between VPC's**

Obviously for application services I would use Amazon RDS for deploying a Postgres relational database, so i would benefit from AWS RDS autoscaling and high availability.
In this case I'm using Elasticsearch as monitoring solution (like SIEM or log aggregator), but we can leverage AWS OpenSearch solution.
Also use AWS ECR for docker image storage.
We could use AWS Secrets for secret management (creation and rotation) and lately integrate into application.

I would use Gitlab for version control. Then Azure DevOps for CI (building steps and uploading image to image repository) and CD (deploying application into EKS)
With Gitlab and Azure DevOps one could be capable of integrating multiple security testing steps which are gonna be touched in "What security controls would you include?" point.

## How would you create the infrastructure?
The infrastructure would be deployed using Terraform, so it can be maintained and documented throughout time, and also be version controled using Gitlab for example.

## How would you maintain it?
As said before using Terraform and a version control solution. Of course this solutions would need to be attended in case of security issues like dependencies vulnerabilities for example.
Also the certs would needs to maintained as we would needs to renew them, and we could use for example certbot.

## What security controls would you include?
As explained before, in Gitlab one could implement some SAST scanning solutions like for example Sonarqube or Snyk, also a secret leak scanner like gitleaks, and some SCA scanner like trivy.
In Azure DevOps or CI/CD part one could leverage some image scanner like Trivy and implement DAST scanning steps through preconfigured dynamic test or using an automated tool like OWASP ZAP.
For Terraform manifests one could also implement some IaC scanning tool like tfsec and also a secret leak scanner like gitleaks, so one could detect misconfigurations or injected vulnerabilities.
In the case of the infrastructure, i would implement as explained before an AWS Firewall, an AWS WAF, loads isolation through multiple step VPC's, etc.

# Diagram
![diagram](https://github.com/fearARGENTINA/challenge-yuno/blob/main/static/Challenge%20Yuno%20diagram.drawio.png)
