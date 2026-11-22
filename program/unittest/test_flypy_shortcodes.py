"""Flypy 出简让全 regression checks.

Run with Python alone, or set RIME_SCHEMA_COMPARE to a local checkout with
lib/rime.dll (librime with Lua) to also deploy and query the schema.
"""

import os
import re
import sys
import unittest
from pathlib import Path
from tempfile import TemporaryDirectory


ROOT = Path(__file__).resolve().parents[2]
TABLE = ROOT / 'custom_phrase/custom_phrase_cjrq_for_xh.txt'
COMPARE = os.environ.get('RIME_SCHEMA_COMPARE')

# Same Flypy syllable; replace the copied 墨奇 shape with the shipped 鹤形 shape.
# Keep the full spelling here to verify the short/full relationship in librime.
CORRECTIONS = (
    ('曹', 'ccc', 'ccao'),
    ('鲷', 'dny', 'dnak'),
    ('骨', 'gug', 'gulo'),
    ('徽', 'hvr', 'hviw'),
    ('奖', 'jll', 'jldd'),
    ('袅', 'nnn', 'nnpy'),
    ('鸥', 'ouq', 'oukn'),
    ('贫', 'pbf', 'pbbr'),
    ('期', 'qic', 'qiqo'),
    ('鲭', 'qky', 'qkao'),
    ('瓤', 'rhy', 'rhwg'),
    ('飕', 'szf', 'szjy'),
    ('状', 'vll', 'vldq'),
    ('卓', 'vob', 'volu'),
    ('瓮', 'wgg', 'wgbw'),
    ('凶', 'xsk', 'xsxk'),
    ('繇', 'yzv', 'yzpx'),
)

# The established Flypy three-key candidate keeps its shortcut. The same
# four-key candidate as the Moqi table gets priority only with a trailing /.
FULL_CODE_HANDOFFS = (
    ('拔', '捌', 'bafd/'),
    ('惑', '夥', 'hogx/'),
    ('架', '驾', 'jxlm/'),
    ('碎', '尿', 'svuu/'),
    ('飕', '锼', 'szjy/'),
    ('咂', '匝', 'zakj/'),
)


class FlypyShortcodes(unittest.TestCase):
    def test_short_table(self):
        rows = [line.split('\t') for line in TABLE.read_text(encoding='utf-8').splitlines()]
        entries = set()
        for char, code, *weight in rows:
            self.assertEqual(len(char), 1)
            self.assertTrue(re.fullmatch(r'[a-z]{2,3}|[a-z]{4}/', code), (char, code))
            self.assertTrue(not weight or len(weight) == 1 and weight[0].isdigit())
            self.assertFalse((char, code) in entries, f'Duplicate row: {char} {code}')
            entries.add((char, code))

        for char, old, full in CORRECTIONS:
            with self.subTest(char=char):
                self.assertNotIn((char, old), entries)
                self.assertIn((char, full[:3]), entries)
        for char, code in (('试', 'uiyg/'), ('围', 'wwkw/'), ('翻', 'fjp'),
                           ('噢', 'ook'), ('嘛', 'mak')):
            self.assertIn((char, code), entries)
        self.assertIn(['她', 'ta', '1'], rows)

        for short, full, code in FULL_CODE_HANDOFFS:
            with self.subTest(code=code):
                self.assertIn((short, code[:3]), entries)
                self.assertEqual([char for char, candidate in entries if candidate == code],
                                 [full])

    @unittest.skipUnless(COMPARE, 'Set RIME_SCHEMA_COMPARE to run librime checks')
    def test_librime_candidates(self):
        compare = Path(COMPARE).resolve()
        sys.path.insert(0, str(compare / 'src'))
        from rime_schema_compare.call_librime import RimeDllWrapper

        schema = 'moqi_wan_flypy'
        with TemporaryDirectory(prefix='rime-flypy-test-') as temp:
            (Path(temp) / 'default.custom.yaml').write_text(
                f'patch:\n  schema_list:\n    - schema: {schema}\n', encoding='utf-8')
            ime = RimeDllWrapper(dll_path=str(compare / 'lib/rime.dll'))
            ime.initialize(app_name='rime.flypy.test', shared_data_dir=str(ROOT),
                           user_data_dir=temp)
            try:
                session = ime.create_session()
                self.assertTrue(session)
                try:
                    self.assertTrue(ime.select_schema(session, schema))

                    def candidates(code):
                        self.assertTrue(ime.feed_input(session, code), code)
                        context = ime.get_context(session) or {}
                        return [candidate['text'] for candidate in context.get('candidates', [])]

                    for char, old, full in CORRECTIONS:
                        with self.subTest(char=char):
                            self.assertEqual(candidates(full[:3])[:1], [char])
                            self.assertIn(char, candidates(full + '/'))
                            # The old code can still expose fallback candidates (e.g. 鸥).
                            self.assertNotEqual(candidates(old)[:1], [char])
                    for short, full, code in FULL_CODE_HANDOFFS:
                        with self.subTest(code=code):
                            self.assertEqual(candidates(code[:3])[:1], [short])
                            self.assertEqual(candidates(code)[:2], [full, short])
                            self.assertNotEqual(candidates(code[:-1])[:1], [full])
                    for char, code in (('试', 'uiyg/'), ('围', 'wwkw/'), ('翻', 'fjp'),
                                       ('曲', 'qul'), ('唉', 'aiku/')):
                        with self.subTest(code=code):
                            self.assertEqual(candidates(code)[:1], [char])
                finally:
                    ime.destroy_session(session)
            finally:
                ime.finalize()


if __name__ == '__main__':
    unittest.main()
