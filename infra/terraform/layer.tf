# always rebuild is the only way to work in CI
# resource "null_resource" "build_layer" {
#   provisioner "local-exec" {
#     # command     = "${local.root_path}/run build"
#     command = "pwd;ls -a;cd ..;pwd;ls -a;cd ..;pwd;ls -a"
#   }
#   triggers = {
#     always_run = "${timestamp()}"
#   }
# }

# data "archive_file" "lambda_layer" {
#   type        = "zip"
#   source_dir  = local.layer_package_path
#   output_path = local.layer_zip_path
#   excludes = [
#     "__pycache__",
#     "**/__pycache__",
#     "*.zip"
#   ]
#   # depends_on = [null_resource.build_layer]
# }
#
# data "archive_file" "lambda_package" {
#   type        = "zip"
#   source_dir  = local.lambda_package_path
#   output_path = local.lambda_zip_path
#   excludes = [
#     "__pycache__",
#     "**/__pycache__",
#   ]
#   # depends_on = [null_resource.build_layer]
# }

resource "aws_lambda_layer_version" "layer" {
  filename            = local.layer_zip_path
  layer_name          = "${local.resource_prefix}-layer"
  compatible_runtimes = ["python3.9"]

  # TODO make this not update every time
  source_code_hash = filebase64sha256(local.layer_zip_path)
}
