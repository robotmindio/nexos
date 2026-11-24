"""Negative controls for the specification checker, not runtime conformance."""
import copy
import json
from pathlib import Path
import sys
import tempfile
import unittest

sys.path.insert(0,str(Path(__file__).resolve().parents[1]))
import validate_spec as spec


class SpecificationChecks(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.schema=spec.load_json(spec.ROOT/'contracts/nexos.schema.json')
        cls.cases=spec.load_json(spec.ROOT/'contracts/examples.json')['cases']
        cls.plan=spec.load_json(spec.ROOT/'program/plan.json')
        cls.state=spec.load_json(spec.ROOT/'program/state.json')
        cls.matrix=spec.load_json(spec.ROOT/'conformance/matrix.json')
        cls.valid={x['definition']:x['instance'] for x in cls.cases if x['id']==x['definition']+'-valid'}
        cls.catalog={(cls.valid['capability']['id'],cls.valid['capability']['version']):cls.valid['capability']}

    def test_fixture_expectations(self):
        for case in self.cases:
            with self.subTest(case=case['id']):
                errors=spec.validate_case(self.schema,case,self.catalog)
                self.assertEqual(not errors,case['expected']=='valid',str(errors))

    def test_duplicate_json_key_rejected(self):
        with tempfile.TemporaryDirectory() as d:
            p=Path(d)/'duplicate.json';p.write_text('{"allowed":false,"allowed":true}')
            with self.assertRaisesRegex(ValueError,'duplicate JSON key'):
                spec.load_json(p)

    def test_nonfinite_json_number_rejected(self):
        with tempfile.TemporaryDirectory() as d:
            p=Path(d)/'nan.json';p.write_text('{"ceiling":NaN}')
            with self.assertRaisesRegex(ValueError,'non-finite'):
                spec.load_json(p)

    def test_dependency_cycle_rejected(self):
        plan=copy.deepcopy(self.plan)
        plan['packages'][0]['depends_on']=['P01']
        self.assertTrue(any('cycle' in x for x in spec.graph_errors(plan)))

    def test_unknown_dependency_rejected(self):
        plan=copy.deepcopy(self.plan);plan['packages'][0]['depends_on']=['P99']
        self.assertTrue(any('unknown dependency' in x for x in spec.graph_errors(plan)))

    def test_duplicate_package_rejected(self):
        plan=copy.deepcopy(self.plan);plan['packages'].append(copy.deepcopy(plan['packages'][0]))
        self.assertTrue(any('duplicate package' in x for x in spec.graph_errors(plan)))

    def test_asymmetric_traceability_rejected(self):
        matrix=copy.deepcopy(self.matrix)
        matrix['experiences'][0]['packages']=[]
        self.assertTrue(any('reciprocal' in x for x in spec.traceability_errors(self.plan,matrix)))

    def test_profile_missing_dependency_rejected(self):
        plan=copy.deepcopy(self.plan);plan['release_profiles'][0]['requires'].remove('P02')
        self.assertTrue(any('dependency-closed' in x for x in spec.traceability_errors(plan,self.matrix)))

    def test_qualified_package_without_evidence_rejected(self):
        state=copy.deepcopy(self.state);state['packages']['P00']['status']='qualified'
        self.assertTrue(any('without evidence' in x for x in spec.state_errors(self.plan,state)))

    def test_blocked_without_reason_rejected(self):
        state=copy.deepcopy(self.state);state['packages']['P00']['status']='blocked'
        self.assertTrue(any('concrete blocker' in x for x in spec.state_errors(self.plan,state)))

    def test_specification_evidence_cannot_qualify(self):
        with tempfile.TemporaryDirectory() as d:
            root=Path(d);(root/'contracts').mkdir()
            (root/'contracts/nexos.schema.json').write_text(json.dumps(self.schema))
            (root/'spec.json').write_text(json.dumps(self.valid['evidence']))
            errors=spec.evidence_reference_errors(['spec.json'],root,subject='P00')
            self.assertTrue(any('cannot qualify runtime' in x for x in errors))

    def test_minimal_true_flags_are_not_evidence(self):
        with tempfile.TemporaryDirectory() as d:
            root=Path(d);(root/'contracts').mkdir()
            (root/'contracts/nexos.schema.json').write_text(json.dumps(self.schema))
            (root/'fake.json').write_text(json.dumps({'validation_kind':'runtime_vm','example_only':False,'result':'passed','qualifies_runtime':True}))
            self.assertTrue(any('invalid qualification evidence' in x for x in spec.evidence_reference_errors(['fake.json'],root)))

    def test_evidence_path_cannot_escape_repository(self):
        errors=spec.evidence_reference_errors(['../../outside.json'],spec.ROOT)
        self.assertTrue(any('missing or escaping' in x for x in errors))

    def test_qualified_profile_requires_qualified_dependencies(self):
        state=copy.deepcopy(self.state);state['profiles']['local-runtime']['status']='qualified'
        for key in self.plan['release_profiles'][0]['requires']:
            state['packages'][key]['status']='implemented'
        errors=spec.state_errors(self.plan,state)
        self.assertTrue(any('not qualified' in x for x in errors))
        self.assertTrue(any('procedure P14 not implemented' in x for x in errors))

    def test_prepare_has_no_client_digest_or_approval(self):
        case=next(x for x in self.cases if x['id']=='request-prepare-valid')
        self.assertNotIn('action_digest',case['instance']['params'])
        self.assertFalse(spec.validate_case(self.schema,case))
        bad=copy.deepcopy(case);bad['instance']['params']['action_digest']='sha256:'+'a'*64
        self.assertTrue(spec.validate_case(self.schema,bad))

    def test_nonlocal_schema_reference_rejected_without_fetch(self):
        self.assertIn('embedded schema uses non-local reference',spec.schema_policy_errors({'$ref':'http://127.0.0.1:1/secret'}))

    def test_schema_depth_is_bounded(self):
        value={'type':'object'}
        for _ in range(40):value={'properties':{'child':value}}
        self.assertTrue(any('depth' in x for x in spec.schema_policy_errors(value)))

    def test_view_query_cannot_mask_fixture_mutation(self):
        value=copy.deepcopy(self.valid['view']);value['bindings'][0]['mode']='query'
        errors=spec.validate_case(self.schema,{'definition':'view','instance':value},self.catalog)
        self.assertTrue(any('mutating' in x for x in errors))

    def test_unknown_scope_id_rejected(self):
        _, errors=spec.resolve_scope({'package_ids':['P99'],'milestone_ids':[],'release_profile_ids':[]},self.plan)
        self.assertTrue(any('unknown scope ID' in x for x in errors))

    def test_milestone_scope_resolves_packages(self):
        covered,errors=spec.resolve_scope({'package_ids':[],'milestone_ids':['M1'],'release_profile_ids':[]},self.plan)
        self.assertFalse(errors)
        self.assertIn('P05',covered)

    def test_active_state_cannot_use_template(self):
        state=copy.deepcopy(self.state)
        state['packages']['P00']['checkpoint']='program/checkpoint-template.json'
        self.assertTrue(any('invalid active checkpoint' in x for x in spec.state_errors(self.plan,state)))

    def test_program_metadata_rejects_global_qualification(self):
        schema=spec.load_json(spec.ROOT/'contracts/program.schema.json')
        state=copy.deepcopy(self.state);state['qualification']='qualified'
        wrapper={'$schema':schema['$schema'],'$defs':schema['$defs'],'$ref':'#/$defs/state'}
        self.assertTrue(list(spec.Draft202012Validator(wrapper).iter_errors(state)))

    def test_p00_can_use_scoped_spec_evidence_without_runtime_claim(self):
        # Synthetic in-memory records test the classification rule only.
        with tempfile.TemporaryDirectory() as d:
            root=Path(d);(root/'contracts').mkdir()
            (root/'contracts/nexos.schema.json').write_text(json.dumps(self.schema))
            evidence=copy.deepcopy(self.valid['evidence'])
            evidence.update(example_only=False)
            evidence['coverage']['packages']=['P00']
            (root/'inventory.json').write_text(json.dumps(evidence))
            self.assertFalse(spec.evidence_reference_errors(['inventory.json'],root,subject='P00',qualification_kind='specification'))
            self.assertTrue(spec.evidence_reference_errors(['inventory.json'],root,subject='P01',qualification_kind='runtime'))

    def test_runtime_evidence_cannot_cover_unrelated_package(self):
        with tempfile.TemporaryDirectory() as d:
            root=Path(d);(root/'contracts').mkdir()
            (root/'contracts/nexos.schema.json').write_text(json.dumps(self.schema))
            evidence=copy.deepcopy(self.valid['evidence'])
            evidence.update(example_only=False,validation_kind='runtime_vm',qualifies_runtime=True,repository_commit='c'*40)
            evidence['environment']['provider_build_digests']=['sha256:'+'a'*64]
            evidence['coverage']['packages']=['P01']
            (root/'scoped.json').write_text(json.dumps(evidence))
            self.assertTrue(any('does not cover package P02' in x for x in spec.evidence_reference_errors(['scoped.json'],root,subject='P02')))


if __name__=='__main__':
    unittest.main()
