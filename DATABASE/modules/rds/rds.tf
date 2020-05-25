resource "aws_db_instance" "default" {
  identifier             = var.db_name
  allocated_storage      = var.db_allocated-storage
  storage_type           = var.db_storage-type
  engine                 = var.db_engine
  engine_version         = var.db_engine-version
  instance_class         = var.db_instance-class
  name                   = var.db_name
  username               = var.db_username
  password               = var.db_password
  port                   = var.db_port
  parameter_group_name   = var.db_parameter-group-name
  skip_final_snapshot    = var.db_skip-final-snapshot
  publicly_accessible    = var.db_publicly-accessible
  vpc_security_group_ids = [ aws_security_group.rds-sg.id, data.aws_security_group.default-sg.id]

  //   provisioner "local-exec" {
  //     command = "mysql -h ${aws_db_instance.default.address} -u${aws_db_instance.default.username} -p${aws_db_instance.default.password} -D${aws_db_instance.default.name} < ${var.sql_script_file}"
  //   }
}

resource "null_resource" "create_tables" {
  depends_on = [aws_db_instance.default]

  provisioner "local-exec" {
    command = "mysql -h ${aws_db_instance.default.address} -u${aws_db_instance.default.username} -p${aws_db_instance.default.password} -D${aws_db_instance.default.name} < ${var.sql_script_file}"
  }
}