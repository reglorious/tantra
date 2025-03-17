import os
import json
import pandas as pd

def read_json_files(directory):
    all_data = []
    
    # Recursively find all JSON files in the directory
    for root, _, files in os.walk(directory):
        for filename in files:
            if filename.endswith(".json"):  # Process only JSON files
                file_path = os.path.join(root, filename)
                with open(file_path, 'r', encoding='utf-8') as file:
                    try:
                        data = json.load(file)  # Load JSON data
                        if isinstance(data, list):  # Ensure it's a list
                            all_data.extend(data)
                        else:
                            print(f"Warning: {filename} does not contain a JSON array.")
                    except json.JSONDecodeError as e:
                        print(f"Error reading {filename}: {e}")
    
    # Create a Pandas DataFrame from the collected data
    df = pd.DataFrame(all_data)
    return df
# Example usage
directory_path = "../dataset"  # Replace with your actual directory
threats_df = read_json_files(directory_path)

# Display the DataFrame
print(threats_df.shape)

replacements = {
    'AWS API Gateway / AWS WAF': 'AWS API Gateway',
    'AWS API GatewayV2' : 'AWS API Gateway',
    'AWS Application Load Balancer (ALB)' : 'AWS Application Load Balancer',
    'AWS AmazonMQ': 'AWS Amazon MQ',
    'AWS Certificate Manager (ACM)': 'AWS Certificate Manager',
    'AWS Certificate Manager (ACM) PCA': 'AWS Certificate Manager',
    'AWS Certificate Manager Private CA': 'AWS Certificate Manager',
    'AWS CloudTrail / Amazon CloudWatch':'AWS CloudTrail',
    'AWS Database Migration Service (DMS)':'AWS Database Migration Service',
    'AWS Elastic Load Balancing':'AWS Elastic Load Balancing',
    'AWS IAM / AWS KMS':'AWS IAM',
    'AWS Identity and Access Management':'AWS IAM',
    'AWS Identity and Access Management (IAM)':'AWS IAM',
    'AWS Lambda / AWS PrivateLink':'AWS Lambda',
    'AWS Key Management Service (KMS)':'AWS KMS',
    'AWS Security Groups':'AWS Security Group',
    'AWS Systems Manager (SSM)':'AWS Systems Manager',
    'AWS IAM Identity Center (SSO)':'AWS IAM',
    'AWS Kinesis Video Streams':'AWS Kinesis',
    'AWS OpenSearch Service':'AWS OpenSearch',
    'AWS Redshift':'AWS RedShift',
    'AWS Sagemaker':'AWS SageMaker',
    'AWS Transfer Family':'AWS Transfer',
    'AWS WAF / Elastic Load Balancing':'AWS WAF',
    'AWS WAF Regional':'AWS WAF',
    'AWS WAFv2':'AWS WAF',
    'AWS Web Application Firewall (WAF)':'AWS WAF',
    'AWS Database Migration Service':'AWS DMS',
    'AWS Load Balancer':'AWS Elastic Load Balancing',
    'AWS LB':'AWS Elastic Load Balancing',
    'AWS VPC / AWS EC2':'AWS VPC',
    'AWS EC2 Auto Scaling':'AWS EC2',
    'AWS EC2 Security Groups':'AWS EC2',
    'AWS Elasticsearch/OpenSearch':'AWS Elasticsearch',
    'Elastic Load Balancing':'AWS Elastic Load Balancing',
    'AWS VPC Security Group':'AWS Security Group',
    'AWS AWS MQ':'AWS MQ',
    'AWS API Gateway / AWS PrivateLink':'AWS API Gateway',
    
}

threats_df["Service"] = threats_df["Service"].str.replace("Amazon", "AWS", regex=False)
threats_df["Service"] = threats_df["Service"].replace(replacements)
threats_df.sort_values(by=["Service"])

set(threats_df["Service"].to_list())

threats_df["Service"].value_counts().to_dict()

threats_df.to_json("aws_full_dataset.json", orient="records", indent=4,force_ascii=False)
