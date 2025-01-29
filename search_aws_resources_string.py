import boto3

# 🔹 Ask user for the search string
search_string = input("Enter the search string: ").strip()

# ✅ Search S3 Buckets
def search_s3():
    s3 = boto3.client("s3")
    buckets = s3.list_buckets()["Buckets"]
    return [f"arn:aws:s3:::{b['Name']}" for b in buckets if search_string in b["Name"]]

# ✅ Search CloudFront Distributions (by Domain Name, ID, and CNAME)
def search_cloudfront():
    cloudfront = boto3.client("cloudfront")
    distributions = cloudfront.list_distributions()
    matching_distributions = []

    if "DistributionList" in distributions and "Items" in distributions["DistributionList"]:
        for dist in distributions["DistributionList"]["Items"]:
            domain_match = search_string in dist["DomainName"]
            id_match = search_string in dist["Id"]
            cname_match = any(search_string in cname for cname in dist.get("Aliases", {}).get("Items", []))

            if domain_match or id_match or cname_match:
                matching_distributions.append({
                    "ARN": dist["ARN"],
                    "ID": dist["Id"],
                    "Domain": dist["DomainName"],
                    "CNAMEs": dist.get("Aliases", {}).get("Items", [])
                })

    return matching_distributions

# ✅ Search Lambda Functions
def search_lambda():
    lambda_client = boto3.client("lambda")
    functions = lambda_client.list_functions()["Functions"]
    return [f["FunctionArn"] for f in functions if search_string in f["FunctionName"]]

# ✅ Search EC2 Instances (by Name Tag)
def search_ec2():
    ec2 = boto3.client("ec2")
    instances = ec2.describe_instances()["Reservations"]
    matching_instances = []

    for reservation in instances:
        for instance in reservation["Instances"]:
            for tag in instance.get("Tags", []):
                if tag["Key"] == "Name" and search_string in tag["Value"]:
                    matching_instances.append(f"arn:aws:ec2:{boto3.session.Session().region_name}:{boto3.client('sts').get_caller_identity()['Account']}:instance/{instance['InstanceId']}")

    return matching_instances

# ✅ Search RDS Databases (by DB Instance Identifier)
def search_rds():
    rds = boto3.client("rds")
    instances = rds.describe_db_instances()["DBInstances"]
    return [db["DBInstanceArn"] for db in instances if search_string in db["DBInstanceIdentifier"]]

# ✅ Search DynamoDB Tables (by Table Name)
def search_dynamodb():
    dynamodb = boto3.client("dynamodb")
    tables = dynamodb.list_tables()["TableNames"]
    return [f"arn:aws:dynamodb:{boto3.session.Session().region_name}:{boto3.client('sts').get_caller_identity()['Account']}:table/{table}" for table in tables if search_string in table]

# ✅ Search IAM Roles (by Role Name)
def search_iam_roles():
    iam = boto3.client("iam")
    roles = iam.list_roles()["Roles"]
    return [role["Arn"] for role in roles if search_string in role["RoleName"]]

# ✅ Search CloudFormation Stacks (by Stack Name)
def search_cloudformation():
    cf = boto3.client("cloudformation")
    stacks = cf.list_stacks(StackStatusFilter=["CREATE_COMPLETE", "UPDATE_COMPLETE"])["StackSummaries"]
    return [stack["StackId"] for stack in stacks if search_string in stack["StackName"]]

# 🔹 Run searches and print results
if __name__ == "__main__":
    print("\n🔍 Searching AWS resources for:", search_string)

    s3_results = search_s3()
    cloudfront_results = search_cloudfront()
    lambda_results = search_lambda()
    ec2_results = search_ec2()
    rds_results = search_rds()
    dynamodb_results = search_dynamodb()
    iam_results = search_iam_roles()
    cloudformation_results = search_cloudformation()

    print("\n🪣 Matching S3 Buckets:")
    print("\n".join(s3_results) if s3_results else "No matches found.")

    print("\n🌍 Matching CloudFront Distributions:")
    if cloudfront_results:
        for result in cloudfront_results:
            print(f"🔹 ARN: {result['ARN']}\n   ID: {result['ID']}\n   Domain: {result['Domain']}")
            if result["CNAMEs"]:
                print(f"   CNAMEs: {', '.join(result['CNAMEs'])}")
            print()
    else:
        print("No matches found.")

    print("\n⚡ Matching Lambda Functions:")
    print("\n".join(lambda_results) if lambda_results else "No matches found.")

    print("\n🖥️ Matching EC2 Instances:")
    print("\n".join(ec2_results) if ec2_results else "No matches found.")

    print("\n💾 Matching RDS Databases:")
    print("\n".join(rds_results) if rds_results else "No matches found.")

    print("\n📊 Matching DynamoDB Tables:")
    print("\n".join(dynamodb_results) if dynamodb_results else "No matches found.")

    print("\n🔑 Matching IAM Roles:")
    print("\n".join(iam_results) if iam_results else "No matches found.")

    print("\n📦 Matching CloudFormation Stacks:")
    print("\n".join(cloudformation_results) if cloudformation_results else "No matches found.")
