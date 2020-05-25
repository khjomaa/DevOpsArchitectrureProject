variable "bucket_name" {}
variable "bucket_acl" { default = "private" }
variable "bucket_force_destroy" { default = false }
variable "function_name" {}
variable "handler" {}
variable "runtime" {}
variable "filename" {}
variable "DB_HOST" {}
variable "DB_USERNAME" {}
variable "DB_PASSWORD" {}
variable "DB_DATABASE" {}
variable "LOG_LEVEL" {
  description = "Setting log level for the lambda function"
  default     = "INFO"
}

