resource "aws_lambda_function" "function" {
  function_name = var.function_name
  handler       = var.handler
  role          = aws_iam_role.iam_for_lambda.arn
  runtime       = var.runtime
  filename      = var.filename

  environment {
    variables = {
      DB_HOST     = var.DB_HOST
      DB_USERNAME = var.DB_USERNAME
      DB_PASSWORD = var.DB_PASSWORD
      DB_DATABASE = var.DB_DATABASE
      LOG_LEVEL   = var.LOG_LEVEL
    }
  }
}

resource "aws_lambda_permission" "allow_bucket_lambda" {
  statement_id  = "AllowExecutionFromS3Bucket"
  action        = "lambda:InvokeFunction"
  function_name = aws_lambda_function.function.arn
  principal     = "s3.amazonaws.com"
  source_arn    = aws_s3_bucket.bucket.arn
}

resource "aws_s3_bucket_notification" "allow_s3_bucket_notification" {
  bucket = aws_s3_bucket.bucket.bucket

  lambda_function {
    lambda_function_arn = aws_lambda_function.function.arn
    events              = ["s3:ObjectCreated:*"]
  }
}
