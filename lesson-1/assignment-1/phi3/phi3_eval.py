import os
import ollama

def run_evaluation():
    model_name = "phi3:latest"
    output_dir = os.path.dirname(os.path.abspath(__file__))

    prompts = {
        "appdev": (
            "Write a high-performance Python function that implements a thread-safe connection pool "
            "for a PostgreSQL database, including connection recycling, validation, and graceful shutdown. "
            "Provide only the Python code with minimal explanations."
        ),
        "data": (
            "Given a database schema with tables: `orders` (order_id, customer_id, order_date, total_amount) "
            "and `order_items` (item_id, order_id, product_id, quantity, unit_price). Write a SQL query "
            "to find the top 5 customers by total spending in the last 30 days, including the number of "
            "unique products they bought, sorted by total spending descending. Also, explain the query "
            "performance implications (e.g. indexes needed)."
        ),
        "devops": (
            "Create a Terraform configuration file to provision an AWS VPC with 2 public subnets, "
            "2 private subnets, an Internet Gateway, and an Application Load Balancer (ALB) routing traffic "
            "to an ECS Fargate service. Include appropriate security groups."
        )
    }

    print(f"Running evaluation for {model_name}...")
    for dept, prompt in prompts.items():
        print(f"  Querying for {dept}...")
        try:
            response = ollama.chat(
                model=model_name,
                messages=[{"role": "user", "content": prompt}]
            )
            content = response["message"]["content"]
            
            output_file = os.path.join(output_dir, f"phi3_{dept}.txt")
            with open(output_file, "w", encoding="utf-8") as f:
                f.write(content)
            print(f"  Saved response to {output_file}")
        except Exception as e:
            print(f"  Error querying {model_name} for {dept}: {e}")

if __name__ == "__main__":
    run_evaluation()
