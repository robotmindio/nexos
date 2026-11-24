.PHONY: verify-spec test-spec
verify-spec:
	python3 scripts/validate_spec.py --report evidence/spec-validation.json

test-spec:
	python3 -m unittest discover -s scripts/tests -v
