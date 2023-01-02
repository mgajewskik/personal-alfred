resource "aws_lambda_function" "lambda" {
  filename         = var.filename
  source_code_hash = filebase64sha256(var.filename)
  function_name    = "${var.resource_prefix}-${var.name}"
  role             = aws_iam_role.lambda.arn
  handler          = var.handler
  runtime          = "python3.9"
  memory_size      = var.memory_size

  environment {
    variables = var.env
  }

  layers = var.layers
}

resource "aws_iam_role" "lambda" {
  name = "${var.resource_prefix}-${var.name}-lambda-role"

  assume_role_policy = jsonencode({
    Version = "2012-10-17"
    Statement = [
      {
        Action = "sts:AssumeRole"
        Effect = "Allow"
        Sid    = ""
        Principal = {
          Service = "lambda.amazonaws.com"
        }
      },
    ]
  })
}

resource "aws_iam_policy" "lambda" {
  name = "${var.resource_prefix}-${var.name}-lambda-policy"
  path = "/"

  policy = jsonencode({
    Version = "2012-10-17"
    Statement = [
      {
        Action   = var.permissions
        Effect   = "Allow"
        Resource = "*"
      },
    ]
  })
}

resource "aws_iam_role_policy_attachment" "lambda" {
  role       = aws_iam_role.lambda.name
  policy_arn = aws_iam_policy.lambda.arn
}
