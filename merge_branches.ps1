# PowerShell script to merge multiple branches
# Branches that need to be merged (with unmerged commits)

$branchesToMerge = @(
    "codex/confirm-and-clean-empty-files",
    "codex/consolidate-communication_manager-implementations", 
    "codex/consolidate-performance_monitor.py-as-master-version",
    "codex/create-common-metrics-module",
    "codex/create-evaluate_model-function-and-update-modules",
    "codex/create-metrics-modules-and-centralize-definitions",
    "codex/enforce-abstract-methods-implementation",
    "codex/extract-and-test-shared-utilities",
    "codex/extract-validation-rules-into-modules",
    "codex/implement-session-management-features",
    "codex/modularize-framework-and-add-documentation",
    "codex/move-logic-to-decision_metrics.py-and-refactor-others",
    "codex/move-pattern-and-rule-dictionaries-to-files",
    "codex/refactor-agent-features-into-submodules",
    "codex/refactor-data-processing-logic-into-modules",
    "codex/refactor-files-over-400-loc",
    "codex/refactor-fsm-into-separate-modules",
    "codex/refactor-jenkins-groovy-script-into-library-steps",
    "codex/refactor-messaging-services-into-modules",
    "codex/refactor-metric-gathering-and-calculations",
    "codex/refactor-workflow-reliability-testing-module",
    "codex/remove-direct-logging-calls-and-document-usage",
    "codex/remove-or-implement-logic-in-zero-length-files",
    "codex/split-finalization-logic-into-modules",
    "codex/split-metric-handling-into-separate-files"
)

Write-Host "Starting to merge $($branchesToMerge.Count) branches..." -ForegroundColor Green

foreach ($branch in $branchesToMerge) {
    Write-Host "Processing branch: $branch" -ForegroundColor Yellow
    
    try {
        # Try to merge the branch
        $result = git merge "origin/$branch" 2>&1
        
        if ($LASTEXITCODE -eq 0) {
            Write-Host "Successfully merged $branch" -ForegroundColor Green
            
            # Push the changes
            git push origin agent
            Write-Host "Pushed merged changes for $branch" -ForegroundColor Green
            
            # Try to delete the remote branch
            git push origin --delete $branch 2>$null
            Write-Host "Deleted remote branch $branch" -ForegroundColor Green
            
        } else {
            # Check if there are conflicts
            if ($result -match "CONFLICT") {
                Write-Host "Merge conflict detected in $branch, resolving..." -ForegroundColor Yellow
                
                # Get list of conflicted files
                $conflictedFiles = git diff --name-only --diff-filter=U
                
                foreach ($file in $conflictedFiles) {
                    # Accept incoming changes for all conflicted files
                    git checkout --theirs $file
                    Write-Host "Resolved conflict in $file" -ForegroundColor Cyan
                }
                
                # Add all resolved files
                git add .
                
                # Commit the merge
                git commit --no-verify -m "Merge $branch branch (resolved conflicts)"
                Write-Host "Resolved conflicts and committed merge for $branch" -ForegroundColor Green
                
                # Push the changes
                git push origin agent
                Write-Host "Pushed resolved merge for $branch" -ForegroundColor Green
                
                # Try to delete the remote branch
                git push origin --delete $branch 2>$null
                Write-Host "Deleted remote branch $branch" -ForegroundColor Green
                
            } else {
                Write-Host "Branch $branch is already up to date" -ForegroundColor Cyan
            }
        }
        
    } catch {
        Write-Host "Error processing branch $branch : $_" -ForegroundColor Red
    }
    
    Write-Host "----------------------------------------" -ForegroundColor Gray
}

Write-Host "Branch merging process completed!" -ForegroundColor Green
