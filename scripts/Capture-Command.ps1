param(
  [Parameter(Mandatory = $true)][string]$Command,
  [Parameter(Mandatory = $true)][string]$OutputPath,
  [string]$Title = 'Kubernetes Lab Evidence'
)

# Captures the actual command output and renders it into a PNG evidence image.
Add-Type -AssemblyName System.Drawing
$result = Invoke-Expression "$Command 2>&1" | Out-String
$font = New-Object System.Drawing.Font('Consolas', 14)
$bmp = New-Object System.Drawing.Bitmap(1600, 900)
$g = [System.Drawing.Graphics]::FromImage($bmp)
$g.Clear([System.Drawing.Color]::FromArgb(30, 30, 30))
$g.DrawString($Title, (New-Object System.Drawing.Font('Segoe UI', 18, [System.Drawing.FontStyle]::Bold)), [System.Drawing.Brushes]::White, 28, 22)
$g.DrawString(('PS> ' + $Command + "`r`n`r`n" + $result), $font, [System.Drawing.Brushes]::LightGreen, (New-Object System.Drawing.RectangleF(28, 70, 1540, 800)))
$folder = Split-Path -Parent $OutputPath
New-Item -ItemType Directory -Force -Path $folder | Out-Null
$bmp.Save($OutputPath, [System.Drawing.Imaging.ImageFormat]::Png)
$g.Dispose(); $bmp.Dispose(); $font.Dispose()
