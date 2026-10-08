---
type: reference
title: Kubernetes Pod Troubleshooting
description: Common troubleshooting steps for Kubernetes pod failures
tags:
  - kubernetes
  - pod
  - troubleshooting
owner: devops
version: 1.0
---

# Kubernetes Pod Troubleshooting

## CrashLoopBackOff

Check pod logs:

```bash
kubectl logs <pod-name>
```

Describe the pod:

```bash
kubectl describe pod <pod-name>
```

Common causes:

- Application startup failure
- Missing environment variables
- Configuration errors

---

## ImagePullBackOff

Describe the pod:

```bash
kubectl describe pod <pod-name>
```

Verify image exists:

- Image repository
- Image tag
- Registry access permissions

---

## Pending Pods

Check pod details:

```bash
kubectl describe pod <pod-name>
```

Common causes:

- Insufficient CPU
- Insufficient memory
- Node selectors
- Taints and tolerations

---

## Pod Status Overview

List all pods:

```bash
kubectl get pods -A
```

List pods with node assignment:

```bash
kubectl get pods -A -o wide
```

Check cluster events:

```bash
kubectl get events -A --sort-by=.metadata.creationTimestamp
```
``