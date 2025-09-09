#!/usr/bin/env python3
"""
Example usage of the Reasonableness Analyzer

This script demonstrates how to use the analyzer with different types of requests and complaints.
"""

from reasonableness_analyzer import analyze_text

def demonstrate_analyzer():
    """Demonstrate the analyzer with various examples."""
    
    examples = [
        {
            "title": "Professional Legal Request",
            "text": """
            Dear Counsel,
            
            I respectfully request that you cease and desist from the ongoing violation
            of our contract dated March 1, 2024 (Section 4.2). Your client's failure
            to perform under the agreement constitutes a material breach.
            
            We have documented evidence of non-performance including emails and witness statements.
            Please respond within 30 days to avoid further legal action.
            
            Respectfully,
            Attorney Smith
            """
        },
        {
            "title": "Reasonable Customer Complaint",
            "text": """
            I am writing to request a refund of $150.00 for the defective product I purchased
            on January 15, 2024. The item (Invoice #12345) stopped working after two days.
            I have the receipt and photos of the defect. Please process this refund within
            10 business days as stated in your return policy.
            """
        },
        {
            "title": "Unreasonable Demand",
            "text": """
            YOU PEOPLE ARE IDIOTS!!! I DEMAND $10,000 IN DAMAGES BECAUSE MY ORDER
            WAS WRONG!!! THIS IS OUTRAGEOUS AND I'M GOING TO SUE EVERYONE!!!
            I'M CALLING THE FBI AND THE PRESIDENT!!!
            """
        },
        {
            "title": "Vague Complaint",
            "text": """
            Something went wrong with my thing and I'm not happy about it.
            Someone should fix this somehow. This is sort of urgent I guess.
            Please do something about this stuff.
            """
        }
    ]
    
    print("REASONABLENESS ANALYZER DEMONSTRATION")
    print("=" * 60)
    print()
    
    for example in examples:
        print(f"📋 {example['title']}")
        print("-" * 40)
        
        result = analyze_text(example['text'])
        
        print(f"Overall Score: {result.overall_score:.2f}/5.0")
        print(f"Reasonableness Level: {result.reasonableness_level.name.replace('_', ' ').title()}")
        print()
        print("Criteria Breakdown:")
        for criterion, score in result.criteria_scores.items():
            print(f"  • {criterion.replace('_', ' ').title()}: {score:.1f}/5.0")
        
        if result.suggestions:
            print()
            print("Suggestions for Improvement:")
            for i, suggestion in enumerate(result.suggestions, 1):
                print(f"  {i}. {suggestion}")
        
        print()
        print("=" * 60)
        print()


if __name__ == "__main__":
    demonstrate_analyzer()
