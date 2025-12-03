from typing import Optional, List, Dict, Any, Literal
from pydantic import BaseModel

class EC2DispatcherParams(BaseModel):
    # ----------------------
    # CORE ACTION FIELD
    # ----------------------
    action: Literal[
        # AMI Actions
        "create_ami", "describe_images", "deregister_ami", "get_latest_ami",

        # INSTANCE CREATION
        "create_instance", "create_instance_minimal", "create_spot_instance",

        # INSTANCE LIFECYCLE
        "start_instance", "stop_instance", "reboot_instance", 
        "hard_reboot_instance", "terminate_instance",

        # INSTANCE INFO
        "list_ec2_instances", "get_instance_details",
        "get_instance_status", "list_running_instances",
        "list_instances_by_tag",

        # SPOT REQUESTS
        "list_spot_requests", "get_spot_request_details", "cancel_spot_request",

        # SSH
        "generate_instance_ssh_instruction",

        # KEYPAIRS
        "create_keypair", "delete_keypair", "list_keypairs",

        # LAUNCH TEMPLATES
        "create_launch_template", "create_launch_template_version",
        "describe_launch_template", "delete_launch_template",
        "list_launch_templates", "launch_from_template",

        # METADATA
        "get_user_data", "describe_metadata_options", "modify_metadata_options",

        # SECURITY GROUPS
        "create_security_group", "delete_security_group",
        "authorize_security_group_rules", "revoke_security_group_rules",
        "describe_security_group", "list_security_groups",

        # PRICING
        "get_ondemand_price", "get_spot_price_history",
        "estimate_instance_cost",
    ]

    # ----------------------
    # COMMON FIELDS
    # ----------------------
    region: Optional[str] = None
    instance_id: Optional[str] = None
    image_id: Optional[str] = None
    instance_ids: Optional[List[str]] = None

    # ----------------------
    # AMI FIELDS
    # ----------------------
    name: Optional[str] = None
    no_reboot: Optional[bool] = True
    description: Optional[str] = None
    tags: Optional[Dict[str, str]] = None
    owners: Optional[List[str]] = None
    image_ids_filter: Optional[List[str]] = None
    filters: Optional[List[Dict[str, Any]]] = None
    os_type: Optional[str] = None
    architecture: Optional[str] = "x86_64"

    # ----------------------
    # INSTANCE CREATION
    # ----------------------
    ImageId: Optional[str] = None
    InstanceType: Optional[str] = None
    MinCount: Optional[int] = 1
    MaxCount: Optional[int] = 1
    KeyName: Optional[str] = None
    SubnetId: Optional[str] = None
    SecurityGroupIds: Optional[List[str]] = None
    BlockDeviceMappings: Optional[List[Dict[str, Any]]] = None
    NetworkInterfaces: Optional[List[Dict[str, Any]]] = None
    TagSpecifications: Optional[List[Dict[str, Any]]] = None
    IamInstanceProfile: Optional[Dict[str, str]] = None
    MetadataOptions: Optional[Dict[str, Any]] = None
    UserData: Optional[str] = None
    ExtraParams: Optional[Dict[str, Any]] = None
    MaxPrice: Optional[str] = None  # For Spot

    # ----------------------
    # INSTANCE FILTERING
    # ----------------------
    states: Optional[List[str]] = None
    instance_types: Optional[List[str]] = None
    vpc_ids: Optional[List[str]] = None
    subnet_ids: Optional[List[str]] = None
    security_group_ids: Optional[List[str]] = None
    tag_key: Optional[str] = None
    tag_value: Optional[str] = None
    spot_only: Optional[bool] = False
    exclude_spot: Optional[bool] = False
    spot_request_id: Optional[str] = None
    custom_filters: Optional[List[Dict[str, Any]]] = None

    # ----------------------
    # SPOT REQUEST FILTERS
    # ----------------------
    spot_request_ids: Optional[List[str]] = None
    spot_states: Optional[List[str]] = None

    # ----------------------
    # SSH HELPERS
    # ----------------------
    pem_path: Optional[str] = None

    # ----------------------
    # METADATA OPTIONS
    # ----------------------
    http_tokens: Optional[str] = None
    http_endpoint: Optional[str] = None
    http_put_response_hop_limit: Optional[int] = None

    # ----------------------
    # SECURITY GROUPS
    # ----------------------
    group_name: Optional[str] = None
    group_id: Optional[str] = None
    inbound_rules: Optional[List[Any]] = None  # IpPermission objects
    rules: Optional[List[Any]] = None
    vpc_id: Optional[str] = None

    # ----------------------
    # LAUNCH TEMPLATE
    # ----------------------
    LaunchTemplateName: Optional[str] = None
    LaunchTemplateId: Optional[str] = None
    VersionDescription: Optional[str] = None
    Version: Optional[str] = None

    # ----------------------
    # PRICING
    # ----------------------
    instance_type: Optional[str] = None
    operating_system: Optional[str] = None
    hours_per_month: Optional[int] = None
    availability_zone: Optional[str] = None
    start_time: Optional[Any] = None
    end_time: Optional[Any] = None
