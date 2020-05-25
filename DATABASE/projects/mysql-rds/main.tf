provider "aws" {
  region  = "us-east-1"
  version = "~> 2.58"
}

provider "null" {
  version = "~> 2.1"
}

module "rds" {
  source                  = "../../modules/rds"
  db_allocated-storage    = 5
  db_storage-type         = "gp2"
  db_engine               = "mysql"
  db_engine-version       = "5.7"
  db_instance-class       = "db.t2.micro"
  db_name                 = "mysqldb"
  db_username             = "admin"
  db_password             = "admin123"
  db_port                 = 3306
  db_parameter-group-name = "default.mysql5.7"
  db_skip-final-snapshot  = true
  db_publicly-accessible  = true
  sql_script_file         = "./sql_scripts/create_tables.sql"
}

output "database_endpoint" {
  value = module.rds.database_endpoint
}

output "database_port" {
  value = module.rds.database_port
}
