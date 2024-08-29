kubectl create serviceaccount demo
kubectl create clusterrolebinding demo --clusterrole=cluster-admin --serviceaccount=default:demo

helm upgrade --install kubernetes-dashboard kubernetes-dashboard/kubernetes-dashboard --create-namespace --namespace kubernetes-dashboard

helm upgrade --install metrics-server metrics-server/metrics-server --namespace kube-system --set args[0]="--kubelet-insecure-tls"

kubectl apply -f prometheus-config.yaml
kubectl apply -f prometheus-deployment.yaml
kubectl expose deployment prometheus --type=LoadBalancer --port=9090

helm upgrade --install prometheus-adapter prometheus-community/prometheus-adapter --namespace monitoring --create-namespace --set prometheus.url=http://prometheus.default --set logLevel=10 --set rules.external[0].seriesQuery=http_requests_total --set rules.external[0].name.as=http_requests_total --set rules.external[0].resources.template="<<.Resource>>" --set rules.external[0].metricsQuery="floor(rate(http_requests_total[1m])*10)"

kubectl create deployment redis --image=redis:alpine --port=6379
kubectl expose deployment redis --type=LoadBalancer --port=6379

kubectl create deployment demo --image=demo:0.1.2 --port=8000
kubectl expose deployment demo --type=LoadBalancer --port=8000
kubectl apply -f hpa-demo.yaml
