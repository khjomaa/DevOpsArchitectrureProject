resource "aws_security_group" "rds-sg" {
  name   = var.db_name
  vpc_id = data.aws_vpc.default_vpc.id
}

resource "aws_security_group_rule" "allow_db_access" {
  from_port         = var.db_port
  protocol          = "TCP"
  security_group_id = aws_security_group.rds-sg.id
  to_port           = var.db_port
  type              = "ingress"
  cidr_blocks       = ["0.0.0.0/0"]
}

resource "aws_security_group_rule" "egress-all" {
  from_port         = 0
  protocol          = "TCP"
  security_group_id = aws_security_group.rds-sg.id
  cidr_blocks       = ["0.0.0.0/0"]
  to_port           = 0
  type              = "egress"
}
