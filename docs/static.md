# Static

The following methods call Veracode REST APIs and return JSON.

## Static CLI

Commands to work with the Static CLI scans, aka Pipeline Scan. The workflow to run a scan is as follows:
- Create a scan
- Add one or more segments
- Start the scan
- Get findings

- `StaticCLI().Scans().create(binary_name, binary_size, binary_hash, app_id(opt), project_name(opt), project_uri(opt), project_ref(opt), commit_hash(opt), dev_stage(opt), scan_timeout (opt))` - Set up a scan
- `StaticCLI().Scans().get(scan_id)` - Get scan details for the scan represented by `scan_id`.
- `StaticCLI().Scans().Segments().add(scan_id,segment_id,file)` - Upload a segment of the scanned file.
- `StaticCLI().Scans().start(scan_id)` - Start the scan represented by `scan_id`.
- `StaticCLI().Scans().cancel(scan_id)` - Cancel the scan represented by `scan_id`.
- `StaticCLI().Scans().Findings().get(scan_id)` - Get the findings for the scan represented by `scan_id`.
