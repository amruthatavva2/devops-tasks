# VPC — Networking

A VPC is an isolated virtual network defined by a CIDR range. Subnets divide it by Availability Zone; route tables choose traffic paths. An Internet Gateway enables public internet routing; a NAT Gateway enables private-subnet outbound access. Security Groups are stateful instance firewalls; Network ACLs are stateless subnet filters. Put public load balancers in public subnets and databases/private workloads in private subnets.
