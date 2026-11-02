from .errors import GateError
from .git import diff_fingerprint


def enforce_publication(config, manifest, states):
    if manifest.get("canceled"):
        raise GateError("run is canceled")
    if not manifest.get("impact_plan", {}).get("frozen"):
        raise GateError("impact plan is not frozen")
    if manifest.get("impact_plan", {}).get("contract_checks") and not manifest.get("contracts_passed"):
        raise GateError("configured cross-service checks have not passed")
    for state in states:
        if state.get("stage") not in {"REVIEWED", "AWAITING_APPROVAL", "COMMITTED", "PUSHED", "PR_CREATED", "PR_CREATED_SYNC_PENDING", "COMPLETED"}:
            raise GateError(f"{state['service_id']} has not passed review")
        current = diff_fingerprint(state["worktree"]) if state.get("stage") in {"REVIEWED", "AWAITING_APPROVAL"} else state.get("reviewed_diff_fingerprint")
        if current != state.get("reviewed_diff_fingerprint"):
            raise GateError(f"{state['service_id']} diff changed after review")
        if not state.get("checks_passed") or state.get("blocking_findings"):
            raise GateError(f"{state['service_id']} has an unresolved verification or review gate")
        if config["policy"].get("publication_mode", "review") == "review" and state.get("publication_required", True):
            approval = state.get("approval_scope", {})
            required = (state["run_id"], state["reviewed_diff_fingerprint"], state["base_ref"])
            actual = (approval.get("run_id"), approval.get("diff_fingerprint"), approval.get("destination"))
            if required != actual or not approval.get("allowed_writes"):
                raise GateError(f"{state['service_id']} lacks revision-bound user approval")
        elif not manifest.get("automatic_authorization"):
            raise GateError("automatic mode lacks recorded run-scoped authorization")
