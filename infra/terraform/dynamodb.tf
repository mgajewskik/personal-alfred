resource "aws_dynamodb_table" "table" {
  name             = "${local.resource_prefix}-table"
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
}
