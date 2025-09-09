#!/usr/bin/env python3
"""
Demonstration script showing the enhanced manipulation detection capabilities.
"""

from enhanced_manipulation_detector import EnhancedManipulationDetector
import json

def demo_enhanced_detection():
    """Demonstrate the enhanced manipulation detection capabilities."""
    
    print("🔍 ENHANCED MANIPULATION DETECTION DEMONSTRATION")
    print("=" * 60)
    
    # Initialize the detector
    detector = EnhancedManipulationDetector()
    
    # Sample communications that would appear in legal cases
    sample_communications = [
        {
            "source": "Text Message Thread",
            "text": "You're overreacting as usual. This never happened the way you remember it. You always make things up when you're upset."
        },
        {
            "source": "Email Communication", 
            "text": "If you leave me, I'll hurt myself and it will be your fault. You know I can't live without you."
        },
        {
            "source": "Recorded Conversation",
            "text": "You can't survive without me. You need me to take care of everything. You're helpless on your own."
        },
        {
            "source": "Social Media Post",
            "text": "After everything I've done for you, how can you be so ungrateful? I sacrificed everything for this relationship."
        },
        {
            "source": "Voice Recording",
            "text": "You made me angry, so I had to yell at you. It's not my fault you can't handle criticism."
        }
    ]
    
    all_instances = []
    
    for i, comm in enumerate(sample_communications, 1):
        print(f"\n📱 ANALYZING COMMUNICATION #{i}: {comm['source']}")
        print("-" * 50)
        print(f"Text: \"{comm['text']}\"")
        print()
        
        # Analyze with enhanced detector
        instances = detector.analyze_text(
            comm['text'], 
            comm['source'],
            context_metadata={'communication_type': comm['source'], 'sequence': i}
        )
        
        all_instances.extend(instances)
        
        if instances:
            print(f"🎯 DETECTED {len(instances)} MANIPULATION PATTERNS:")
            for instance in instances:
                print(f"  • Pattern: {instance.pattern_name.replace('_', ' ').title()}")
                print(f"    Method: {instance.pattern_type}")
                print(f"    Confidence: {instance.confidence_score:.3f}")
                print(f"    Sentiment: {instance.sentiment_score:.3f}")
                if instance.semantic_similarity > 0:
                    print(f"    Semantic Similarity: {instance.semantic_similarity:.3f}")
                print()
        else:
            print("❌ No manipulation patterns detected")
    
    # Generate comprehensive analysis
    print("\n📊 COMPREHENSIVE ANALYSIS SUMMARY")
    print("=" * 60)
    
    if all_instances:
        # Pattern frequency analysis
        pattern_counts = {}
        for instance in all_instances:
            pattern_name = instance.pattern_name.replace('_', ' ').title()
            pattern_counts[pattern_name] = pattern_counts.get(pattern_name, 0) + 1
        
        print("🔍 PATTERN FREQUENCY:")
        for pattern, count in sorted(pattern_counts.items(), key=lambda x: x[1], reverse=True):
            print(f"  • {pattern}: {count} instances")
        
        # Method effectiveness
        method_counts = {}
        for instance in all_instances:
            method_counts[instance.pattern_type] = method_counts.get(instance.pattern_type, 0) + 1
        
        print(f"\n🧠 DETECTION METHOD EFFECTIVENESS:")
        for method, count in sorted(method_counts.items(), key=lambda x: x[1], reverse=True):
            print(f"  • {method.title()}: {count} detections")
        
        # Confidence analysis
        high_confidence = [i for i in all_instances if i.confidence_score > 0.8]
        medium_confidence = [i for i in all_instances if 0.6 <= i.confidence_score <= 0.8]
        low_confidence = [i for i in all_instances if i.confidence_score < 0.6]
        
        print(f"\n📈 CONFIDENCE DISTRIBUTION:")
        print(f"  • High Confidence (>0.8): {len(high_confidence)} instances")
        print(f"  • Medium Confidence (0.6-0.8): {len(medium_confidence)} instances") 
        print(f"  • Low Confidence (<0.6): {len(low_confidence)} instances")
        
        # Legal documentation recommendations
        print(f"\n⚖️  LEGAL DOCUMENTATION RECOMMENDATIONS:")
        print(f"  • Focus on {len(high_confidence)} high-confidence instances for court presentation")
        print(f"  • Document specific dates, times, and context for each incident")
        print(f"  • Track escalation patterns across {len(set(i.source_file for i in all_instances))} communication sources")
        print(f"  • Consider expert witness testimony for complex manipulation patterns")
        
        # Export summary
        summary_data = {
            "total_instances": len(all_instances),
            "pattern_breakdown": pattern_counts,
            "method_breakdown": method_counts,
            "confidence_summary": {
                "high": len(high_confidence),
                "medium": len(medium_confidence), 
                "low": len(low_confidence)
            },
            "recommendations": [
                f"Focus on {len(high_confidence)} high-confidence instances for court presentation",
                "Document specific dates, times, and context for each incident",
                f"Track escalation patterns across {len(set(i.source_file for i in all_instances))} communication sources",
                "Consider expert witness testimony for complex manipulation patterns"
            ]
        }
        
        with open("demo_analysis_summary.json", "w") as f:
            json.dump(summary_data, f, indent=2)
        
        print(f"\n💾 Analysis summary exported to: demo_analysis_summary.json")
        
    else:
        print("❌ No manipulation patterns detected in any communications")
    
    print(f"\n✅ DEMONSTRATION COMPLETED")
    print(f"Total Manipulation Instances Detected: {len(all_instances)}")
    print("=" * 60)

if __name__ == "__main__":
    demo_enhanced_detection()