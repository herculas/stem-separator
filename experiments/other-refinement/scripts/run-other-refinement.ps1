param(
    [Parameter(Mandatory = $true)]
    [string]$InputFile,

    [string]$OutputRoot,

    [string]$ExistingStemsRoot,

    [ValidateSet('bowed_strings', 'brass', 'woodwind', 'synth', 'keys', 'percussion')]
    [string[]]$Targets = @('bowed_strings', 'brass', 'woodwind', 'synth', 'keys', 'percussion'),

    [switch]$KeepDecodedWav
)

$ErrorActionPreference = 'Stop'
Set-StrictMode -Version Latest
$env:PYTHONUTF8 = '1'

$projectRoot = (Resolve-Path (Join-Path $PSScriptRoot '..\..\..')).Path
$python = Join-Path $projectRoot '.venv\Scripts\python.exe'
$msst = Join-Path $projectRoot '.venv\Scripts\msst.exe'
$modelRoot = Join-Path $projectRoot 'models\experimental\mvsep-mega-53'
$workRoot = Join-Path $projectRoot '.work\experiments\other-refinement'
$partitionScript = Join-Path $PSScriptRoot 'partition-other.py'
$env:MPLCONFIGDIR = Join-Path $projectRoot '.work\matplotlib'

if (-not $OutputRoot) {
    $OutputRoot = Join-Path $projectRoot 'outputs\experiments\other-refinement'
}
if (-not $ExistingStemsRoot) {
    $ExistingStemsRoot = Join-Path $projectRoot 'outputs\6-stem'
}

foreach ($required in @($python, $msst, $partitionScript)) {
    if (-not (Test-Path -LiteralPath $required -PathType Leaf)) {
        throw "Required file not found: $required"
    }
}

$source = Get-Item -LiteralPath $InputFile
$trackName = [System.IO.Path]::GetFileNameWithoutExtension($source.Name)
$existingOther = Join-Path (Join-Path $ExistingStemsRoot $trackName) "${trackName}_other.wav"
if (-not (Test-Path -LiteralPath $existingOther -PathType Leaf)) {
    throw "Existing six-stem other track not found: $existingOther. Run run-bs-roformer.ps1 first."
}

$workDir = Join-Path $workRoot $trackName
$decodedWav = Join-Path $workDir "$trackName.wav"
$trackOutput = Join-Path $OutputRoot $trackName
$rawOutput = Join-Path $trackOutput 'raw_candidates'
$consistentOutput = Join-Path $trackOutput 'consistent_stems'

New-Item -ItemType Directory -Force -Path $workDir, $rawOutput, $consistentOutput, $env:MPLCONFIGDIR | Out-Null

$ffmpeg = (& $python -c "import imageio_ffmpeg; print(imageio_ffmpeg.get_ffmpeg_exe())").Trim()
if (-not (Test-Path -LiteralPath $ffmpeg -PathType Leaf)) {
    throw "FFmpeg executable not found: $ffmpeg"
}

Write-Host "Decoding original mix: $($source.FullName)"
& $ffmpeg -hide_banner -loglevel error -y -i $source.FullName -vn -map_metadata -1 -ac 2 -ar 44100 -c:a pcm_f32le $decodedWav
if ($LASTEXITCODE -ne 0) {
    throw "FFmpeg failed with exit code $LASTEXITCODE"
}

foreach ($target in $Targets) {
    $modelBase = "bs_mega_53stem_${target}_mvsep"
    $config = Join-Path $modelRoot "$modelBase.yaml"
    $checkpoint = Join-Path $modelRoot "$modelBase.ckpt"
    foreach ($asset in @($config, $checkpoint)) {
        if (-not (Test-Path -LiteralPath $asset -PathType Leaf)) {
            throw "Model asset not found: $asset"
        }
    }

    Write-Host "Separating candidate: $target"
    & $msst inference `
        --model_type bs_roformer `
        --config_path $config `
        --start_check_point $checkpoint `
        --input_folder $workDir `
        --store_dir $rawOutput `
        --device_ids 0 `
        --pcm_type FLOAT `
        --filename_template '{instr}' `
        --disable_detailed_pbar
    if ($LASTEXITCODE -ne 0) {
        throw "MSST failed for target: $target"
    }
}

Write-Host 'Projecting candidates into the existing other stem'
& $python $partitionScript `
    --other $existingOther `
    --candidates-dir $rawOutput `
    --output-dir $consistentOutput `
    --targets $Targets
if ($LASTEXITCODE -ne 0) {
    throw "Other-stem partitioning failed with exit code $LASTEXITCODE"
}

if (-not $KeepDecodedWav -and (Test-Path -LiteralPath $decodedWav -PathType Leaf)) {
    Remove-Item -LiteralPath $decodedWav
}

Write-Host "Completed: $trackOutput"
