provider "aws" {
  region      = var.aws_region
  max_retries = 10
}

module "api" {
  source          = "./modules/lambda"
  resource_prefix = local.resource_prefix
  name            = "api"
  handler         = "service.lambdas.api.lambda_handler"
  memory_size     = 128

  env = {
    "LOG_LEVEL"               = "DEBUG"
    "ADMIN_CHAT_ID"           = var.admin_chat_id
    "DUMMY_AUTH_TOKEN"        = var.dummy_auth_token
    "TELEGRAM_BOT_TOKEN"      = var.telegram_bot_token
    "LUMIGO_TRACER_TOKEN"     = var.lumigo_tracer_token
    "DYNAMO_TABLE_NAME"       = aws_dynamodb_table.table.name
    "DYNAMO_TABLE_STREAM_ARN" = aws_dynamodb_table.table.stream_arn
    "SQS_QUEUE_URL"           = aws_sqs_queue.admin.url
    "SNS_TOPIC_ARN"           = aws_sns_topic.admin.arn
  }

  permissions = [
    "logs:CreateLogGroup",
    "logs:CreateLogStream",
    "logs:PutLogEvents",
    "sns:Publish",
    "sqs:SendMessage",
    "sqs:ReceiveMessage",
  ]

  filename = local.lambda_zip_path
  layers = [
    aws_lambda_layer_version.layer.arn
  ]
}

resource "aws_lambda_function_url" "api" {
  function_name      = module.api.function_name
  authorization_type = "NONE"
}

module "bot" {
  source          = "./modules/lambda"
  resource_prefix = local.resource_prefix
  name            = "bot"
  handler         = "service.lambdas.bot.lambda_handler"
  memory_size     = 128

  env = {
    "LOG_LEVEL"               = "DEBUG"
    "ADMIN_CHAT_ID"           = var.admin_chat_id
    "DUMMY_AUTH_TOKEN"        = var.dummy_auth_token
    "TELEGRAM_BOT_TOKEN"      = var.telegram_bot_token
    "LUMIGO_TRACER_TOKEN"     = var.lumigo_tracer_token
    "DYNAMO_TABLE_NAME"       = aws_dynamodb_table.table.name
    "DYNAMO_TABLE_STREAM_ARN" = aws_dynamodb_table.table.stream_arn
    "SQS_QUEUE_URL"           = aws_sqs_queue.admin.url
    "SNS_TOPIC_ARN"           = aws_sns_topic.admin.arn
  }

  permissions = [
    "logs:CreateLogGroup",
    "logs:CreateLogStream",
    "logs:PutLogEvents",
    "dynamodb:DescribeStream",
    "dynamodb:GetRecords",
    "dynamodb:ListStreams",
    "dynamodb:DescribeTable",
    "dynamodb:ListTagsOfResource",
    "dynamodb:Query",
    "dynamodb:Scan",
    "dynamodb:BatchGetItem",
    "dynamodb:BatchWriteItem",
    "dynamodb:PutItem",
    "dynamodb:UpdateItem",
    "dynamodb:DeleteItem",
    "dynamodb:GetItem",
  ]

  filename = local.lambda_zip_path
  layers = [
    aws_lambda_layer_version.layer.arn
  ]
}

resource "aws_lambda_function_url" "bot" {
  function_name      = module.bot.function_name
  authorization_type = "NONE"
}
