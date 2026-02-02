# Build script for SSHD Archipelago Client

Write-Host "Building SSHD Archipelago Client..." -ForegroundColor Cyan

# Build the client executable
Write-Host "`nBuilding ArchipelagoSSHDClient.exe..." -ForegroundColor Yellow
pyinstaller SSHDClient.spec --clean

if ($LASTEXITCODE -eq 0) {
    Write-Host "`nBuild successful!" -ForegroundColor Green
    Write-Host "Executable location: dist\ArchipelagoSSHDClient.exe" -ForegroundColor Green
    
    # Get file size
    $exe = Get-Item "dist\ArchipelagoSSHDClient.exe"
    $sizeMB = [math]::Round($exe.Length / 1MB, 2)
    Write-Host "File size: $sizeMB MB" -ForegroundColor Cyan
    
    Write-Host "`nTo test the client:" -ForegroundColor Yellow
    Write-Host "  1. Start Ryujinx with SSHD running" -ForegroundColor White
    Write-Host "  2. Run: .\dist\ArchipelagoSSHDClient.exe" -ForegroundColor White
    Write-Host "  3. Connect to your Archipelago server" -ForegroundColor White
} else {
    Write-Host "`nBuild failed!" -ForegroundColor Red
    exit 1
}
