provider "kubernetes" {
  config_path = "~/.kube/config"
}

resource "kubernetes_namespace" "gitops" {
  metadata {
    name = "gitops-namespace"
  }
}

resource "kubernetes_deployment" "flask_app" {
  metadata {
    name = "flask-app"
    namespace = kubernetes_namespace.gitops.metadata[0].name
  }

  spec {
    replicas = 2

    selector {
      match_labels = {
        app = "flask-app"
      }
    }

    template {
      metadata {
        labels = {
          app = "flask-app"
        }
      }

      spec {
        container {
          image = "salmaborchani/flask-app:latest"  # Use unique tag instead of 'latest' in production
          name  = "flask-container"
          image_pull_policy = "Always"  # Ensure Kubernetes always pulls the latest image

          port {
            container_port = 5000
          }
        }
      }
    }
  }
}
