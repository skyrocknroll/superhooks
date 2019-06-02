import unittest

import mock


class SuperHooksTests(unittest.TestCase):
    url = 'http://localhost:8090/'
    unexpected_err_msg = 'bar:foo;BACKOFF;PROCESS_STATE_FATAL;processname:foo groupname:bar from_state:BACKOFF '
    events = 'FATAL,EXITED'

    def _get_target_class(self):
        from superhooks.superhooks import SuperHooks
        return SuperHooks

    def _make_one_mocked(self, **kwargs):
        kwargs['url'] = kwargs.get('url', self.url)
        kwargs['events'] = kwargs.get('events', self.events)

        obj = self._get_target_class()(**kwargs)
        obj.send_message = mock.Mock()
        return obj

    def get_process_fatal_event(self, pname, gname):
        headers = {
            'ver': '3.0', 'poolserial': '7', 'len': '71',
            'server': 'supervisor', 'eventname': 'PROCESS_STATE_FATAL',
            'serial': '7', 'pool': 'superhooks',
        }
        payload = 'processname:{} groupname:{} from_state:BACKOFF'.format(pname, gname)
        return (headers, payload)

    def test_get_process_state_change_msg(self):
        crash = self._make_one_mocked()
        hdrs, payload = self.get_process_fatal_event('foo', 'bar')
        msg = crash.get_process_state_change_msg(hdrs, payload)
        self.assertEqual(self.unexpected_err_msg, msg)


if __name__ == '__main__':
    unittest.main()
