"""Set RIME_SCHEMA_COMPARE to a checkout with lib/rime.dll to run this smoke test."""

import ctypes
import os
import sys
import unittest
from pathlib import Path
from tempfile import TemporaryDirectory


ROOT = Path(__file__).resolve().parents[2]
COMPARE = os.environ.get('RIME_SCHEMA_COMPARE')
SCHEMA = 'moqi_wan_ms_wb'


@unittest.skipUnless(COMPARE, 'Set RIME_SCHEMA_COMPARE to run librime checks')
class MicrosoftUserDict(unittest.TestCase):
    def test_ac_learns_words_with_and_without_semicolon(self):
        compare = Path(COMPARE).resolve()
        sys.path.insert(0, str(compare / 'src'))
        from rime_schema_compare.call_librime import RimeDllWrapper

        with TemporaryDirectory(prefix='rime-ms-user-dict-') as temp:
            (Path(temp) / 'default.custom.yaml').write_text(
                f'patch:\n  schema_list:\n    - schema: {SCHEMA}\n', encoding='utf-8')
            # Prevent fallback to a previously trained table in shared_data_dir.
            (Path(temp) / 'user.custom.dict.txt').write_text(
                '# Rime table\n#@/db_name\tuser.custom.dict\n#@/db_type\ttabledb\n', encoding='utf-8')
            ime = RimeDllWrapper(dll_path=str(compare / 'lib/rime.dll'))
            ime.initialize(app_name='rime.ms.user.dict.test', shared_data_dir=str(ROOT),
                           user_data_dir=temp)
            try:
                process_key = ime.dll.RimeProcessKey
                process_key.argtypes = [ctypes.c_size_t, ctypes.c_int, ctypes.c_int]
                process_key.restype = ctypes.c_int

                def type_keys(keys):
                    session = ime.create_session()
                    self.assertTrue(session)
                    try:
                        self.assertTrue(ime.select_schema(session, SCHEMA))
                        for key in keys:
                            self.assertTrue(process_key(session, ord(key), 0), keys)
                        return (ime.get_context(session) or {}).get('candidates') or []
                    finally:
                        ime.destroy_session(session)

                for code, text in (('dlqtskd;', '带却扫定'), ('bafuef', '吧弗恩')):
                    with self.subTest(code=code):
                        def learned(candidates):
                            return any(c['text'] == text and c.get('comment') == '*'
                                       for c in candidates)

                        self.assertFalse(learned(type_keys(code)))
                        self.assertEqual([c['text'] for c in type_keys('ac' + code)[:1]], [text])
                        type_keys('ac' + code + ' ')
                        self.assertTrue(learned(type_keys(code)))
                self.assertIn('皴', [c['text'] for c in type_keys('cpcw/')])
            finally:
                ime.finalize()


if __name__ == '__main__':
    unittest.main()
