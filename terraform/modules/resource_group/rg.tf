resource "azurerm_resource_group" "staging" {
  name     = "${var.resource_group}"
  location = "${var.location}"
}