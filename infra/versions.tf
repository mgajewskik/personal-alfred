terraform {
  required_version = ">= 0.12.26, < 1.2.0"

  backend "remote" {
    hostname     = "app.terraform.io"
    organization = "mgajewskik"

    workspaces {
      name = "alfred-service-stateful"
    }
  }

  required_providers {
    aws = {
      source  = "hashicorp/aws"
      version = ">= 2, < 5"
    }
  }
}
