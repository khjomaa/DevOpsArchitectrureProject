provider "aws" {
  region  = "us-east-1"
  version = "~> 2.58"
}

module "lines_counter" {
  source               = "../../modules/lines_counter"
  bucket_name          = "khalilj-files-bucket"
  filename             = "lines_counter.zip"
  function_name        = "LinesCounter"
  handler              = "lines_counter.lambda_handler"
  runtime              = "python3.7"
  bucket_force_destroy = true
  DB_HOST              = "mysqldb.czepioy0aj4g.us-east-1.rds.amazonaws.com"
  DB_USERNAME          = "admin"
  DB_PASSWORD          = "admin123"
  DB_DATABASE          = "mysqldb"
}

output "s3_bucket_arn" {
  value       = module.lines_counter.bucket-arn
  description = "The ARN of the S3 bucket"
}
