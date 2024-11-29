# GitOps-Driven-Python-Application-Deployment

Commands to Apply Terraform:

bash
Copy code
terraform init
terraform plan
terraform apply


Install ArgoCD
Commands:

kubectl create namespace argocd
kubectl apply -n argocd -f https://raw.githubusercontent.com/argoproj/argo-cd/stable/manifests/install.yaml

Command to Apply ArgoCD Application:

kubectl apply -f Application.yaml


Monitoring and Metrics
1. Deploy Prometheus and Grafana
Commands:

helm install prometheus prometheus-community/prometheus
helm install grafana grafana/grafana

Prometheus Configurations:

Use a ServiceMonitor to scrape /metrics endpoint from the Flask app.

Testing and Rollbacks
1. Test the Application
Push updates to the repository and verify the deployment through ArgoCD.
2. Simulate Rollback
Use ArgoCD CLI to rollback to a previous revision:

argocd app rollback flask-app --revision <revision>
