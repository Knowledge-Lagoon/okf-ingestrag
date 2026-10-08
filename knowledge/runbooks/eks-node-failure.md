---
type: runbook
title: EKS Node Failure
description: Troubleshooting failed EKS worker nodes
tags:
  - eks
  - kubernetes
  - node
owner: devops
version: 1.0
---

# EKS Node Failure

## Symptoms

- Nodes not ready
- Pods stuck in Pending
- Cluster autoscaler not scaling

## Investigation

1. Check node status

```bash
kubectl get nodes