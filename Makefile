PYTHON ?= python3
SETUP_PYTHON ?= python3.13
FGTOOLS = .venv/bin/fgtools
BASE ?= main
RUNEBENDER_REPO ?= $(HOME)/GH/repos/runebender
RUN_NATIVE = cd "$(RUNEBENDER_REPO)" && cargo run --quiet --locked --
DESIGNSPACE = $(CURDIR)/sources/Blocksync.designspace
BUILD = $(if $(NO_BUILD),,build)
VENV = .venv
VENV_PYTHON = $(VENV)/bin/python
export PATH := $(CURDIR)/.venv/bin:$(PATH)

GF_REPO_PATH ?= /Users/eli/GH/forks/fonts
GF_CLEAN_REPO_PATH ?= /private/tmp/blocksync-google-fonts
VALUES ?= documentation/google-fonts-final-values.template.json

.PHONY: help setup venv build qa test proof reports source-readiness warning-worklist metadata-reachability-cleanup placeholder-audit decision-application-check family-name-readiness authorship-disclosure-readiness packager-source-strategy proof-review-readiness proof-review-packet release-metadata-readiness metadata-check metadata-final-check package-context-check release-archive-build release-archive-check prepare-gf-clean-checkout final-values-packet final-values-proposal maintainer-decision-request final-values-check apply-final-values package-dry-run-readiness packager-dry-run-record downstream-pr-draft downstream-pr-readiness submission-handoff-readiness google-fonts-reference-refresh agent-porting-manifest agent-reuse-readiness next-actions blockers script-gate-tests package-dry-run final-readiness-check release-check preflight preflight-only clean

help:
	@printf '%s\n' \
		'Blocksync / Font.Garden workflow:' \
		'  make status / queue    Show grades and component dependencies' \
		'  make runebender       Open the designspace in the native checkout' \
		'  make check-changes BASE=... GLYPHS=... MASTERS=...  Verify a draft batch' \
		'  make diff / render / proof-web / specimen / media / site  Proofing tools' \
		'  make setup          Create venv and install requirements' \
		'  make build          Build variable and static TTFs into fonts/' \
		'  make qa             Build, then run Fontspector Google Fonts profile' \
		'  make test           Check project structure and pinned Font.Garden QA' \
		'  make proof          Build, then generate the Font.Garden PDF and width proof' \
		'  make reports        Regenerate release/readiness reports' \
		'  make source-readiness Validate designspace/UFO source readiness' \
		'  make warning-worklist Generate the Fontspector warning worklist' \
		'  make metadata-reachability-cleanup Inspect unsafe support-mark unencoding path' \
		'  make placeholder-audit Audit unresolved Google Fonts handoff placeholders' \
		'  make decision-application-check Map decisions to metadata/package/PR blockers' \
		'  make family-name-readiness Report family-name and RFN readiness' \
		'  make authorship-disclosure-readiness Report authorship/disclosure readiness' \
		'  make packager-source-strategy Report source.config_yaml/archive strategy readiness' \
		'  make proof-review-readiness Report visual proof review readiness' \
		'  make proof-review-packet Generate maintainer proof/WARN review packet' \
		'  make release-metadata-readiness Report date_added/source.commit readiness' \
		'  make metadata-check Build, then verify downstream metadata draft' \
		'  make package-context-check Build, then run package-context Fontspector' \
		'  make release-archive-build Build local fallback release/archive zip' \
		'  make release-archive-check Regenerate release/archive manifest only' \
		'  make prepare-gf-clean-checkout Prepare isolated google/fonts checkout' \
		'  make final-values-packet Generate maintainer final-values answer packet' \
		'  make final-values-proposal Generate non-final values proposal JSON' \
		'  make maintainer-decision-request Generate concise final-answer request' \
		'  make final-values-check VALUES=path Validate final values JSON' \
		'  make apply-final-values VALUES=path Apply final values JSON to drafts' \
		'  make package-dry-run-readiness Report guarded no-PR Packager dry-run readiness' \
		'  make packager-dry-run-record Report final no-PR Packager run evidence' \
		'  make downstream-pr-draft Generate downstream PR title/body draft' \
		'  make downstream-pr-readiness Report downstream Google Fonts PR readiness' \
		'  make submission-handoff-readiness Check Add Font issue/handoff staleness' \
		'  make google-fonts-reference-refresh Check live-reference refresh record' \
		'  make agent-porting-manifest Generate reusable workflow copy manifest' \
		'  make agent-reuse-readiness Report reusable agent workflow readiness' \
		'  make next-actions   Report owner-grouped Google Fonts next actions' \
		'  make blockers       Report final Google Fonts submission blockers' \
		'  make script-gate-tests Run release-script guard tests' \
		'  make package-dry-run Run guarded no-PR Packager dry run after final metadata' \
		'  make final-readiness-check Fail until final submission blockers are resolved' \
		'  make release-check   Build once, then run all release handoff gates' \
		'  make preflight      Build, then run release-structure checks' \
		'  make preflight-only Run release-structure checks without building' \
		'  make clean          Remove generated build outputs and venv'

setup: $(VENV)/.fontgarden-tools

venv: setup

$(VENV)/.fontgarden-tools: requirements.txt requirements.in
	test -x $(VENV_PYTHON) || $(SETUP_PYTHON) -m venv $(VENV)
	$(VENV_PYTHON) -m pip install -r requirements.txt
	$(FGTOOLS) install-tools
	touch $@

build: setup
	./build.sh

qa: $(BUILD)
	./scripts/check_gf_fonts.sh

test: $(BUILD) preflight-only
	$(VENV_PYTHON) sources/test_assignment.py
	$(VENV_PYTHON) sources/check_layout.py
	$(FGTOOLS) qa

namecheck-live: $(BUILD)
	$(VENV)/bin/fontspector -p googlefonts --checkid fontdata_namecheck --error-code-on fail fonts/variable/*.ttf

test-google-fonts: $(BUILD)
	$(FGTOOLS) qa --checks google-fonts

test-fontgarden: $(BUILD)
	$(FGTOOLS) qa --checks fontgarden

proof: $(BUILD)
	$(FGTOOLS) media --proof $(PAGE)
	$(VENV_PYTHON) sources/width_proof.py

# The existing GF handoff checks its separate Diffenator2 proof bundle.
proof-legacy: $(BUILD)
	test -x venv/bin/diffenator2 || $(SETUP_PYTHON) -m venv venv
	test -x venv/bin/diffenator2 || venv/bin/python -m pip install diffenator2==0.5.0
	mkdir -p out/proof
	PATH="$(CURDIR)/venv/bin:$$PATH" venv/bin/diffenator2 proof fonts/variable/*.ttf fonts/ttf/*.ttf -o out/proof
	$(VENV_PYTHON) scripts/build_proof_index.py
	$(VENV_PYTHON) scripts/report_proof_review_readiness.py
	$(VENV_PYTHON) scripts/report_proof_review_packet.py

runebender:
	$(RUN_NATIVE) "$(DESIGNSPACE)"

runebender-mcp:
	@$(RUN_NATIVE) mcp --live

runebender-font-mcp:
	@$(RUN_NATIVE) mcp --font "$(DESIGNSPACE)"

runebender-cli:
	cd "$(RUNEBENDER_REPO)" && cargo build --quiet --locked --bin runebender

status:
	$(FGTOOLS) status

queue:
	$(FGTOOLS) queue

check-design: runebender-cli
	PATH="$(RUNEBENDER_REPO)/target/debug:$$PATH" $(FGTOOLS) check-design $(if $(GLYPHS),$(GLYPHS),--not-green)

check-changes:
	$(VENV_PYTHON) sources/check_assignment.py --base "$(BASE)" --glyphs "$(GLYPHS)" --masters "$(MASTERS)"

render: runebender-cli
	@test -n "$(GLYPHS)"
	PATH="$(RUNEBENDER_REPO)/target/debug:$$PATH" $(FGTOOLS) render "$(GLYPHS)" --base "$(BASE)"

diff:
	$(FGTOOLS) diff --base "$(BASE)"

proof-web: $(BUILD)
	$(FGTOOLS) proof-web --current

specimen: $(BUILD)
	$(FGTOOLS) media --specimen $(PAGE)

media: $(BUILD)
	$(FGTOOLS) media $(FORMAT) $(if $(CANVAS),--canvas $(CANVAS),)

formats:
	$(FGTOOLS) media --list

site: proof specimen media
	$(FGTOOLS) site
	cp output/proof/widths.html output/site/widths.html
	cp fonts/variable/*.ttf output/site/

.PHONY: namecheck-live proof-legacy test-google-fonts test-fontgarden status queue check-design check-changes render diff runebender runebender-mcp runebender-font-mcp runebender-cli proof-web specimen media formats site

reports: agent-reuse-readiness

warning-worklist:
	$(VENV_PYTHON) scripts/report_zero_warning_worklist.py

metadata-reachability-cleanup:
	$(VENV_PYTHON) scripts/remove_unreachable_support_mark_unicodes.py

placeholder-audit:
	$(VENV_PYTHON) scripts/report_open_placeholders.py

decision-application-check: placeholder-audit
	$(VENV_PYTHON) scripts/report_decision_application_blockers.py

source-readiness: venv
	$(VENV_PYTHON) scripts/report_source_readiness.py

family-name-readiness: build
	$(VENV_PYTHON) scripts/report_family_name_readiness.py

authorship-disclosure-readiness:
	$(VENV_PYTHON) scripts/report_authorship_disclosure_readiness.py

packager-source-strategy:
	$(VENV_PYTHON) scripts/report_packager_source_strategy.py

proof-review-readiness:
	$(VENV_PYTHON) scripts/report_proof_review_readiness.py

proof-review-packet: proof-review-readiness
	$(VENV_PYTHON) scripts/report_proof_review_packet.py

release-metadata-readiness: build
	$(VENV_PYTHON) scripts/report_release_metadata_readiness.py

metadata-check: build
	$(VENV_PYTHON) scripts/check_downstream_metadata.py --require-font

metadata-final-check: build
	$(VENV_PYTHON) scripts/check_downstream_metadata.py --require-font --final

package-context-check: build
	$(VENV_PYTHON) scripts/check_package_context.py

release-archive-build: build
	$(VENV_PYTHON) scripts/build_release_archive.py

release-archive-check:
	$(VENV_PYTHON) scripts/build_release_archive.py --check-only

prepare-gf-clean-checkout:
	GF_CLEAN_REPO_PATH="$(GF_CLEAN_REPO_PATH)" bash scripts/prepare_clean_gf_checkout.sh

final-values-packet:
	$(VENV_PYTHON) scripts/report_final_values_packet.py

final-values-proposal:
	$(VENV_PYTHON) scripts/report_final_values_proposal.py

maintainer-decision-request:
	$(VENV_PYTHON) scripts/report_maintainer_decision_request.py

final-values-check:
	$(VENV_PYTHON) scripts/apply_final_values.py --values "$(VALUES)"

apply-final-values:
	$(VENV_PYTHON) scripts/apply_final_values.py --values "$(VALUES)" --apply

package-dry-run-readiness:
	GF_REPO_PATH="$(GF_REPO_PATH)" GF_CLEAN_REPO_PATH="$(GF_CLEAN_REPO_PATH)" $(VENV_PYTHON) scripts/report_package_dry_run_readiness.py

packager-dry-run-record:
	$(VENV_PYTHON) scripts/report_packager_dry_run_record.py

downstream-pr-draft:
	$(VENV_PYTHON) scripts/report_downstream_pr_draft.py

downstream-pr-readiness:
	$(VENV_PYTHON) scripts/report_downstream_pr_draft.py
	GF_REPO_PATH="$(GF_REPO_PATH)" GF_CLEAN_REPO_PATH="$(GF_CLEAN_REPO_PATH)" $(VENV_PYTHON) scripts/report_downstream_pr_readiness.py

submission-handoff-readiness:
	$(VENV_PYTHON) scripts/report_submission_handoff_readiness.py

google-fonts-reference-refresh:
	$(VENV_PYTHON) scripts/report_google_fonts_reference_refresh.py

agent-porting-manifest:
	$(VENV_PYTHON) scripts/report_agent_porting_manifest.py

agent-reuse-readiness:
	$(VENV_PYTHON) scripts/report_google_fonts_reference_refresh.py
	$(VENV_PYTHON) scripts/report_release_metadata_readiness.py
	$(VENV_PYTHON) scripts/report_family_name_readiness.py
	$(VENV_PYTHON) scripts/report_authorship_disclosure_readiness.py
	$(VENV_PYTHON) scripts/report_packager_source_strategy.py
	$(VENV_PYTHON) scripts/report_proof_review_readiness.py
	$(VENV_PYTHON) scripts/report_proof_review_packet.py
	GF_REPO_PATH="$(GF_REPO_PATH)" GF_CLEAN_REPO_PATH="$(GF_CLEAN_REPO_PATH)" $(VENV_PYTHON) scripts/report_package_dry_run_readiness.py
	$(VENV_PYTHON) scripts/report_packager_dry_run_record.py
	$(VENV_PYTHON) scripts/report_downstream_pr_draft.py
	GF_REPO_PATH="$(GF_REPO_PATH)" GF_CLEAN_REPO_PATH="$(GF_CLEAN_REPO_PATH)" $(VENV_PYTHON) scripts/report_downstream_pr_readiness.py
	$(VENV_PYTHON) scripts/report_open_placeholders.py
	$(VENV_PYTHON) scripts/report_decision_application_blockers.py
	$(VENV_PYTHON) scripts/report_final_values_packet.py
	$(VENV_PYTHON) scripts/report_final_values_proposal.py
	$(VENV_PYTHON) scripts/report_maintainer_decision_request.py
	$(VENV_PYTHON) scripts/report_next_actions.py
	$(VENV_PYTHON) scripts/report_final_submission_blockers.py
	$(VENV_PYTHON) scripts/report_submission_handoff_readiness.py
	$(VENV_PYTHON) scripts/report_google_fonts_reference_refresh.py
	$(VENV_PYTHON) scripts/report_agent_porting_manifest.py
	$(VENV_PYTHON) scripts/report_agent_reuse_readiness.py

next-actions:
	$(VENV_PYTHON) scripts/report_next_actions.py

blockers:
	$(VENV_PYTHON) scripts/report_final_submission_blockers.py

script-gate-tests: venv
	bash scripts/test_release_archive_gates.sh
	bash scripts/test_package_gf_dry_run_gates.sh
	$(VENV_PYTHON) scripts/test_apply_final_values.py
	$(VENV_PYTHON) scripts/test_agent_porting_manifest.py
	$(VENV_PYTHON) scripts/test_final_values_packet.py
	$(VENV_PYTHON) scripts/test_maintainer_decision_request.py
	$(VENV_PYTHON) scripts/test_packager_dry_run_record.py
	$(VENV_PYTHON) scripts/test_downstream_pr_draft.py

package-dry-run: build
	GF_REPO_PATH="$(GF_REPO_PATH)" bash scripts/package_gf_dry_run.sh

final-readiness-check:
	$(VENV_PYTHON) scripts/check_final_readiness.py

release-check: build
	$(VENV_PYTHON) scripts/report_release_metadata_readiness.py
	$(VENV_PYTHON) scripts/report_source_readiness.py
	$(VENV_PYTHON) scripts/report_family_name_readiness.py
	$(VENV_PYTHON) scripts/report_authorship_disclosure_readiness.py
	./scripts/check_gf_fonts.sh
	$(VENV_PYTHON) scripts/check_downstream_metadata.py --require-font
	$(VENV_PYTHON) scripts/check_package_context.py
	$(VENV_PYTHON) scripts/report_zero_warning_worklist.py
	$(VENV_PYTHON) scripts/build_release_archive.py
	$(VENV_PYTHON) scripts/report_packager_source_strategy.py
	$(VENV_PYTHON) scripts/report_proof_review_readiness.py
	$(VENV_PYTHON) scripts/report_proof_review_packet.py
	GF_REPO_PATH="$(GF_REPO_PATH)" GF_CLEAN_REPO_PATH="$(GF_CLEAN_REPO_PATH)" $(VENV_PYTHON) scripts/report_package_dry_run_readiness.py
	$(VENV_PYTHON) scripts/report_packager_dry_run_record.py
	$(VENV_PYTHON) scripts/report_downstream_pr_draft.py
	GF_REPO_PATH="$(GF_REPO_PATH)" GF_CLEAN_REPO_PATH="$(GF_CLEAN_REPO_PATH)" $(VENV_PYTHON) scripts/report_downstream_pr_readiness.py
	$(VENV_PYTHON) scripts/report_open_placeholders.py
	$(VENV_PYTHON) scripts/report_decision_application_blockers.py
	$(VENV_PYTHON) scripts/report_final_values_packet.py
	$(VENV_PYTHON) scripts/report_final_values_proposal.py
	$(VENV_PYTHON) scripts/report_maintainer_decision_request.py
	$(VENV_PYTHON) scripts/report_next_actions.py
	$(VENV_PYTHON) scripts/report_final_submission_blockers.py
	$(VENV_PYTHON) scripts/report_submission_handoff_readiness.py
	$(VENV_PYTHON) scripts/report_google_fonts_reference_refresh.py
	$(VENV_PYTHON) scripts/report_agent_porting_manifest.py
	$(VENV_PYTHON) scripts/report_agent_reuse_readiness.py
	$(MAKE) script-gate-tests
	$(PYTHON) scripts/gf_preflight.py

preflight: build preflight-only

preflight-only:
	$(PYTHON) scripts/gf_preflight.py

clean:
	rm -rf $(VENV) output build build.ninja .ninja_log fonts out dist build.stamp
	find . -name "*.pyc" -delete
