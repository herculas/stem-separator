[CmdletBinding(DefaultParameterSetName = 'Path')]
param(
    [Parameter(Mandatory = $true, ParameterSetName = 'Path')]
    [string]$InputFile,

    [Parameter(Mandatory = $true, ParameterSetName = 'Library')]
    [string]$Track,

    [Parameter(ParameterSetName = 'Library')]
    [string]$Collection,

    [string]$OutputRoot,

    [switch]$KeepDecodedWav
)

$ErrorActionPreference = 'Stop'
Set-StrictMode -Version Latest
$env:PYTHONUTF8 = '1'

$projectRoot = Split-Path -Parent $PSScriptRoot
$python = Join-Path $projectRoot '.venv\Scripts\python.exe'
$modelsDir = Join-Path $projectRoot 'models'
$workRoot = Join-Path $projectRoot '.work\bs-roformer'
$localConfigPath = Join-Path $projectRoot 'config\local.psd1'

if (-not $OutputRoot) {
    $OutputRoot = Join-Path $projectRoot 'outputs\6-stem'
}

if (-not (Test-Path -LiteralPath $python -PathType Leaf)) {
    throw "Python environment not found: $python"
}
if ($PSCmdlet.ParameterSetName -eq 'Library') {
    if (-not (Test-Path -LiteralPath $localConfigPath -PathType Leaf)) {
        throw "Local music-library config not found: $localConfigPath. Copy config/local.example.psd1 to config/local.psd1."
    }
    $localConfig = Import-PowerShellDataFile -LiteralPath $localConfigPath
    if (-not $localConfig.MusicRoot) {
        throw "MusicRoot is missing from: $localConfigPath"
    }
    if (-not $Collection) {
        $Collection = $localConfig.DefaultCollection
    }
    if (-not $Collection) {
        throw 'Collection was not supplied and DefaultCollection is not configured.'
    }
    $InputFile = Join-Path (Join-Path $localConfig.MusicRoot $Collection) $Track
}

$source = Get-Item -LiteralPath $InputFile
$trackName = [System.IO.Path]::GetFileNameWithoutExtension($source.Name)
$workDir = Join-Path $workRoot $trackName
$decodedWav = Join-Path $workDir "$trackName.wav"
$trackOutput = Join-Path $OutputRoot $trackName

New-Item -ItemType Directory -Force -Path $modelsDir, $workDir, $trackOutput | Out-Null

$ffmpeg = (& $python -c "import imageio_ffmpeg; print(imageio_ffmpeg.get_ffmpeg_exe())").Trim()
if (-not (Test-Path -LiteralPath $ffmpeg -PathType Leaf)) {
    throw "FFmpeg executable not found: $ffmpeg"
}

Write-Host "Decoding: $($source.FullName)"
& $ffmpeg -hide_banner -loglevel error -y -i $source.FullName -vn -map_metadata -1 -ac 2 -ar 44100 -c:a pcm_s24le $decodedWav
if ($LASTEXITCODE -ne 0) {
    throw "FFmpeg failed with exit code $LASTEXITCODE"
}

Write-Host "Separating on CUDA: $trackName"
& $python -c 'from bs_roformer.inference import main; main()' `
    --model 'roformer-model-bs-roformer-sw-by-jarredou' `
    --models_dir $modelsDir `
    --input_folder $workDir `
    --store_dir $trackOutput `
    --device cuda
if ($LASTEXITCODE -ne 0) {
    throw "BS-RoFormer failed with exit code $LASTEXITCODE"
}

if (-not $KeepDecodedWav -and (Test-Path -LiteralPath $decodedWav -PathType Leaf)) {
    Remove-Item -LiteralPath $decodedWav
}

Write-Host "Completed: $trackOutput"
