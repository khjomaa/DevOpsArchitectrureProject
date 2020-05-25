output "database_endpoint" {
  value = aws_db_instance.default.address
}

output "database_port" {
  value = aws_db_instance.default.port
}