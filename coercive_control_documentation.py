#!/usr/bin/env python3
"""
Coercive Control Patterns Documentation Tool

This tool scans documents for coercive control patterns and emotional manipulation tactics,
creating structured documentation for mental health professionals.

Usage:
    python coercive_control_documentation.py [directory_path]
"""

import os
import re
import sys
import json
import docx
from datetime import datetime
from collections import defaultdict
from typing import Dict, List, Tuple, Any


class CoerciveControlDetector:
    """Detects coercive control patterns in text documents."""
    
    def __init__(self):
        self.patterns = self._initialize_patterns()
        self.detected_instances = defaultdict(list)
        
    def _initialize_patterns(self) -> Dict[str, Dict[str, List[str]]]:
        """Initialize keyword patterns for each coercive control category."""
        return {
            "isolation_and_monitoring": {
                "description": "Restricting contact, tracking devices, excessive check-ins, password control, or blocking transport and finances to limit autonomy",
                "keywords": [
                    "tracking", "monitoring", "check in", "check-in", "checking up",
                    "password", "passwords", "location", "GPS", "phone access",
                    "restrict contact", "block contact", "isolate", "isolation",
                    "car keys", "transportation", "bank account", "credit card",
                    "social media", "friends", "family", "surveillance", "watching",
                    "following", "stalking", "control access", "permission to",
                    "not allowed", "forbid", "forbidden", "cut off", "cut-off"
                ]
            },
            "rule_making_and_enforcement": {
                "description": "Imposing arbitrary rules, shifting expectations, and punishing deviations with silent treatment, rage, or threats",
                "keywords": [
                    "rules", "you must", "you have to", "you need to", "you should",
                    "silent treatment", "ignoring", "punishment", "punish",
                    "consequences", "discipline", "obey", "obedience", "comply",
                    "expectations", "demands", "requirements", "orders",
                    "rage", "anger", "yelling", "screaming", "threatening",
                    "threats", "if you don't", "or else", "consequences",
                    "arbitrary", "changing rules", "moving goalposts"
                ]
            },
            "minimizing_denying_blaming": {
                "description": "Flipping the script, reframing concerns as overreactions, or claiming the victim made them act this way",
                "keywords": [
                    "overreacting", "over-reacting", "dramatic", "sensitive",
                    "made me", "you made me", "your fault", "you caused",
                    "not that bad", "didn't happen", "never said that",
                    "you're imagining", "you're crazy", "you're being",
                    "flip the script", "turn it around", "blame shift",
                    "victim", "playing victim", "not my fault",
                    "deny", "denial", "minimize", "exaggerate"
                ]
            },
            "financial_control": {
                "description": "Withholding funds, dictating spending, sabotaging work, or creating dependency to gain leverage",
                "keywords": [
                    "money", "finances", "spending", "budget", "allowance",
                    "bank account", "credit card", "debt", "financial",
                    "work", "job", "employment", "sabotage", "quit",
                    "paycheck", "income", "earnings", "control money",
                    "withhold", "dependency", "dependent", "leverage",
                    "economic", "financial abuse", "hide money", "secret account"
                ]
            },
            "self_harm_threats": {
                "description": "If you leave, I'll hurt myself - making the other responsible for their survival; repeat crises timed to control choices",
                "keywords": [
                    "hurt myself", "kill myself", "suicide", "self-harm",
                    "if you leave", "without you", "can't live without",
                    "end it all", "not worth living", "responsible for",
                    "your fault if", "crisis", "emergency", "timing",
                    "hospital", "pills", "overdose", "cutting"
                ]
            },
            "guilt_fear_obligation": {
                "description": "Leveraging pity, tears, or staged victimhood to extract compliance; withdrawing affection or support as punishment",
                "keywords": [
                    "guilt", "pity", "feel sorry", "tears", "crying",
                    "victim", "poor me", "suffering", "pain",
                    "withdraw", "withhold affection", "cold shoulder",
                    "punishment", "compliance", "obligation", "duty",
                    "owe me", "after everything", "sacrifice", "staged"
                ]
            },
            "gaslighting_reality_distortion": {
                "description": "Denying obvious facts, rewriting history, or manufacturing confusion so targets doubt their own judgment",
                "keywords": [
                    "gaslighting", "gaslight", "never happened", "didn't say",
                    "you're imagining", "you're crazy", "memory", "remember",
                    "that's not what happened", "rewrite history", "confusion",
                    "doubt", "judgment", "reality", "facts", "obvious",
                    "manufacturing", "distortion", "deny obvious"
                ]
            },
            "weaponized_incompetence": {
                "description": "Performing tasks poorly to force the partner to carry all responsibilities, then using that imbalance to control outcomes",
                "keywords": [
                    "incompetence", "can't do", "don't know how", "bad at",
                    "force to do", "carry responsibility", "imbalance",
                    "control outcomes", "poorly", "weaponize", "helpless",
                    "can't handle", "too difficult", "you're better at"
                ]
            },
            "credibility_attacks": {
                "description": "Exaggerating or misrepresenting mental health to depict instability or unfitness, especially in custody or protection proceedings",
                "keywords": [
                    "unstable", "unfit", "mental health", "crazy", "insane",
                    "bipolar", "depressed", "anxiety", "therapy", "medication",
                    "custody", "court", "proceedings", "credibility", "reputation",
                    "character", "fitness", "parenting", "exaggerate", "misrepresent"
                ]
            },
            "third_party_enlistment": {
                "description": "Recruiting friends, family, or professionals to validate a narrative that isolates the target or pressures them to comply",
                "keywords": [
                    "recruit", "enlist", "friends", "family", "professionals",
                    "validate", "narrative", "isolate", "pressure", "comply",
                    "gang up", "turn against", "convince", "persuade",
                    "flying monkeys", "allies", "support", "backing"
                ]
            },
            "procedural_coercion": {
                "description": "Filing serial complaints, exploiting court processes, or tactical concern requests primarily to surveil or control rather than protect",
                "keywords": [
                    "serial complaints", "court", "legal", "filing", "process",
                    "tactical", "concern", "welfare check", "wellness check",
                    "surveil", "surveillance", "control", "exploit", "harassment",
                    "frivolous", "abuse of process", "vexatious"
                ]
            },
            "love_bombing_to_dependency": {
                "description": "High-intensity care, gifts, and 'I'll take care of you' narratives that evolve into surveillance, decision-seizing, and curtailed freedom",
                "keywords": [
                    "love bombing", "gifts", "care", "take care of you",
                    "intensity", "overwhelming", "surveillance", "decisions",
                    "freedom", "curtailed", "dependency", "control", "seize",
                    "intense attention", "excessive gifts", "too much too fast"
                ]
            },
            "jealousy_as_care": {
                "description": "I'm just worried becomes constant checking, dictating clothing, or escorting to limit independent activity",
                "keywords": [
                    "jealousy", "worried", "checking", "clothing", "what you wear",
                    "escort", "accompany", "independent", "activity", "limit",
                    "possessive", "territorial", "suspicious", "interrogate"
                ]
            },
            "communication_patterns": {
                "description": "Punisher, self-punisher, sufferer, tantalizer patterns and chronic ambiguity with moving goalposts",
                "keywords": [
                    "punisher", "punishment", "self-punish", "suffering", "sufferer",
                    "tantalizer", "tease", "ambiguity", "unclear", "confusing",
                    "moving goalposts", "changing standards", "never right",
                    "learned helplessness", "compliance", "conditional love",
                    "approval", "obedience", "chronic", "pattern"
                ]
            }
        }
    
    def scan_text(self, text: str, source_file: str = "") -> Dict[str, List[Dict]]:
        """Scan text for coercive control patterns."""
        text_lower = text.lower()
        results = {}
        
        for pattern_name, pattern_data in self.patterns.items():
            matches = []
            for keyword in pattern_data["keywords"]:
                if keyword.lower() in text_lower:
                    # Find all occurrences with context
                    contexts = self._find_keyword_contexts(text, keyword)
                    for context in contexts:
                        matches.append({
                            "keyword": keyword,
                            "context": context,
                            "source_file": source_file,
                            "timestamp": datetime.now().isoformat(),
                            "pattern_description": pattern_data["description"]
                        })
            
            if matches:
                results[pattern_name] = matches
        
        return results
    
    def _find_keyword_contexts(self, text: str, keyword: str, context_length: int = 200) -> List[str]:
        """Find keyword occurrences with surrounding context."""
        contexts = []
        text_lower = text.lower()
        keyword_lower = keyword.lower()
        
        start = 0
        while True:
            index = text_lower.find(keyword_lower, start)
            if index == -1:
                break
            
            # Extract context around the keyword
            start_context = max(0, index - context_length // 2)
            end_context = min(len(text), index + len(keyword) + context_length // 2)
            context = text[start_context:end_context].strip()
            
            contexts.append(context)
            start = index + 1
        
        return contexts
    
    def scan_docx_file(self, file_path: str) -> Dict[str, List[Dict]]:
        """Scan a Word document for coercive control patterns."""
        try:
            doc = docx.Document(file_path)
            text = ""
            for paragraph in doc.paragraphs:
                text += paragraph.text + "\n"
            
            return self.scan_text(text, os.path.basename(file_path))
        except Exception as e:
            print(f"Error reading {file_path}: {e}")
            return {}
    
    def scan_text_file(self, file_path: str) -> Dict[str, List[Dict]]:
        """Scan a text file for coercive control patterns."""
        try:
            with open(file_path, 'r', encoding='utf-8', errors='ignore') as file:
                text = file.read()
            
            return self.scan_text(text, os.path.basename(file_path))
        except Exception as e:
            print(f"Error reading {file_path}: {e}")
            return {}
    
    def scan_directory(self, directory_path: str) -> Dict[str, Any]:
        """Scan all documents in a directory for coercive control patterns."""
        all_results = defaultdict(list)
        file_count = 0
        
        for root, dirs, files in os.walk(directory_path):
            for file in files:
                file_path = os.path.join(root, file)
                file_ext = os.path.splitext(file)[1].lower()
                
                results = {}
                if file_ext == '.docx':
                    results = self.scan_docx_file(file_path)
                elif file_ext in ['.txt', '.md']:
                    results = self.scan_text_file(file_path)
                
                if results:
                    file_count += 1
                    for pattern_name, matches in results.items():
                        all_results[pattern_name].extend(matches)
        
        return {
            "summary": {
                "files_scanned": file_count,
                "total_patterns_detected": len(all_results),
                "scan_timestamp": datetime.now().isoformat()
            },
            "patterns": dict(all_results)
        }


class DocumentationGenerator:
    """Generates structured documentation reports for mental health professionals."""
    
    def __init__(self, detector: CoerciveControlDetector):
        self.detector = detector
    
    def generate_checklist_report(self, scan_results: Dict[str, Any], output_file: str = None) -> str:
        """Generate a checklist-style report for tracking instances."""
        report = []
        
        # Header
        report.append("=" * 80)
        report.append("COERCIVE CONTROL PATTERNS DOCUMENTATION REPORT")
        report.append("=" * 80)
        report.append(f"Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        report.append(f"Files Scanned: {scan_results['summary']['files_scanned']}")
        report.append(f"Patterns Detected: {scan_results['summary']['total_patterns_detected']}")
        report.append("")
        
        # Summary checklist
        report.append("PATTERN DETECTION SUMMARY:")
        report.append("-" * 40)
        
        for pattern_name in self.detector.patterns.keys():
            pattern_display = pattern_name.replace("_", " ").title()
            detected = "✓" if pattern_name in scan_results['patterns'] else "✗"
            count = len(scan_results['patterns'].get(pattern_name, []))
            report.append(f"[{detected}] {pattern_display}: {count} instances")
        
        report.append("")
        
        # Detailed findings
        report.append("DETAILED PATTERN ANALYSIS:")
        report.append("=" * 50)
        
        for pattern_name, matches in scan_results['patterns'].items():
            if not matches:
                continue
            
            pattern_display = pattern_name.replace("_", " ").title()
            pattern_desc = self.detector.patterns[pattern_name]["description"]
            
            report.append(f"\n{pattern_display.upper()}")
            report.append("-" * len(pattern_display))
            report.append(f"Description: {pattern_desc}")
            report.append(f"Instances Found: {len(matches)}")
            report.append("")
            
            # Group by source file
            files_dict = defaultdict(list)
            for match in matches:
                files_dict[match['source_file']].append(match)
            
            for source_file, file_matches in files_dict.items():
                report.append(f"  Source: {source_file}")
                for i, match in enumerate(file_matches, 1):
                    report.append(f"    {i}. Keyword: '{match['keyword']}'")
                    report.append(f"       Context: {match['context'][:150]}...")
                    report.append(f"       Timestamp: {match['timestamp']}")
                    report.append("")
        
        # Documentation tracking template
        report.append("\nDOCUMENTATION TRACKING TEMPLATE:")
        report.append("=" * 50)
        report.append("Use this template to track additional information for each instance:")
        report.append("")
        report.append("[ ] Pattern: ________________________")
        report.append("[ ] Date/Time: ______________________")
        report.append("[ ] Witnesses: ______________________")
        report.append("[ ] Outcome/Response: ________________")
        report.append("[ ] Frequency: ______________________")
        report.append("[ ] Function/Payoff: _________________")
        report.append("[ ] Third-party Corroboration: _______")
        report.append("")
        
        # Pattern markers guidance
        report.append("PATTERN MARKERS TO DOCUMENT:")
        report.append("-" * 30)
        report.append("• Frequency and timing: Note if crises or threats arise at key decision points")
        report.append("• Function and payoff: Document if behavior secures access, stops separation, or silences objections")
        report.append("• Generalization: Track if tactics appear across multiple contexts and escalate when resisted")
        report.append("• Third-party corroboration: Collect therapist notes, GAL reports, police/medical records")
        report.append("")
        
        report_text = "\n".join(report)
        
        if output_file:
            with open(output_file, 'w', encoding='utf-8') as f:
                f.write(report_text)
            print(f"Report saved to: {output_file}")
        
        return report_text
    
    def generate_json_report(self, scan_results: Dict[str, Any], output_file: str = None) -> str:
        """Generate a JSON report for programmatic analysis."""
        json_data = {
            "metadata": {
                "tool_version": "1.0.0",
                "scan_timestamp": scan_results['summary']['scan_timestamp'],
                "files_scanned": scan_results['summary']['files_scanned'],
                "patterns_detected": scan_results['summary']['total_patterns_detected']
            },
            "pattern_definitions": self.detector.patterns,
            "findings": scan_results['patterns'],
            "recommendations": [
                "Document dates, times, and witnesses for each instance",
                "Track frequency and timing patterns, especially around key decisions",
                "Note function and payoff of behaviors",
                "Collect third-party corroboration when possible",
                "Monitor for escalation when tactics are resisted"
            ]
        }
        
        json_text = json.dumps(json_data, indent=2)
        
        if output_file:
            with open(output_file, 'w', encoding='utf-8') as f:
                f.write(json_text)
            print(f"JSON report saved to: {output_file}")
        
        return json_text


def main():
    """Main function to run the coercive control documentation tool."""
    if len(sys.argv) > 1:
        directory_path = sys.argv[1]
    else:
        directory_path = "."
    
    if not os.path.exists(directory_path):
        print(f"Error: Directory '{directory_path}' does not exist.")
        sys.exit(1)
    
    print("Coercive Control Patterns Documentation Tool")
    print("=" * 50)
    print(f"Scanning directory: {directory_path}")
    print("This may take a few moments...")
    print()
    
    # Initialize detector and scan directory
    detector = CoerciveControlDetector()
    scan_results = detector.scan_directory(directory_path)
    
    # Generate documentation
    generator = DocumentationGenerator(detector)
    
    # Create reports directory if it doesn't exist
    reports_dir = "coercive_control_reports"
    os.makedirs(reports_dir, exist_ok=True)
    
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    
    # Generate checklist report
    checklist_file = os.path.join(reports_dir, f"coercive_control_checklist_{timestamp}.txt")
    checklist_report = generator.generate_checklist_report(scan_results, checklist_file)
    
    # Generate JSON report
    json_file = os.path.join(reports_dir, f"coercive_control_data_{timestamp}.json")
    json_report = generator.generate_json_report(scan_results, json_file)
    
    # Print summary
    print(f"Scan completed successfully!")
    print(f"Files scanned: {scan_results['summary']['files_scanned']}")
    print(f"Patterns detected: {scan_results['summary']['total_patterns_detected']}")
    print(f"Reports generated in: {reports_dir}/")
    print()
    
    # Show brief summary of findings
    if scan_results['patterns']:
        print("PATTERNS DETECTED:")
        for pattern_name, matches in scan_results['patterns'].items():
            pattern_display = pattern_name.replace("_", " ").title()
            print(f"  • {pattern_display}: {len(matches)} instances")
    else:
        print("No coercive control patterns detected in the scanned documents.")


if __name__ == "__main__":
    main()