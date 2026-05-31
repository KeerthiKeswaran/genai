import os
import ollama

def load_context(filename):
    script_dir = os.path.dirname(os.path.abspath(__file__))
    path = os.path.abspath(os.path.join(script_dir, "..", "contexts", filename))
    with open(path, "r", encoding="utf-8") as f:
        return f.read()

def run_evaluation():
    model_name = "tinyllama:latest"
    output_dir = os.path.dirname(os.path.abspath(__file__))

    # Load context files
    try:
        coding_context = load_context("coding_standards.txt")
        schema_context = load_context("schema_rules.txt")
        troubleshoot_context = load_context("troubleshooting_guide.txt")
    except Exception as e:
        print(f"Error loading context files: {e}")
        return

    prompts = {
        "appdev": {
            "context": coding_context,
            "query": (
                "Using the provided AppDev Coding Standards context, write a high-performance Python function "
                "that implements a thread-safe connection pool for a PostgreSQL database. Ensure your code strictly "
                "adheres to the naming conventions, error handling rules, thread safety requirements, and performance "
                "guidelines specified in the context document. Provide only the Python code with minimal explanations."
            )
        },
        "data": {
            "context": schema_context,
            "query": (
                "Based on the provided Database Schema Rules context, write a SQL query to find the top 5 customers "
                "by total spending in the last 30 days, including the number of unique products they bought, sorted "
                "by total spending descending. Make sure to adhere to all indexing guidelines, column qualification, "
                "explicit join rules, and date functions constraints detailed in the context document. Explain the query "
                "performance implications and which indexes from the guide are utilized."
            )
        },
        "devops": {
            "context": troubleshoot_context,
            "query": (
                "Using the DevOps Infrastructure Troubleshooting Guide context, create a Terraform configuration file "
                "to provision an AWS VPC with 2 public subnets, 2 private subnets, an Internet Gateway, and an "
                "Application Load Balancer (ALB) routing traffic to an ECS Fargate service. Make sure your configuration "
                "addresses the security groups ingress/egress rules and route tables routing logic required to prevent the "
                "target group health check and internet access issues highlighted in the troubleshooting guide."
            )
        }
    }

    print(f"Running assignment-2 evaluation for {model_name}...")
    for dept, data in prompts.items():
        print(f"  Querying for {dept}...")
        print(f"  Prompt: {data['query']}")
        try:
            response = ollama.chat(
                model=model_name,
                messages=[
                    {"role": "system", "content": f"Use this reference context to perform the user request:\n\n{data['context']}"},
                    {"role": "user", "content": data['query']}
                ]
            )
            content = response["message"]["content"]
            
            output_file = os.path.join(output_dir, f"tinyllama_{dept}.txt")
            with open(output_file, "w", encoding="utf-8") as f:
                f.write(content)
            print(f"  Saved response to {output_file}")
        except Exception as e:
            print(f"  Error querying {model_name} for {dept}: {e}")

if __name__ == "__main__":
    run_evaluation()
