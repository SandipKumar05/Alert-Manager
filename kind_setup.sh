
## follow the link for kind installation 
# https://kind.sigs.k8s.io/docs/user/quick-start#installation

# create namespace 
kubectl create ns monitoring

helm install prometheus prometheus-community/kube-prometheus-stack --namespace monitoring

kubectl port-forward -n monitoring svc/prometheus-kube-prometheus-prometheus 9090:9090
kubectl port-forward -n monitoring svc/prometheus-grafana 3000:80
kubectl port-forward -n monitoring svc/prometheus-kube-prometheus-alertmanager 9093:9093
kubectl port-forward -n alert-manager svc/alert-manager 5000:80