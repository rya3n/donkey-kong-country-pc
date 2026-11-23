[CmdletBinding()]
param(
    [Parameter(Mandatory)]
    [string]$Executable,

    [ValidatePattern('^[a-fA-F0-9]{64}$')]
    [string]$ExpectedSha256,

    [string]$Dumpbin = 'dumpbin.exe'
)

$ErrorActionPreference = 'Stop'
$file = Get-Item -LiteralPath $Executable
if ($file -isnot [IO.FileInfo]) { throw 'Expected a Windows executable file.' }

$hash = (Get-FileHash -LiteralPath $file.FullName -Algorithm SHA256).Hash.ToLowerInvariant()
if ($ExpectedSha256 -and $hash -ne $ExpectedSha256) {
    throw 'Executable SHA-256 does not match the expected value.'
}

$bytes = [IO.File]::ReadAllBytes($file.FullName)
if ($bytes.Length -lt 64 -or [BitConverter]::ToUInt16($bytes, 0) -ne 0x5A4D) {
    throw 'The file has no DOS executable header.'
}
$peOffset = [int64][BitConverter]::ToUInt32($bytes, 0x3C)
if ($peOffset -lt 64 -or $peOffset -gt $bytes.Length - 24 -or
    [BitConverter]::ToUInt32($bytes, $peOffset) -ne 0x00004550) {
    throw 'The file has no valid PE header.'
}
$optionalOffset = $peOffset + 24
$optionalSize = [BitConverter]::ToUInt16($bytes, $peOffset + 20)
if ($optionalSize -lt 70 -or $optionalOffset + $optionalSize -gt $bytes.Length) {
    throw 'The PE optional header is incomplete.'
}
$machine = [BitConverter]::ToUInt16($bytes, $peOffset + 4)
$characteristics = [BitConverter]::ToUInt16($bytes, $peOffset + 22)
$magic = [BitConverter]::ToUInt16($bytes, $optionalOffset)
$subsystem = [BitConverter]::ToUInt16($bytes, $optionalOffset + 68)
if ($machine -ne 0x8664 -or $magic -ne 0x020B -or $subsystem -ne 2 -or
    ($characteristics -band 0x2002) -ne 0x0002) {
    throw 'Expected an x64 Windows GUI executable.'
}

$tool = Get-Command -Name $Dumpbin -CommandType Application
$dependencies = & $tool.Source /DEPENDENTS $file.FullName
if ($LASTEXITCODE -ne 0) { throw 'DUMPBIN /DEPENDENTS failed.' }
$imports = @($dependencies | ForEach-Object {
    if ($_ -match '^\s+([A-Za-z0-9_.-]+\.dll)\s*$') { $Matches[1].ToLowerInvariant() }
} | Sort-Object -Unique)
if (!$imports) { throw 'DUMPBIN returned no DLL imports.' }

$apiSets = @($imports | Where-Object { $_ -match '^(api|ext)-ms-' })
$sideBySide = @($imports | Where-Object {
    Test-Path -LiteralPath (Join-Path $file.DirectoryName $_) -PathType Leaf
})
$inSystemDirectory = @($imports | Where-Object {
    $_ -notin $apiSets -and
    (Test-Path -LiteralPath (Join-Path ([Environment]::SystemDirectory) $_) -PathType Leaf)
})
$unresolved = @($imports | Where-Object {
    $_ -notin $apiSets -and $_ -notin $sideBySide -and $_ -notin $inSystemDirectory
})
$visualCppRuntime = @($imports | Where-Object {
    $_ -match '^(msvc[pr]\d|vcruntime\d|concrt\d|vcomp\d|ucrtbased\.)'
})
if ((Get-FileHash -LiteralPath $file.FullName -Algorithm SHA256).Hash -ne $hash) {
    throw 'The executable changed during inspection.'
}

[ordered]@{
    executable = $file.Name
    bytes = $bytes.LongLength
    sha256 = $hash
    target = 'windows-x64-gui'
    dll_imports = $imports
    api_sets = $apiSets
    present_beside_executable = $sideBySide
    present_in_system_directory = $inSystemDirectory
    unresolved_on_inspection_host = $unresolved
    visual_cpp_runtime_imports = $visualCppRuntime
} | ConvertTo-Json -Depth 3
