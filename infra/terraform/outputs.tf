output "api_lambda_url" {
  value = aws_lambda_function_url.api.function_url
}

output "bot_lambda_url" {
  value = aws_lambda_function_url.bot.function_url
}
