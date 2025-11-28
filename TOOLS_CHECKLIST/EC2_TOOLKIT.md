# ✅ **EC2 Tools Roadmap (MCP Server)**

A complete roadmap of all EC2-related tools planned for the AWS-MCP server, including priority-based implementation order and progress tracking.

This roadmap covers **every actionable EC2 operation available via the boto3 EC2 API**, organized into priorities for structured development.

---

# 🚀 **PHASE 1 — TOP PRIORITY (Core EC2 Interactions)**

These tools provide essential EC2 control.
💯 **Implement these first before building advanced automation or agents.**

## ✅ **1. Instance Listing & Details**

| Tool                         | Description                         | Status    |
| ---------------------------- | ----------------------------------- | --------- |
| `aws.list_ec2_instances`     | List all EC2 instances in a region  | ✅ DONE    |
| `aws.get_instance_details`   | Detailed info for a single instance | ⬜ Pending |
| `aws.get_instance_status`    | Health + system status              | ⬜ Pending |
| `aws.list_running_instances` | List only running instances         | ⬜ Pending |
| `aws.list_instances_by_tag`  | Filter by tag key/value             | ⬜ Pending |

---

## ✅ **2. Instance Lifecycle (High Use-Case)**

| Tool                       | Description   | Status    |
| -------------------------- | ------------- | --------- |
| `aws.start_instance`       | Start EC2     | ⬜ Pending |
| `aws.stop_instance`        | Stop EC2      | ⬜ Pending |
| `aws.reboot_instance`      | Reboot EC2    | ⬜ Pending |
| `aws.terminate_instance`   | Terminate EC2 | ⬜ Pending |
| `aws.hard_reboot_instance` | Forced reboot | ⬜ Pending |

---

## ✅ **3. Instance Creation (Critical for automation)**

| Tool                          | Description                            | Status    |
| ----------------------------- | -------------------------------------- | --------- |
| `aws.create_instance`         | Launch EC2 with parameters             | ⬜ Pending |
| `aws.create_instance_minimal` | Quick-create: instance_type + AMI only | ⬜ Pending |
| `aws.create_spot_instance`    | Create spot EC2                        | ⬜ Pending |
| `aws.cancel_spot_request`     | Cancel spot request                    | ⬜ Pending |

---

# ⚡ **PHASE 2 — IMPORTANT (Useful for real workflows)**

These come after core lifecycle functionality.

## 🔧 **4. Instance Configuration & Updates**

| Tool                            | Description               | Status    |
| ------------------------------- | ------------------------- | --------- |
| `aws.change_instance_type`      | t2.micro → t3.small       | ⬜ Pending |
| `aws.update_user_data`          | Replace/modify user-data  | ⬜ Pending |
| `aws.modify_instance_attribute` | Generic modify (umbrella) | ⬜ Pending |
| `aws.enable_api_termination`    | Allow termination         | ⬜ Pending |
| `aws.disable_api_termination`   | Prevent termination       | ⬜ Pending |

---

## 🏷 **5. Tags Management (Highly used)**

| Tool                     | Description          | Status    |
| ------------------------ | -------------------- | --------- |
| `aws.list_instance_tags` | Show tags            | ⬜ Pending |
| `aws.add_tags`           | Add/replace tags     | ⬜ Pending |
| `aws.remove_tags`        | Remove specific tags | ⬜ Pending |

---

## 📡 **6. Networking (EC2-scope only)**

(No VPC, no SG — those are separate categories)

| Tool                          | Description               | Status    |
| ----------------------------- | ------------------------- | --------- |
| `aws.describe_addresses`      | List Elastic IPs          | ⬜ Pending |
| `aws.allocate_elastic_ip`     | Create new EIP            | ⬜ Pending |
| `aws.release_elastic_ip`      | Delete EIP                | ⬜ Pending |
| `aws.associate_elastic_ip`    | Attach EIP to instance    | ⬜ Pending |
| `aws.disassociate_elastic_ip` | Remove EIP                | ⬜ Pending |
| `aws.assign_private_ips`      | Add secondary private IPs | ⬜ Pending |
| `aws.unassign_private_ips`    | Remove private IPs        | ⬜ Pending |

---

# ⚙️ **PHASE 3 — ADVANCED EC2 MANAGEMENT**

Once core features work perfectly, build these.

## 🖼 **7. AMI Operations**

| Tool                   | Description         | Status    |
| ---------------------- | ------------------- | --------- |
| `aws.describe_images`  | List AMIs           | ⬜ Pending |
| `aws.create_image`     | Create AMI from EC2 | ⬜ Pending |
| `aws.deregister_image` | Delete AMI          | ⬜ Pending |

---

## 💾 **8. Volume & Storage Operations**

| Tool                         | Description                       | Status    |
| ---------------------------- | --------------------------------- | --------- |
| `aws.describe_volumes`       | List volumes attached to instance | ⬜ Pending |
| `aws.modify_volume`          | Resize or change type             | ⬜ Pending |
| `aws.create_volume_snapshot` | Snapshot root volume              | ⬜ Pending |
| `aws.describe_snapshots`     | List snapshots                    | ⬜ Pending |
| `aws.delete_snapshot`        | Delete snapshot                   | ⬜ Pending |

---

## 🖥 **9. Metadata & Monitoring**

| Tool                              | Description                | Status    |
| --------------------------------- | -------------------------- | --------- |
| `aws.get_console_output`          | Instance console logs      | ⬜ Pending |
| `aws.enable_detailed_monitoring`  | Enable CloudWatch detailed | ⬜ Pending |
| `aws.disable_detailed_monitoring` | Disable CW detailed        | ⬜ Pending |
| `aws.get_instance_metadata`       | IMDSv2 metadata            | ⬜ Pending |

---

# 🧪 **PHASE 4 — SMART/AI ENHANCED TOOLS**

These make your project **unique** and differentiate it from plain wrappers.

## 🤖 **10. Intelligent EC2 Tools**

| Tool                           | Description                             | Status    |
| ------------------------------ | --------------------------------------- | --------- |
| `aws.recommend_instance_type`  | Suggest instance type based on workload | ⬜ Pending |
| `aws.estimate_ec2_cost`        | Estimate cost per hour/month            | ⬜ Pending |
| `aws.find_best_price_instance` | Compare across families                 | ⬜ Pending |
| `aws.explain_instance`         | Human-readable instance summary         | ⬜ Pending |
| `aws.plan_instance_creation`   | Convert natural language → EC2 spec     | ⬜ Pending |

---

# 🚀 **PROJECT MILESTONES**

## **Milestone 1 (Day 1–2)**

✔ Basic MCP server
✔ List EC2 instances
✔ Start/stop/terminate
➡ **Goal: Complete PHASE 1**

## **Milestone 2 (Day 3–5)**

✔ Tag tools
✔ EIP tools
✔ Change instance type
➡ **Goal: Complete PHASE 2**

## **Milestone 3 (Day 6–10)**

✔ AMIs
✔ Volumes
✔ Metadata
➡ **Goal: Complete PHASE 3**

## **Milestone 4 (Day 11–14)**

✔ Intelligent tools
✔ Auto infra planning
➡ **Goal: Fully agentic EC2 assistant**

---

# 🌟 **Final Product Vision**

Your MCP server becomes a **complete EC2 automation suite** that lets users do:

> “Create a GPU instance for training under ₹10/hour”
>
> “Stop all unused instances”
>
> “Create an AMI, resize the volume, attach EIP, and reboot”

All via natural language.