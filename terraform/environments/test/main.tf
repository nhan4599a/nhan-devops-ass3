terraform {
  required_providers {
    azurerm = {
        source = "hashicorp/azurerm",
        version = "~> 3.0.2"
    }
  }

  required_version = ">= 1.1.0"
}
provider "azurerm" {
  tenant_id       = "${var.tenant_id}"
  subscription_id = "${var.subscription_id}"
  client_id       = "${var.client_id}"
  client_secret   = "${var.client_secret}"
  features {}
}

# module "resource_group" {
#   source               = "../../modules/resource_group"
#   resource_group       = "${var.resource_group_name}"
#   location             = "${var.location}"
# }
module "network" {
  source               = "../../modules/network"
  address_space        = "${var.address_space}"
  location             = "${var.location}"
  virtual_network_name = "${var.virtual_network_name}"
  application_type     = "${var.application_type}"
  resource_type        = "NET"
  resource_group       = "${var.resource_group_name}"
  address_prefix  = "${var.address_prefix}"
}

module "nsg" {
  source           = "../../modules/network_security_group"
  location         = "${var.location}"
  application_type = "${var.application_type}"
  resource_type    = "NSG"
  resource_group   = "${var.resource_group_name}"
  subnet_id        = "${module.network.subnet_id}"
  address_prefix = "${var.address_prefix}"
}
module "appservice" {
  source           = "../../modules/appservice"
  location         = "${var.location}"
  application_type = "${var.application_type}"
  resource_type    = "AppService"
  resource_group   = "${var.resource_group_name}"
}
module "publicip" {
  source           = "../../modules/publicip"
  location         = "${var.location}"
  application_type = "${var.application_type}"
  resource_type    = "publicip"
  resource_group   = "${var.resource_group_name}"
}

module "vm" {
  source               = "../../modules/vm"
  location             = "${var.location}"
  resource_group       = "${var.resource_group_name}"
  resource_type        = "vm"

  admin_username       = "azureuser"
  subnet_id_test       = module.network.subnet_id_test
  instance_ids         = module.publicip.public_ip_address_id
  packer_image         = var.packer_image_id
  admin_password      = var.admin_password
  az_devops_org = var.az_devops_org
  az_devops_env = var.az_devops_env
  az_devops_proj = var.az_devops_proj
  az_devops_pat = var.az_devops_pat
}