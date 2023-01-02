variable "aws_region" {
  type    = string
  default = "eu-west-1"
}

variable "service_name" {
  type = string
}

variable "environment" {
  type    = string
  default = "dev"
}

variable "base_domain" {
  type = string
}

variable "telegram_bot_token" {
  type = string
}

variable "admin_chat_id" {
  type = string
}

variable "dummy_auth_token" {
  type = string
}

variable "lumigo_tracer_token" {
  type = string
}

locals {
  resource_prefix = "${var.aws_region}-${var.service_name}-${var.environment}"

  # old variables for zipping archives in terraform
  # root_path           = "${path.module}/../.."
  # lambda_package_path = "${local.root_path}/service"
  # package_path        = "${local.root_path}/infra/terraform/package"
  # layer_package_path  = "${local.package_path}/zip"
  # lambda_zip_path     = "${local.package_path}/lambda.zip"
  # layer_zip_path      = "${local.package_path}/layer.zip"

  lambda_zip_path = "${path.module}/lambda.zip"
  layer_zip_path  = "${path.module}/layer.zip"
}
