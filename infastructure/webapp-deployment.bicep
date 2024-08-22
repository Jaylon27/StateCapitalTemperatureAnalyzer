@description('Generate a Suffix based on the Resource Group ID')
param suffix string = uniqueString(resourceGroup().id)

@description('Use the Resource Group Location')
param location string = resourceGroup().location

resource acr 'Microsoft.ContainerRegistry/registries@2021-09-01' existing = {
  name: 'azurecr${suffix}'
}

resource appServicePlan 'Microsoft.Web/serverfarms@2022-03-01' = {
  name: 'asp-${suffix}'
  location: location
  kind: 'linux'
  properties: {
    reserved: true
  }
  sku: {
    name: 'B1'  // Change this to another SKU if needed, e.g., 'B2', 'P1v2'
  }
}

resource webApp 'Microsoft.Web/sites@2022-03-01' = {
  name: 'app-${suffix}'
  location: location
  tags: {}
  properties: {
    siteConfig: {
      acrUseManagedIdentityCreds: true
      appSettings: [
        {
          name: 'PYTHON_VERSION'
          value: '3.12' 
        }
        {
          name: 'DASH_ENV'
          value: 'Docker'
        }
        {
          name: 'PORT'
          value: '8050'
        }
      ]
      linuxFxVersion: 'DOCKER|azurecrd4h36xqh4cp46.azurecr.io/weatherapp:latest'
    }
    serverFarmId: appServicePlan.id
  }
  identity: {
    type: 'SystemAssigned'
  }
}
