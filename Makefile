PY ?= $(CURDIR)/.venv/bin/python

.PHONY: test synth deploy
test:
	cd backend && $(PY) -m pytest -q

synth:
	cd infra && npx cdk synth

deploy:
	bash scripts/deploy.sh
