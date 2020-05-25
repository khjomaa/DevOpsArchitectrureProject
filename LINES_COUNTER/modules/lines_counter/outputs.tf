output "iam_for_lambda" {
  value = aws_iam_role.iam_for_lambda
}

output "bucket-arn" {
  value = aws_s3_bucket.bucket.arn
}