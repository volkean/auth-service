# auth-service

This is a demo application for experimenting with horizontally auto-scaling architecture on `Kubernetes`.
It counts HTTP requests and scales up when the average number of requests per pod reaches 10.
The count is stored in `Redis`. This is for demonstration purposes only and is not intended for production use.

It uses `Prometheus` and `Prometheus Adapter` to track metrics in accordance with Kubernetes HPA.

You can try it by first running `build` and then `create` commands on Windows and by make targets on Mac and Linux.  

To view the dashboard, wait until all resources are ready and then run:

```shell
kubectl -n kubernetes-dashboard port-forward svc/kubernetes-dashboard-kong-proxy 8443:443
```
and navigate to https://localhost:8443/ using your token created with `kubectl create token demo`  

### Endpoints
We have root("/"), "/login", "/metrics", "/health" endpoints.
After port-forwarding as `kubectl port-forward service/demo --address=0.0.0.0 8000:8000` you can just try these endpoints with curl commands below.
> `$ curl http://localhost:8000/` 
```json
{
  "counter": "1",
  "message": "Hello there!"
}
```

> `$ curl http://localhost:8000/login -F username=demo -F password=demo`
```json
{
  "counter": "2",
  "message": "Hello demo!",
  "token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiJkZW1vIiwiZXhwIjoxNzI0OTM5Nzc2fQ.KugE9zZzVGXfTnvuYD_u82017-Fb9aSQHn4cS0_AY-o"
}
```

### Make a Load Test
To observe up-scaling, continuously flood your cluster with requests. 
```shell
kubectl run --rm -i busybox --image=radial/busyboxplus -- sh -c "for i in \$(seq 1 100); do curl http://demo:8000/login -F username=demo -F password=demo; done"
```

I just made up metrics query to be like rate in the last 1 minute and multipled it by 10 just to make easy to get scaled. You can play with the query as you wish.

> metricsQuery=floor(rate(http_requests_total[1m])*10)

