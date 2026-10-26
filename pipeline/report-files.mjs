// One manifest for publication and content-hash validation.
export function reportFiles(report) {
  const files=['latest.json','latest.md','coverage.json','README.md','cost-curve.svg','snapshots/'+report.report_date+'.json'];
  if(report.workload_selection)files.push('workloads.json','workloads.md','workloads/cost-curves.svg','workloads/snapshots/'+report.report_date+'.json');
  return files;
}
