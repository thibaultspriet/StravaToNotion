terraform {
  required_providers {
    aws = {
      source  = "hashicorp/aws"
      version = "5.22.0"
    }
  }
}

provider "aws" {
  region = "eu-north-1"
} # access key are set as environment variables

data "aws_iam_policy_document" "assume_role" {
  statement {
    effect = "Allow"

    principals {
      type        = "Service"
      identifiers = ["lambda.amazonaws.com"]
    }

    actions = ["sts:AssumeRole"]
  }
}

# Log resources
data "aws_iam_policy_document" "demo_lambda_logging" {
  statement {
    effect = "Allow"

    actions = [
      "logs:CreateLogGroup",
      "logs:CreateLogStream",
      "logs:PutLogEvents",
    ]

    resources = ["arn:aws:logs:*:*:*"]
  }
}

resource "aws_iam_policy" "demo_lambda_logging" {
  name        = "demo_lambda_logging"
  path        = "/"
  description = "IAM policy for logging from a lambda"
  policy      = data.aws_iam_policy_document.demo_lambda_logging.json
}

resource "aws_iam_role" "demo_iam_for_lambda" {
  name               = "demo_iam_for_lambda"
  assume_role_policy = data.aws_iam_policy_document.assume_role.json
}

resource "aws_iam_role_policy_attachment" "lambda_logs" {
  role       = aws_iam_role.demo_iam_for_lambda.name
  policy_arn = aws_iam_policy.demo_lambda_logging.arn
}

# Lambda function that receives events called the listener
variable "lambda_function_name" {
  default = "listener"
}

resource "aws_lambda_function" "listener_lambda" {
  filename      = "../deployment_package.zip"
  function_name = var.lambda_function_name
  role          = aws_iam_role.demo_iam_for_lambda.arn
  handler       = "listener.controller"
  runtime       = "python3.11"

  depends_on = [
    aws_iam_role_policy_attachment.lambda_logs,
    aws_cloudwatch_log_group.listener_logs,
  ]

  environment {
    variables = {
      SQS_URL = aws_sqs_queue.terraform_queue.url
    }
  }

}

resource "aws_lambda_function_url" "listener_url" {
  function_name      = aws_lambda_function.listener_lambda.function_name
  authorization_type = "NONE"
}

# This is to optionally manage the CloudWatch Log Group for the Lambda Function.
# If skipping this resource configuration, also add "logs:CreateLogGroup" to the IAM policy below.
resource "aws_cloudwatch_log_group" "listener_logs" {
  name              = "/aws/lambda/${var.lambda_function_name}"
  retention_in_days = 7
}

# FIFO queue to enable listener to push events to the event processor lamnda function
resource "aws_iam_role_policy" "sqs_policy" {
  name = "sqs_send_message_policy"
  role = aws_iam_role.demo_iam_for_lambda.name

  policy = <<EOF
{
  "Version": "2012-10-17",
  "Statement": [
    {
      "Effect": "Allow",
      "Action": "sqs:SendMessage",
      "Resource": "${aws_sqs_queue.terraform_queue.arn}"
    }
  ]
}
EOF
}
resource "aws_sqs_queue" "terraform_queue" {
  name                        = "demo_async_processing.fifo"
  fifo_queue                  = true
  content_based_deduplication = true
  delay_seconds               = 0
  max_message_size            = 262144
  message_retention_seconds   = 600
  receive_wait_time_seconds   = 0
}

# Lambda function that process events from the queue
variable "lambda_process_function_name" {
  default = "demo_process_events"
}

resource "aws_lambda_function" "process_events" {
  # If the file is not in the current working directory you will need to include a
  # path.module in the filename.
  filename      = "../deployment_package.zip"
  function_name = var.lambda_process_function_name
  role          = aws_iam_role.demo_iam_for_lambda.arn
  handler       = "process_events.controller"
  runtime       = "python3.11"

  depends_on = [
    aws_iam_role_policy_attachment.lambda_logs,
    aws_cloudwatch_log_group.process_events,
  ]

}

# Logs
resource "aws_cloudwatch_log_group" "process_events" {
  name              = "/aws/lambda/${var.lambda_process_function_name}"
  retention_in_days = 7
}

# Event mapping : trigger lambda function process_events from SQS
resource "aws_lambda_event_source_mapping" "sqs_trigger" {
  event_source_arn = aws_sqs_queue.terraform_queue.arn
  function_name    = aws_lambda_function.process_events.arn
}

# IAM
#Attachment of a Managed AWS IAM Policy for Lambda sqs execution
resource "aws_iam_role_policy_attachment" "lambda_basic_sqs_queue_execution_policy" {
  policy_arn = "arn:aws:iam::aws:policy/service-role/AWSLambdaSQSQueueExecutionRole"
  role       = aws_iam_role.demo_iam_for_lambda.name
}