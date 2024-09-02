resource "azurerm_network_interface" "staging" {
  name                = "nic0"
  location            = var.location
  resource_group_name = var.resource_group

  ip_configuration {
    name                          = "internal"
    subnet_id                     = var.subnet_id_test
    private_ip_address_allocation = "Dynamic"
    public_ip_address_id          = var.instance_ids
  }
}

resource "azurerm_linux_virtual_machine" "test" {
  name                            = "vm0"
  location                        = var.location
  resource_group_name             = var.resource_group
  size                            = "Standard_B1s"
  admin_username                  = var.admin_username
  admin_password                  = var.admin_password
  source_image_id                 = var.packer_image
  disable_password_authentication = true
  
  network_interface_ids = [
    azurerm_network_interface.test.id
  ]

  os_disk {
    storage_account_type = "Standard_LRS"
    caching              = "ReadWrite"
  }
}

resource "azurerm_virtual_machine_extension" "test" {
  name = "vm0-extension"
  virtual_machine_id = azurerm_linux_virtual_machine.test.id
  publisher = "Microsoft.Azure.Extensions"
  type = "CustomScript"
  type_handler_version = "2.0"
  settings = <<SETTINGS
  {
    "commandToExecute": "mkdir azagent;cd azagent;curl -fkSL -o vstsagent.tar.gz https://vstsagentpackage.azureedge.net/agent/3.243.1/vsts-agent-linux-x64-3.243.1.tar.gz;tar -zxvf vstsagent.tar.gz; if [ -x "$(command -v systemctl)" ]; then ./config.sh --environment --environmentname "${var.az_devops_env}" --acceptteeeula --agent $HOSTNAME --url https://dev.azure.com/${var.az_devops_org}/ --work _work --projectname '${var.az_devops_proj}' --auth PAT --token ${var.az_devops_pat} --runasservice; sudo ./svc.sh install; sudo ./svc.sh start; else ./config.sh --environment --environmentname "${var.az_devops_env}" --acceptteeeula --agent $HOSTNAME --url https://dev.azure.com/${var.az_devops_org}/ --work _work --projectname '${var.az_devops_proj}' --auth PAT --token ${var.az_devops_pat}; ./run.sh; fi"
  }
  SETTINGS
}