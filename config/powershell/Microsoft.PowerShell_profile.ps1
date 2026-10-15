# ==============================================================================
# PowerShell Profile - Interactive History Prediction (ListView)
# ==============================================================================

if (Get-Module -ListAvailable -Name PSReadLine) {
    Import-Module PSReadLine
    # Display predictive suggestions from command history in interactive vertical list view
    Set-PSReadLineOption -PredictionSource History
    Set-PSReadLineOption -PredictionViewStyle ListView
    
    # Keybindings for smooth menu navigation
    Set-PSReadLineKeyHandler -Key Tab -Function Complete
    Set-PSReadLineKeyHandler -Key UpArrow -Function PreviousHistory
    Set-PSReadLineKeyHandler -Key DownArrow -Function NextHistory
}

function Invoke-Explorer {
    param([string]$Path = ".")
    Start-Process -FilePath "start" -ArgumentList $Path
}
Set-Alias -Name explorer -Value Invoke-Explorer -Option AllScope -ErrorAction SilentlyContinue
Set-Alias -Name open -Value Invoke-Explorer -Option AllScope -ErrorAction SilentlyContinue

