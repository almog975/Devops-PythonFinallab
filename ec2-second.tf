# Second region compute (aliased provider = aws.second)

# --- Public Windows instance ---
# RDP is permitted only from the primary region's public Windows instance's
# public IP - no other source (not even the user's own computer).

resource "aws_security_group" "second_public_win_sg" {
  provider    = aws.second
  name        = "${local.second_name}-Public-Win-SG"
  vpc_id      = aws_vpc.second.id

  ingress {
    description = "RDP from the primary region's public Windows instance only"
    from_port   = 3389
    to_port     = 3389
    protocol    = "tcp"
    cidr_blocks = ["${aws_instance.primary_public_win.public_ip}/32"]
  }

  egress {
    from_port   = 0
    to_port     = 0
    protocol    = "-1"
    cidr_blocks = ["0.0.0.0/0"]
  }

  tags = {
    Name = "${local.second_name}-Public-Win-SG"
  }
}

resource "aws_instance" "second_public_win" {
  provider               = aws.second
  ami                    = local.second_windows_ami
  instance_type          = var.instance_type
  subnet_id              = aws_subnet.second_public.id
  key_name               = var.key_pair_names["second"]
  vpc_security_group_ids = [aws_security_group.second_public_win_sg.id]

  tags = {
    Name = "${local.second_name}-Public-Win"
  }
}

# --- Private instances (first private subnet), sourced from the second
# region's own public Windows instance ---

resource "aws_security_group" "second_private_win_sg" {
  provider    = aws.second
  name        = "${local.second_name}-Private-Win-SG"
  vpc_id      = aws_vpc.second.id

  ingress {
    description = "HTTP from the second region's public Windows instance"
    from_port   = 80
    to_port     = 80
    protocol    = "tcp"
    cidr_blocks = ["${aws_instance.second_public_win.public_ip}/32"]
  }

  ingress {
    description = "RDP from the second region's public Windows instance"
    from_port   = 3389
    to_port     = 3389
    protocol    = "tcp"
    cidr_blocks = ["${aws_instance.second_public_win.public_ip}/32"]
  }

  egress {
    from_port   = 0
    to_port     = 0
    protocol    = "-1"
    cidr_blocks = ["0.0.0.0/0"]
  }

  tags = {
    Name = "${local.second_name}-Private-Win-SG"
  }
}

resource "aws_instance" "second_private_win" {
  provider               = aws.second
  ami                    = local.second_windows_ami
  instance_type          = var.instance_type
  subnet_id              = aws_subnet.second_private[0].id
  key_name               = var.key_pair_names["second"]
  vpc_security_group_ids = [aws_security_group.second_private_win_sg.id]

  tags = {
    Name = "${local.second_name}-Private-Win"
  }
}

resource "aws_security_group" "second_private_linux_sg" {
  provider    = aws.second
  name        = "${local.second_name}-Private-Linux-SG"
  vpc_id      = aws_vpc.second.id

  ingress {
    description = "HTTP from the second region's public Windows instance"
    from_port   = 80
    to_port     = 80
    protocol    = "tcp"
    cidr_blocks = ["${aws_instance.second_public_win.public_ip}/32"]
  }

  ingress {
    description = "SSH from the second region's public Windows instance"
    from_port   = 22
    to_port     = 22
    protocol    = "tcp"
    cidr_blocks = ["${aws_instance.second_public_win.public_ip}/32"]
  }

  egress {
    from_port   = 0
    to_port     = 0
    protocol    = "-1"
    cidr_blocks = ["0.0.0.0/0"]
  }

  tags = {
    Name = "${local.second_name}-Private-Linux-SG"
  }
}

resource "aws_instance" "second_private_linux" {
  provider               = aws.second
  ami                    = local.second_linux_ami
  instance_type          = var.instance_type
  subnet_id              = aws_subnet.second_private[0].id
  key_name               = var.key_pair_names["second"]
  vpc_security_group_ids = [aws_security_group.second_private_linux_sg.id]

  tags = {
    Name = "${local.second_name}-Private-Linux"
  }
}
