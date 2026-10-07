# IAM — Governance

IAM controls AWS authentication and authorization. **Users** represent people/workloads, **groups** collect users, **roles** provide assumable temporary permissions, and **policies** define allowed/denied actions on resources. Follow least privilege, use roles instead of long-lived keys, require MFA, rotate/remove unused credentials, and review CloudTrail/access reports. Typical uses: developer access, EC2 instance roles, and cross-account access.
