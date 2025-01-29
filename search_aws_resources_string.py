import boto3

# 🔹 Define the search string
search_string = "my-search-string"  # Change this to your search term

# ✅ Search S3 Buckets
def search_s3():
    s3 = boto3.client("s3")
    buckets = s3.list_buckets()["Buckets"]
    matching_buckets = [f"arn:aws:s3:::{b['Name']}" for b in buckets if search_string in b["Name"]]
    return matching_buckets

# ✅ Search CloudFront Distributions (by Domain Name, ID, and CNAME)
def search_cloudfront():
    cloudfront = boto3.client("cloudfront")
    distributions = cloudfront.list_distributions()
    matching_distributions = []

    if "DistributionList" in distributions and "Items" in distributions["DistributionList"]:
        for dist in distributions["DistributionList"]["Items"]:
            domain_match = search_string in dist["DomainName"]
            id_match = search_string in dist["Id"]
            cname_match = False

            if "Aliases" in dist and "Items" in dist["Aliases"]:
                for cname in dist["Aliases"]["Items"]:
                    if search_string in cname:
                        cname_match = True
                        break  # Stop checking if a match is found

            if domain_match or id_match or cname_match:
                matching_distributions.append({
                    "ARN": dist["ARN"],
                    "ID": dist["Id"],
                    "Domain": dist["DomainName"],
                    "CNAMEs": dist["Aliases"]["Items"] if "Aliases" in dist else []
                })

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
