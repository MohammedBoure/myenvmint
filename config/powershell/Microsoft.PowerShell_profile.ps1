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
