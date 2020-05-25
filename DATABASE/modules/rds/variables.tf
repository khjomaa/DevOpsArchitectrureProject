# Security Settings
data "aws_vpc" "default_vpc" {
  default = true
}

data "aws_subnet_ids" "subnets" {
  vpc_id = data.aws_vpc.default_vpc.id
}

data "aws_security_group" "default-sg" {
  name = "default"
}

# MySQL Settings
variable "db_name" {
  description = "The name of the database to create when the DB instance is created"
  type        = string
}
variable "db_username" {
  description = "Username for the master DB user."
  type        = string
}
variable "db_password" {
  description = "Password for the master DB user"
  type        = string
}
variable "db_port" {
  description = "Database port"
  type        = number
}
variable "db_allocated-storage" {
  description = "The amount of allocated storage"
  type        = number
}
variable "db_storage-type" {
  description = "One of 'standard' (magnetic), 'gp2' (general purpose SSD), or 'io1' (provisioned IOPS SSD). The default is 'io1' if iops is specified, 'gp2' if not."
  type        = string
}
variable "db_engine" {
  description = "The database engine to use"
  type        = string
}
variable "db_engine-version" {
  description = "The engine version to use"
  type        = string
}
variable "db_instance-class" {
  description = "The instance type of the RDS instance"
  type        = string
}
variable "db_parameter-group-name" {
  description = "Name of the DB parameter group to associate"
  type        = string
}
variable "db_skip-final-snapshot" {
  description = "Determines whether a final DB snapshot is created before the DB instance is deleted"
  type        = bool
}
variable "db_publicly-accessible" {
  description = "Bool to control if instance is publicly accessible"
  type        = bool
}
variable "sql_script_file" {
  description = "Path of sql script"
  type        = string
}