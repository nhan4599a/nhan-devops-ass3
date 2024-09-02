# Azure GUIDS
variable "subscription_id" {}
variable "client_id" {}
variable "client_secret" {}
variable "tenant_id" {}

# Resource Group/Location
variable "location" {}
variable "resource_group_name" {}
variable "application_type" {}

# Network
variable virtual_network_name {}
variable address_prefix {}
variable address_space {}
variable packer_image {}
variable admin_password {}
variable "az_devops_pat" {}
variable "az_devops_env" {}
variable "az_devops_org" {}
variable "az_devops_proj" {}