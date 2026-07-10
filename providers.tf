terraform {
  required_providers {
    aws = {
      source  = "hashicorp/aws"
      version = "~> 5.0"
    }
  }
}

# Primary region provider (no alias = default provider)
provider "aws" {
  region     = var.regions["primary"]
  access_key = var.Key
  secret_key = var.Secret
  token      = var.Token
}

# Second region provider (aliased providers do not inherit from the default, so
# credentials must be repeated here)
provider "aws" {
  alias      = "second"
  region     = var.regions["second"]
  access_key = var.Key
  secret_key = var.Secret
  token      = var.Token
}
