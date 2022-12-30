resource "aws_dynamodb_table" "users" {
  name             = "${local.resource_prefix}-users"
  billing_mode     = "PAY_PER_REQUEST"
  stream_enabled   = true
  stream_view_type = "NEW_AND_OLD_IMAGES"
  hash_key         = "PK"
  range_key        = "SK"

  attribute {
    name = "PK"
    type = "S"
  }

  attribute {
    name = "SK"
    type = "S"
  }

  attribute {
    name = "DATA"
    type = "S"
  }

  attribute {
    name = "CreatedAt"
    type = "N"
  }

  # TODO LSI might be not needed at all, check with other PK values
  local_secondary_index {
    name            = "LSI1"
    range_key       = "CreatedAt"
    projection_type = "ALL"
  }

  global_secondary_index {
    name            = "GSI1"
    hash_key        = "SK"
    range_key       = "DATA"
    projection_type = "ALL"
  }

  global_secondary_index {
    name            = "GSI2"
    hash_key        = "SK"
    range_key       = "CreatedAt"
    projection_type = "ALL"
  }

  server_side_encryption {
    enabled = true
  }

  # seems to be not needed for pay per request model
  # lifecycle {
  #   ignore_changes = [
  #     read_capacity, write_capacity
  #   ]
  # }
}

output "users_table_name" {
  value = aws_dynamodb_table.users.name
}

output "users_table_stream_arn" {
  value = aws_dynamodb_table.users.stream_arn
}
