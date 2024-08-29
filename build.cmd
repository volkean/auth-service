docker build -t demo:0.1.2 .
kind create cluster --name demo
kind load docker-image demo:0.1.2 --name demo