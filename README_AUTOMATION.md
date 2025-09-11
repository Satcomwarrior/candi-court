# Coercive Control Documentation System - AUTOMATED

## Overview
This is a fully automated system for documenting coercive control patterns and weaponized mental health behaviors. The system integrates interactive tracking, automated report generation, and continuous monitoring.

## 🚀 Quick Start

### Option 1: One-Click Automation
Double-click `run_automation.bat` and choose your option.

### Option 2: PowerShell Direct
```powershell
.\automate_coercive_control.ps1 -Dashboard
```

### Option 3: Background Monitoring
```powershell
.\automate_coercive_control.ps1 -Monitor
```

## 📁 Files in This System

| File | Purpose | How to Use |
|------|---------|------------|
| `coercive_control_tracker.html` | Interactive web-based tracker | Open in browser to document patterns |
| `automate_coercive_control.ps1` | Master automation script | Run with different parameters for different modes |
| `coercive_control_report_generator.ps1` | Professional report generator | Automatically generates legal/mental health reports |
| `psychological_patterns_documenter.ps1` | Pattern analysis tool | Scans files for psychological patterns |
| `run_automation.bat` | Simple launcher | Easy access menu for all functions |
| `setup_scheduled_task.ps1` | Task scheduler setup | Creates automated background monitoring |

## 🎯 Automation Features

### 1. **Interactive Dashboard**
```powershell
.\automate_coercive_control.ps1 -Dashboard
```
- System status overview
- Quick action menu
- Recent activity monitoring
- One-click report generation

### 2. **Background Monitoring**
```powershell
.\automate_coercive_control.ps1 -Monitor
```
- Automatically detects new JSON exports
- Generates reports when new data is available
- Runs continuously in background
- Configurable monitoring interval

### 3. **Scheduled Automation**
```powershell
.\setup_scheduled_task.ps1
```
- Creates Windows scheduled task
- Monitors every 5 minutes automatically
- Runs even when computer is locked
- No manual intervention required

### 4. **One-Click Launcher**
Double-click `run_automation.bat`:
1. Open Dashboard (Interactive Menu)
2. Start Monitoring (Automated Background)
3. Quick Report Generation
4. Open Tracker Only

## 📊 Workflow Automation

### Step 1: Document Patterns
1. Open `coercive_control_tracker.html` in your browser
2. Select categories and check relevant behaviors
3. Add detailed notes with dates, quotes, witnesses
4. Click "Export JSON" to save your work

### Step 2: Automated Processing
- **Manual**: Run `.\automate_coercive_control.ps1` to process immediately
- **Automatic**: Background monitoring detects new exports and processes automatically
- **Scheduled**: Windows task runs processing every 5 minutes

### Step 3: Professional Reports Generated
The system automatically creates:
- **Coercive Control Report**: Professional analysis for legal/mental health review
- **Psychological Patterns Report**: Structured documentation of patterns
- **Integration Reports**: Correlates with existing analysis files

## ⚙️ Configuration

### Automation Settings
Edit the `$config` section in `automate_coercive_control.ps1`:
```powershell
$config = @{
    LastProcessedExport = $null
    AutoBackup = $true
    EmailNotifications = $false  # Set to $true to enable
    IntegrationEnabled = $true
}
```

### Monitoring Interval
Change the monitoring frequency:
```powershell
.\automate_coercive_control.ps1 -Monitor -MonitorInterval 60  # Check every 60 seconds
```

## 📈 Advanced Features

### Integration with Existing Files
The system automatically:
- Scans existing `ANALYSIS_*.txt` files
- Correlates patterns across documents
- Updates reports when new evidence is added
- Maintains chronological documentation

### Backup System
- Automatic backups of all documentation
- Timestamped archives
- Recovery from backup files
- Configurable backup frequency

### Logging
- Comprehensive activity logging
- Error tracking and recovery
- Performance monitoring
- Audit trail for legal purposes

## 🔧 Troubleshooting

### Common Issues

**"Tracker file not found"**
- Ensure all files are in the same directory
- Check file permissions
- Verify file hasn't been moved or renamed

**"No exports found"**
- Make sure you've clicked "Export JSON" in the HTML tracker
- Check that exports are being saved to the Downloads folder
- Verify file naming pattern

**"Reports not generating"**
- Check PowerShell execution policy: `Set-ExecutionPolicy RemoteSigned`
- Ensure all script files are present
- Review error logs in `automation.log`

### Manual Recovery
```powershell
# Force reprocessing of all exports
Get-ChildItem "focus-export-*.json" | ForEach-Object {
    # Process each export manually
    .\coercive_control_report_generator.ps1
}
```

## 📋 Professional Integration

### For Legal Professionals
- Reports are formatted for court admissibility
- Pattern evidence demonstrates "course of conduct"
- Timeline correlation supports protective orders
- Structured for forensic documentation

### For Mental Health Professionals
- DSM-aligned pattern recognition
- Risk assessment frameworks
- Treatment planning support
- Crisis intervention documentation

### For Protective Services
- Safety planning integration
- Risk level assessment
- Intervention coordination
- Long-term monitoring support

## 🔒 Security & Privacy

- All data stored locally (no cloud uploads)
- Browser-based tracker uses local storage only
- No external dependencies or APIs
- Professional-grade documentation standards
- HIPAA-compliant structure for mental health data

## 📞 Support

### Quick Diagnosis
Run the dashboard to check system status:
```powershell
.\automate_coercive_control.ps1 -Dashboard
```

### Log Review
Check `automation.log` for detailed activity:
```powershell
Get-Content automation.log -Tail 20
```

### System Reset
To reset the entire system:
```powershell
Remove-Item automation_config.json
Remove-Item automation.log
# Then re-run setup
```

---

## 🎯 Next Steps

1. **Start Here**: Double-click `run_automation.bat`
2. **Document**: Open the HTML tracker and begin documenting patterns
3. **Automate**: Set up scheduled monitoring for continuous operation
4. **Review**: Use generated reports for professional consultation

This automated system transforms pattern documentation from manual work into a professional, integrated workflow that supports legal proceedings, mental health treatment, and protective services coordination.

**Remember**: This system creates documentation for professional review. Always consult qualified mental health and legal professionals for assessment and action planning.
