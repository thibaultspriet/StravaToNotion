variable "VERIFY_TOKEN" {
  description = "The Strava verify token"
  type        = string
}

variable "ACCOUNT_ID" {
  description = "The aws account id"
  type        = string
}

variable "AIRTABLE_PAT" {
  description = "airtable personal access token for the strava base"
  type        = string
}

variable "AIRTABLE_BASE_ID" {
  description = "id of the airtable base"
  type        = string
}

variable "AIRTABLE_TABLE_STRAVA_ID" {
  description = "id of the table that stores Strava tokens"
  type        = string
}

variable "AIRTABLE_TABLE_REL_STRAVA_NOTION_ID" {
  description = "id of the table that stores relation between Strava athlete id and Notion bot id"
  type        = string
}

variable "AIRTABLE_TABLE_NOTION" {
  description = "id of the table that stores Notion integration data"
  type        = string
}

variable "STRAVA_CLIENT_ID" {
  description = "client id of Strava application"
  type        = string
}

variable "STRAVA_CLIENT_SECRET" {
  description = "client secret of Strava application"
  type        = string
}

variable "NOTION_CLIENT_ID" {
  description = "client id of Notion integration"
  type        = string
}

variable "NOTION_CLIENT_SECRET" {
  description = "client secret of Notion integration"
  type        = string
}

variable "NOTION_CLIENT_REDIRECT_URI" {
  description = "Notion redirect URI of integration"
  type        = string
}

variable "lambda_function_name" {
  description = "lambda function name of Strava callback"
  default     = "strava_webhook"
}

variable "region" {
  description = "AWS deployment region"
  default     = "eu-north-1"
}

variable "sqs_name" {
  description = "name of sqs queue"
  default     = "strava-events.fifo"
}




terraform {
  required_providers {
    aws = {
      source  = "hashicorp/aws"
      version = "5.22.0"
    }
  }
}

provider "aws" {
  region = var.region
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

############ Logs ############
data "aws_iam_policy_document" "lambda_logging" {
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

resource "aws_iam_policy" "lambda_logging" {
  name        = "lambda_logging"
  path        = "/"
  description = "IAM policy for logging from a lambda"
  policy      = data.aws_iam_policy_document.lambda_logging.json
}

resource "aws_iam_role" "iam_for_lambda" {
  name               = "iam_for_lambda"
  assume_role_policy = data.aws_iam_policy_document.assume_role.json
}

resource "aws_iam_role_policy_attachment" "lambda_logs" {
  role       = aws_iam_role.iam_for_lambda.name
  policy_arn = aws_iam_policy.lambda_logging.arn
}

############ Lambda : strava webhook ############

resource "aws_lambda_function" "test_lambda" {
  filename      = "../deployment_package.zip"
  function_name = var.lambda_function_name
  role          = aws_iam_role.iam_for_lambda.arn
  handler       = "lambda_function.controller"
  runtime       = "python3.11"

  depends_on = [
    aws_iam_role_policy_attachment.lambda_logs,
    aws_cloudwatch_log_group.strava_webhook,
  ]

  environment {
    variables = {
      VERIFY_TOKEN = var.VERIFY_TOKEN,
      SQS_URL      = aws_sqs_queue.terraform_queue.url
      NOTION_CLIENT_ID = var.NOTION_CLIENT_ID
      NOTION_CLIENT_SECRET = var.NOTION_CLIENT_SECRET
      NOTION_CLIENT_REDIRECT_URI = var.NOTION_CLIENT_REDIRECT_URI
    }
  }
}

resource "aws_lambda_function_url" "test_latest" {
  function_name      = aws_lambda_function.test_lambda.function_name
  authorization_type = "NONE"
}

# This is to optionally manage the CloudWatch Log Group for the Lambda Function.
# If skipping this resource configuration, also add "logs:CreateLogGroup" to the IAM policy below.
resource "aws_cloudwatch_log_group" "strava_webhook" {
  name              = "/aws/lambda/${var.lambda_function_name}"
  retention_in_days = 7
}

############ SQS FIFO queue ############
resource "aws_iam_role_policy" "sqs_policy" {
  name = "sqs_send_message_policy"
  role = aws_iam_role.iam_for_lambda.name

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
  name                        = var.sqs_name
  fifo_queue                  = true
  content_based_deduplication = true
  delay_seconds               = 0
  max_message_size            = 262144
  message_retention_seconds   = 600
  receive_wait_time_seconds   = 0
  redrive_policy = jsonencode({
    deadLetterTargetArn = aws_sqs_queue.terraform_queue_deadletter.arn
    maxReceiveCount     = 1
  })
}

resource "aws_sqs_queue" "terraform_queue_deadletter" {
  name                        = "dlq-strava-events.fifo"
  fifo_queue                  = true
  content_based_deduplication = true
  message_retention_seconds   = 604800 // 7 days
  redrive_allow_policy = jsonencode({
    redrivePermission = "byQueue",
    sourceQueueArns   = ["arn:aws:sqs:${var.region}:${var.ACCOUNT_ID}:${var.sqs_name}"]
  })
}

############ Lambda : process events ############
variable "lambda_process_function_name" {
  default = "process_events"
}

resource "aws_lambda_function" "process_events" {
  # If the file is not in the current working directory you will need to include a
  # path.module in the filename.
  filename      = "../deployment_package.zip"
  function_name = var.lambda_process_function_name
  role          = aws_iam_role.iam_for_lambda.arn
  handler       = "lambda_process_events.controller"
  runtime       = "python3.11"
  timeout       = 60

  environment {
    variables = {
      AIRTABLE_PAT                        = var.AIRTABLE_PAT
      AIRTABLE_BASE_ID                    = var.AIRTABLE_BASE_ID
      AIRTABLE_TABLE_STRAVA_ID            = var.AIRTABLE_TABLE_STRAVA_ID
      AIRTABLE_TABLE_REL_STRAVA_NOTION_ID = var.AIRTABLE_TABLE_REL_STRAVA_NOTION_ID
      AIRTABLE_TABLE_NOTION               = var.AIRTABLE_TABLE_NOTION
      STRAVA_CLIENT_ID                    = var.STRAVA_CLIENT_ID
      STRAVA_CLIENT_SECRET                = var.STRAVA_CLIENT_SECRET
    }
  }

  depends_on = [
    aws_iam_role_policy_attachment.lambda_logs,
    aws_cloudwatch_log_group.process_events,
  ]

}

// Logs
resource "aws_cloudwatch_log_group" "process_events" {
  name              = "/aws/lambda/${var.lambda_process_function_name}"
  retention_in_days = 7
}

// Event mapping : trigger from SQS
resource "aws_lambda_event_source_mapping" "sqs_trigger" {
  event_source_arn        = aws_sqs_queue.terraform_queue.arn
  function_name           = aws_lambda_function.process_events.arn
  function_response_types = ["ReportBatchItemFailures"]
}

// IAM
#Attachment of a Managed AWS IAM Policy for Lambda sqs execution
resource "aws_iam_role_policy_attachment" "lambda_basic_sqs_queue_execution_policy" {
  policy_arn = "arn:aws:iam::aws:policy/service-role/AWSLambdaSQSQueueExecutionRole"
  role       = aws_iam_role.iam_for_lambda.name
}
