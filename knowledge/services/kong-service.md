---
type: service
title: Kong API Gateway
description: Service catalog entry for Kong API Gateway
tags:
  - kong
  - api-gateway
  - ingress
owner: platform-team
version: 1.0
---

# Kong API Gateway

## Purpose

Kong provides API gateway and ingress capabilities for applications running on Kubernetes.

## Dependencies

- Amazon EKS
- Route53
- ACM Certificates

## Related Runbooks

- Kong Restart
- Kong Upgrade
- Kong Troubleshooting

## Monitoring

- Prometheus
- Grafana

## Key Commands

Check Kong pods:

```bash
kubectl get pods -n kong
```

View Kong logs:

```bash
kubectl logs -n kong <pod-name>
```

Restart Kong deployment:

```bash
kubectl rollout restart deployment kong -n kong
```