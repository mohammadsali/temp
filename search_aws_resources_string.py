import boto3

# 🔹 Define the search string
search_string = "my-search-string"  # Change this to your search term

# ✅ Search S3 Buckets
def search_s3():
    s3 = boto3.client("s3")
    buckets = s3.list_buckets()["Buckets"]
    matching_buckets = [f"arn:aws:s3:::{b['Name']}" for b in buckets if search_string in b["Name"]]
    return matching_buckets

# ✅ Search CloudFront Distributions
def search_cloudfront():
    cloudfront = boto3.client("cloudfront")
    distributions = cloudfront.list_distributions()
    matching_distributions = []

    if "DistributionList" in distributions and "Items" in distributions["DistributionList"]:
        for dist in distributions["DistributionList"]["Items"]:
            if search_string in dist["DomainName"] or search_string in dist["Id"]:
                matching_distributions.append(dist["ARN"])

    return matching_distributions

# ✅ Search Lambda Functions
def search_lambda():
    lambda_client = boto3.client("lambda")
    functions = lambda_client.list_functions()["Functions"]
    matching_functions = [f["FunctionArn"] for f in functions if search_string in f["FunctionName"]]
    return matching_functions

# 🔹 Run searches and print results
if __name__ == "__main__":
    print("🔍 Searching AWS resources for:", search_string)

    s3_results = search_s3()
    cloudfront_results = search_cloudfront()
    lambda_results = search_lambda()

    print("\n🪣 Matching S3 Buckets:")
    print("\n".join(s3_results) if s3_results else "No matches found.")

    print("\n🌍 Matching CloudFront Distributions:")
    print("\n".join(cloudfront_results) if cloudfront_results else "No matches found.")

    print("\n⚡ Matching Lambda Functions:")
    print("\n".join(lambda_results) if lambda_results else "No matches found.")
