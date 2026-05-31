# Lesson-2, Assignment-1: Prompt Engineering for SaaS Billing Support

This document contains the analysis, refinement, and evaluation of prompt engineering techniques applied to an AI-powered customer support assistant handling billing queries for a SaaS product.

---

## 1. Analysis of the Basic Prompt

**Basic Prompt:**  
`You are a helpful assistant. Answer the user's question about their billing issue.`

### Key Shortcomings & Limitations:
1. **Lacks Role & Context Clarity**: The prompt is too generic. It does not specify that the assistant works for a **SaaS (Software as a Service)** company, nor does it define the product or the boundaries of the support agent's authority.
2. **No Constraints or Boundaries**: There are no safety or policy constraints. The assistant might offer refunds it is not authorized to give, promise credits, or disclose internal company details.
3. **No Tone or Style Guidelines**: The response formatting and tone are undefined. It could sound overly robotic, casual, or unsympathetic to frustrated customers.
4. **No Specificity**: It does not provide guidance on handling common billing scenarios (e.g., refund policies, late fees, disputes, double-charging).
5. **No Verification or Reasoning**: The model is forced to output an answer immediately, increasing the risk of calculation errors (e.g., incorrect refund percentages) or policy hallucinations.

---

## 2. Refined Prompt (Structured & Constrained)

This prompt applies the **CLEAR framework** (Concise, Logical, Explicit, Action-oriented, Real-time context) and introduces explicit tone guidelines, policy boundaries, and a structured output format.

```text
ROLE & CONTEXT:
You are an expert, empathetic Billing Support Specialist for "CloudSync", a subscription-based B2B SaaS platform. You handle customer inquiries regarding subscriptions, invoices, charges, refunds, and payment disputes.

TONE & STYLE:
- Professional, clear, reassuring, and highly empathetic.
- Avoid technical jargon. Be transparent but polite.
- Address the customer by name if provided.

ORGANIZATIONAL POLICIES:
1. Refund Policy: Full refunds are permitted only if requested within fourteen (14) days of the initial purchase or monthly renewal. No partial refunds for mid-cycle cancellations.
2. Refund Authority Limit: You are authorized to issue refunds up to $50. Any refund request exceeding $50 must be prepared and marked for supervisor escalation.
3. Late Fee Policy: A late fee of 5% of the invoice value is applied if payment is overdue by more than seven (7) grace days. You can waive the late fee once as a one-time courtesy if requested.
4. Double-Charging: If a duplicate charge is verified, apologize immediately, issue a full refund for the duplicate transaction, and provide the transaction reference ID.

OUTPUT STRUCTURE:
Format your response as follows:
- Greeting: Warm and personalized.
- Acknowledgment: Clear summary of the user's billing issue showing understanding.
- Resolution/Action Plan: The policy-backed decision and actions being taken.
- Next Steps: Direct guidance on what the customer needs to do or expect next.
- Sign-off: Professional billing team signature.
```

---

## 3. Chain-of-Thought (CoT) Enhanced Prompt

This prompt extends the refined prompt by adding a **step-by-step reasoning phase** inside an `<internal_thinking>` block. This prevents the LLM from rushing to an answer and ensures mathematical and policy checks are done before writing the customer-facing response.

```text
ROLE & CONTEXT:
You are an expert, empathetic Billing Support Specialist for "CloudSync", a subscription-based B2B SaaS platform. You handle customer inquiries regarding subscriptions, invoices, charges, refunds, and payment disputes.

ORGANIZATIONAL POLICIES:
1. Refund Policy: Full refunds are permitted only if requested within fourteen (14) days of the initial purchase or monthly renewal. No partial refunds for mid-cycle cancellations.
2. Refund Authority Limit: You are authorized to issue refunds up to $50. Any refund request exceeding $50 must be prepared and marked for supervisor escalation.
3. Late Fee Policy: A late fee of 5% of the invoice value is applied if payment is overdue by more than seven (7) grace days. You can waive the late fee once as a one-time courtesy if requested.
4. Double-Charging: If a duplicate charge is verified, apologize immediately, issue a full refund for the duplicate transaction, and provide the transaction reference ID.

INSTRUCTIONS:
Before drafting the customer response, you MUST reason step-by-step inside an `<internal_thinking>` XML tag. Follow this logical sequence:
1. Identify the core billing problem (e.g., late fee waiver request, refund request, incorrect charge).
2. Retrieve the relevant policy guideline from the "ORGANIZATIONAL POLICIES" section.
3. Extract transaction details (dates, amounts, grace periods) from the user's query.
4. Perform necessary calculations (e.g., date differences, refund values, 5% late fee amounts) step-by-step.
5. Check authority limit constraints (e.g., is the refund > $50?).
6. Determine the final resolution and next actions.
7. Outline the structure of the final customer reply.

After the closing </internal_thinking> tag, write your professional customer-facing response. Use a professional, empathetic, and reassuring tone. Structure the final reply with a greeting, acknowledgment, clear resolution, next steps, and sign-off.
```

---

## 4. Sample Responses Comparison

### Scenario A: Refund Request Outside 14-Day Window
* **Customer Query:** *"Hi, I bought the CloudSync annual plan ($120) 22 days ago, but my team decided to use another tool. Can I get a full refund?"*

#### Basic Prompt Response
> "Hello! I can help you with your refund. I will process a refund for your $120 annual plan since you are no longer using the tool. It should appear back in your account in 5-10 business days. Let me know if you need anything else."
>
> *(Critique: **Violates Policy.** It authorized a $120 refund which violates both the 14-day limit and the $50 supervisor escalation authority limit).*

#### Refined Prompt Response
> "Dear Customer,
> 
> Thank you for reaching out to CloudSync billing support. I understand you are requesting a refund for your annual subscription of $120.
> 
> Unfortunately, our company policy only allows refunds for subscriptions within 14 days of purchase. Since your purchase was made 22 days ago, we cannot process a refund. Your subscription will remain active until the end of the billing cycle.
> 
> Please let us know if you would like assistance cancelling your auto-renewal to avoid future charges.
> 
> Sincerely,  
> CloudSync Billing Team"
>
> *(Critique: **Policy correct, but rigid.** Followed the rules, but lacked internal reasoning checks or suggestions of escalation/alternative customer satisfaction steps).*

#### CoT-Enhanced Prompt Response
> <internal_thinking>
> 1. Core Problem: Customer requesting a refund for an annual plan ($120).
> 2. Relevant Policy: Refund Policy (Refunds allowed only within 14 days). Refund Authority (Up to $50; >$50 requires supervisor escalation).
> 3. User Details: Purchase date = 22 days ago. Subscription price = $120.
> 4. Calculations: 22 days > 14 days limit. The request is outside the refund window. The amount is $120 (exceeds $50 limit).
> 5. Authority Constraint: The requested refund is $120. Even if exceptions were made, it exceeds my $50 limit and requires supervisor escalation.
> 6. Resolution: Deny immediate refund as it is outside the 14-day window. However, since it's a high-value annual contract cancellation, escalate the ticket to a billing supervisor to check for partial credit or exceptions.
> 7. Output Structure: Warm greeting, acknowledge the purchase details, politely explain the 14-day refund window, offer cancellation details, inform that the request is escalated to a supervisor for exception review.
> </internal_thinking>
> 
> "Hi there,
> 
> Thank you for reaching out to CloudSync Billing Support. I understand you are looking to request a refund of $120 for your annual plan subscription as your team's needs have shifted.
> 
> According to our standard policy, full refunds can only be processed within 14 days of the initial purchase. Because your purchase was made 22 days ago, it falls outside this standard window.
> 
> However, I want to make sure we support your team as best as we can. Because this is an annual subscription, I have escalated your request to our Billing Supervisor to see if we can make a one-time exception or offer a prorated credit. 
> 
> You can expect a follow-up from our supervisor within 24 hours. In the meantime, I have disabled auto-renewal on your account so you will not be charged again.
> 
> Best regards,  
> CloudSync Billing Team"
>
> *(Critique: **Excellent.** Followed the 14-day policy, recognized the $50 escalation limit, and handled the high-value dispute constructively without violating compliance).*

---

### Scenario B: Dispute of Late Fees
* **Customer Query:** *"Hi, I paid my invoice ($300) 8 days late and got hit with a $15 fee. I never got a reminder email. Can you please remove this late fee?"*

#### Basic Prompt Response
> "Sure, I can remove that $15 late fee for you since you didn't receive the reminder email. I've updated your account."
>
> *(Critique: **Too simple.** Offers no explanation of the late fee structure, doesn't verify grace periods, and does not state it is a one-time courtesy waiver).*

#### Refined Prompt Response
> "Dear Customer,
> 
> I understand you are disputing the $15 late fee on your invoice.
> 
> Our policy applies a 5% fee on invoices overdue by more than 7 days. Your payment was 8 days overdue. However, we can waive this fee once as a one-time courtesy. I have waived the $15 fee and updated your account balance.
> 
> Please ensure future payments are made on time.
> 
> Best regards,  
> CloudSync Billing Team"
>
> *(Critique: **Policy correct.** Mentions the policy rules and waives the fee, but does not detail the math behind it).*

#### CoT-Enhanced Prompt Response
> <internal_thinking>
> 1. Core Problem: Customer disputing a late fee of $15 on a $300 invoice.
> 2. Relevant Policy: Late Fee Policy (5% fee applied if payment is overdue by >7 grace days. Can waive once as a one-time courtesy).
> 3. User Details: Overdue period = 8 days. Invoice value = $300. Late fee charged = $15.
> 4. Calculations: 
>    - Overdue check: 8 days > 7 grace days limit (Late fee is valid).
>    - Late fee calculation: 5% of $300 = $15. The charge is correct.
> 5. Authority Constraint: I can waive the fee as a one-time courtesy. The fee is $15, which is under my $50 authority limit.
> 6. Resolution: Waive the $15 fee as a one-time courtesy, remind the customer of the 7-day grace period, and check why they did not receive the email.
> 7. Output Structure: Personalized greeting, acknowledge the disputed fee, explain the 5% late fee rule and the 7-day grace period, confirm the waiver of the $15 charge, explain how to update email preferences.
> </internal_thinking>
> 
> "Hi there,
> 
> Thank you for contacting CloudSync Billing Support. I understand you are disputing the $15 late fee applied to your invoice of $300, and you mentioned not receiving our reminder email.
> 
> Our system automatically applies a 5% late fee (which calculates to $15 on a $300 balance) when payments are overdue by more than our 7-day grace period. Since your payment was received 8 days past the due date, the system applied the fee.
> 
> However, I completely understand the frustration of missing notifications. I have waived the $15 fee from your account as a one-time courtesy. You will see a credit for this amount on your account dashboard.
> 
> I have also verified your billing email on file to ensure you receive payment reminders moving forward. Please add billing@cloudsync.com to your email contacts to prevent these notifications from landing in your spam folder.
> 
> Warm regards,  
> CloudSync Billing Team"
>
> *(Critique: **Outstanding.** Explains the 5% late fee math, verifies the grace period policy, waives the fee within guidelines, and proactively helps the customer resolve the email reminder issue).*

---

## 5. Evaluation and Recommendation

### Which approach worked best?
The **Chain-of-Thought (CoT) Enhanced Prompt** performed significantly better than both the basic and the refined prompts.

### Why did CoT perform best?
1. **Mathematical Accuracy**: By forcing the model to calculate values (e.g., verifying that a $15 fee on $300 is exactly 5%, or that 22 days is greater than 14 days) inside the `<internal_thinking>` tag, it dramatically reduced mathematical and logical errors.
2. **Constraint Enforcement & Risk Mitigation**: The model evaluated the $50 refund authority limit *before* proposing a solution. In Scenario A, it recognized that the $120 refund was outside its direct authority limit, resulting in a safe escalation path rather than a policy violation or flat refusal.
3. **Structured Contextual Empathy**: The CoT prompt allowed the model to first "plan" the emotional tone and structure of the response, producing answers that feel personalized and supportive rather than cold and regulatory.
4. **Proactive Troubleshooting**: In the thinking phase, the model identified secondary customer issues (such as missing reminder emails) and formulated solutions (verifying email configurations) as part of the final response.
