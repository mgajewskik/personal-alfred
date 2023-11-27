resource "aws_sns_topic" "admin" {
  name = "admin-notification-topic"
}

# resource "aws_sns_topic_subscription" "endpoint" {
#   topic_arn = aws_sns_topic.admin.arn
#   protocol  = "https"
#   endpoint  = "${aws_lambda_function_url.api.function_url}admin"
# }

resource "aws_sns_topic_subscription" "queue" {
  topic_arn = aws_sns_topic.admin.arn
  protocol  = "sqs"
  endpoint  = aws_sqs_queue.admin.arn
}

resource "aws_sqs_queue" "admin" {
  name                      = "admin-notification-queue"
  delay_seconds             = 90
  max_message_size          = 2048
  message_retention_seconds = 86400
  receive_wait_time_seconds = 10
  # redrive_policy = jsonencode({
  #   deadLetterTargetArn = aws_sqs_queue.terraform_queue_deadletter.arn
  #   maxReceiveCount     = 4
  # })
}

resource "aws_sqs_queue_policy" "admin" {
  queue_url = aws_sqs_queue.admin.id

  policy = <<POLICY
{
  "Version": "2012-10-17",
  "Id": "admin-sqs-policy",
  "Statement": [
    {
      "Sid": "First",
      "Effect": "Allow",
      "Principal": "*",
      "Action": "sqs:SendMessage",
      "Resource": "${aws_sqs_queue.admin.arn}",
      "Condition": {
        "ArnEquals": {
          "aws:SourceArn": "${aws_sns_topic.admin.arn}"
        }
      }
    }
  ]
}
POLICY
}
