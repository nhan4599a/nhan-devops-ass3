resource "azurerm_service_plan" "test" {
  name                = "${var.application_type}-${var.resource_type}"
  location            = var.location
  resource_group_name = var.resource_group
  os_type             = "Windows"
  sku_name            = "F1"
}

resource "azurerm_windows_web_app" "test" {
  name                = "${var.application_type}-${var.resource_type}"
  location            = var.location
  resource_group_name = var.resource_group
  service_plan_id     = azurerm_service_plan.test.id

  app_settings = {
    "WEBSITE_RUN_FROM_PACKAGE" = 0
  }
  site_config {
    always_on = false
  }
  lifecycle {
    ignore_changes = [
      logs,
      tags
    ]
  }
}

resource "azurerm_monitor_action_group" "test" {
  name = "${var.application_type}-action_group"
  resource_group_name = var.resource_group
  short_name = "${var.application_type}-action_group"

  email_receiver {
    name = "Nhan4599"
    email_address = "nhan0385790927@gmail.com"
  }
}

resource "azurerm_monitor_metric_alert" "test" {
  name = "${var.application_type}-alert"
  resource_group_name = var.resource_group
  scopes = [azurerm_windows_web_app.test.id]
  description = "Action will be triggered in HTTP status 404"

  criteria {
    metric_namespace = "Microsoft.Web/sites"
    metric_name = "Http4xx"
    aggregation = "Count"
    operator = "GreaterThan"
    threshold = 2
    dimension {
      name = "HttpStatusCode"
      operator = "Include"
      values = ["404"]
    }
  }

  action {
    action_group_id = azurerm_monitor_action_group.test.id
  }

  severity = 2
  enabled = true
}