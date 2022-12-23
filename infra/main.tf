provider "aws" {
  region      = var.aws_region
  max_retries = 10
}

resource "aws_s3_bucket" "storage" {
  bucket = "${local.resource_prefix}-storage"
  acl    = "private"

  server_side_encryption_configuration {
    rule {
      apply_server_side_encryption_by_default {
        sse_algorithm = "AES256"
      }
    }
  }
}

output "s3_bucket_name" {
  value = aws_s3_bucket.storage.id
}
