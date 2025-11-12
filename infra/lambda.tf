resource "aws_iam_role" "lambda_role" {
  name = "${var.project_name}-lambda-role-${random_id.suffix.hex}"
  assume_role_policy = jsonencode({
    Version = "2012-10-17",
    Statement = [{
      Effect    = "Allow",
      Principal = { Service = "lambda.amazonaws.com" },
      Action    = "sts:AssumeRole"
    }]
  })
}


resource "aws_iam_role_policy_attachment" "lambda_basic" {
  role       = aws_iam_role.lambda_role.name
  policy_arn = "arn:aws:iam::aws:policy/service-role/AWSLambdaBasicExecutionRole"
}

# Built by the workflow into ../backend_build
data "archive_file" "lambda_zip" {
  type        = "zip"
  source_dir  = "${path.module}/../backend_build"
  output_path = "${path.module}/../backend_build/lambda.zip"
}

resource "aws_lambda_function" "func" {
  function_name    = "${var.project_name}-handler-${random_id.suffix.hex}"
  role             = aws_iam_role.lambda_role.arn
  runtime          = "python3.12"
  handler          = "lambda_handler.lambda_handler" # file.function
  filename         = data.archive_file.lambda_zip.output_path
  source_code_hash = data.archive_file.lambda_zip.output_base64sha256
  timeout          = 10
  memory_size      = 256
  environment {
    variables = { STAGE = "prod" }
  }
}

output "lambda_name" { value = aws_lambda_function.func.function_name }
