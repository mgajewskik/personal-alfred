terraform {
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
      version = ">= 4.48.0"
    }
  }
}
