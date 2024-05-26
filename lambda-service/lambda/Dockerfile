# Specify AWS Lambda Python 3.12 base image
FROM public.ecr.aws/lambda/python:3.12

# Copying requirements.txt into Docker's working directory
COPY requirements.txt ./

# Isnstall required package from requirements.txt and placing them in the LAMBDA_TASK_ROOT
#--target option allows to specify where packages should be installed
RUN python3 -m pip install -r requirements.txt --target ${LAMBDA_TASK_ROOT}

# Copy all file into LAMBDA_TASK_ROOT
COPY ./ ${LAMBDA_TASK_ROOT}

# Run the command on handler function from main.py file
CMD ["main.handler"]