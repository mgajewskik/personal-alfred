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

locals {
  resource_prefix = "${var.aws_region}-${var.service_name}-${var.environment}"
}
