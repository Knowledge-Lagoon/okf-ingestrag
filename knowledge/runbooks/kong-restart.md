---
type: runbook
title: Kong Restart
description: Procedure to restart Kong deployment in Kubernetes
tags:
  - kong
  - restart
  - kubernetes
owner: devops
version: 1.0
---

# Kong Restart

## Restart Deployment

```bash
kubectl rollout restart deployment kong -n kong