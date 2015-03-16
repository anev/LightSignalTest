import unittest
import json

import Light


class LightTest(unittest.TestCase):
    def setUp(self):
        self.app = Light.app.test_client()

    def test_clear(self):
        resp = self.app.get('/clear')
        parsed = json.loads(resp.data)
        assert parsed["status"] == "ok"

    def test_unknown_sequence(self):
        self.app.get('/clear')
        req = "{'observation': {    'color': 'green',    'numbers': ['1110111', '0011101']  },  'sequence': '12'}"
        resp = self.app.post('/observation/add', data=req)
        parsed = json.loads(resp.data)
        assert parsed['status'] == 'error'

    def test_invalid_format(self):
        req = "{'obse"
        resp = self.app.post('/observation/add', data=req)
        parsed = json.loads(resp.data)
        assert parsed["status"] == "error"
        assert parsed["msg"] == "Invalid input data"

    def test_wrong_color(self):
        req = "{'observation':{'color': 'black', 'numbers': ['1110111', '0011101']}, 'sequence': '12'}"
        resp = self.app.post('/observation/add', data=req)
        parsed = json.loads(resp.data)
        assert parsed['status'] == 'error'
        assert parsed["msg"] == "Invalid input data"

    def test_wrong_numbers(self):
        req = "{'observation':{'color': 'green', 'numbers': ['1110111', '001110']}, 'sequence': '12'}"
        resp = self.app.post('/observation/add', data=req)
        parsed = json.loads(resp.data)
        assert parsed['status'] == 'error'
        assert parsed["msg"] == "Invalid input data"

    def test_wrong_numbers(self):
        req = "{'observation':{'color': 'green', 'numbers': ['111011', '0011101']}, 'sequence': '12'}"
        resp = self.app.post('/observation/add', data=req)
        parsed = json.loads(resp.data)
        assert parsed['status'] == 'error'
        assert parsed["msg"] == "Invalid input data"

    def test_wrong_numbers_count(self):
        req = "{'observation':{'color': 'green', 'numbers': ['1110111', '0011101', '1111111']}, 'sequence': '12'}"
        resp = self.app.post('/observation/add', data=req)
        parsed = json.loads(resp.data)
        assert parsed['status'] == 'error'
        assert parsed["msg"] == "Invalid input data"

    def test_wrong_numbers_count_1(self):
        req = "{'observation':{'color': 'green', 'numbers': ['1110111']}, 'sequence': '12'}"
        resp = self.app.post('/observation/add', data=req)
        parsed = json.loads(resp.data)
        assert parsed['status'] == 'error'
        assert parsed["msg"] == "Invalid input data"

    def test_wrong_format_no_sequence(self):
        req = "{'observation':{'color': 'green', 'numbers': ['1110111', '0011101']}}"
        resp = self.app.post('/observation/add', data=req)
        parsed = json.loads(resp.data)
        assert parsed['status'] == 'error'
        assert parsed["msg"] == "Invalid input data"

    def test_wrong_format_no_color(self):
        req = "{'observation':{'numbers': ['1110111', '0011101']}, 'sequence': '12'}"
        resp = self.app.post('/observation/add', data=req)
        parsed = json.loads(resp.data)
        assert parsed['status'] == 'error'
        assert parsed["msg"] == "Invalid input data"

    def test_wrong_format_no_numbers(self):
        req = "{'observation':{'color': 'green'}, 'sequence': '12'}"
        resp = self.app.post('/observation/add', data=req)
        parsed = json.loads(resp.data)
        assert parsed['status'] == 'error'
        assert parsed["msg"] == "Invalid input data"

    def test_wrong_format_no_observation(self):
        req = "{'sequence': '12'}"
        resp = self.app.post('/observation/add', data=req)
        parsed = json.loads(resp.data)
        assert parsed['status'] == 'error'
        assert parsed["msg"] == "Invalid input data"

    def new_seq(self):
        resp = self.app.post('/sequence/create', data='{}')
        return json.loads(resp.data)['response']['sequence']

    def test_first_red(self):
        resp = self.app.get('/clear')
        seq = self.new_seq()

        req = "{'observation': {'color': 'red','numbers': ['1110111', '0011101']  }, 'sequence': '" + seq + "'}"
        resp = self.app.post('/observation/add', data=req)

        parsed = json.loads(resp.data)
        assert parsed['status'] == 'error'
        assert parsed['msg'] == "There isn't enough data"

    def test_first_red2(self):
        resp = self.app.get('/clear')
        seq = self.new_seq()

        req = "{'observation': {'color': 'green','numbers': ['1110111', '0011101']  }, 'sequence': '" + seq + "'}"
        resp = self.app.post('/observation/add', data=req)

        req = "{'observation': {'color': 'red','numbers': ['1110111', '0011101']  }, 'sequence': '" + seq + "'}"
        resp = self.app.post('/observation/add', data=req)

        req = "{'observation': {'color': 'green','numbers': ['1110111', '0011101']  }, 'sequence': '" + seq + "'}"
        resp = self.app.post('/observation/add', data=req)

        parsed = json.loads(resp.data)
        assert parsed['status'] == 'error'
        assert parsed['msg'] == "The red observation should be the last"

    D_S_1 = ['0010111',  # 0
             '0010010',  # 1
             '0011101',  # 2
             '0011011',  # 3
             '0011010',  # 4
             '0001011',  # 5
             '0001111',  # 6
             '0010010',  # 7
             '0011111',  # 8
             '0011011']  # 9

    def req(self, code1, code2, seq):
        return "{'observation': {'color': 'green','numbers': ['" + code1 + "', '" + code2 + "']  }, 'sequence': '" + seq + "'}"

    def test_observation_1(self):
        resp = self.app.get('/clear')
        seq = self.new_seq()

        req = self.req(self.D_S_1[0], self.D_S_1[9], seq)
        resp = self.app.post('/observation/add', data=req)
        startNums = json.loads(resp.data)['response']['start']
        self.assertIn(9, startNums)

        req = self.req(self.D_S_1[0], self.D_S_1[8], seq)
        resp = self.app.post('/observation/add', data=req)
        startNums = json.loads(resp.data)['response']['start']
        self.assertIn(9, startNums)

        req = self.req(self.D_S_1[0], self.D_S_1[7], seq)
        resp = self.app.post('/observation/add', data=req)
        startNums = json.loads(resp.data)['response']['start']
        self.assertIn(9, startNums)

        req = self.req(self.D_S_1[0], self.D_S_1[6], seq)
        resp = self.app.post('/observation/add', data=req)
        startNums = json.loads(resp.data)['response']['start']
        self.assertIn(9, startNums)

        req = self.req(self.D_S_1[0], self.D_S_1[5], seq)
        resp = self.app.post('/observation/add', data=req)
        startNums = json.loads(resp.data)['response']['start']
        self.assertIn(9, startNums)

        req = self.req(self.D_S_1[0], self.D_S_1[4], seq)
        resp = self.app.post('/observation/add', data=req)
        startNums = json.loads(resp.data)['response']['start']
        self.assertIn(9, startNums)

        req = self.req(self.D_S_1[0], self.D_S_1[3], seq)
        resp = self.app.post('/observation/add', data=req)
        startNums = json.loads(resp.data)['response']['start']
        self.assertIn(9, startNums)

        req = self.req(self.D_S_1[0], self.D_S_1[2], seq)
        resp = self.app.post('/observation/add', data=req)
        startNums = json.loads(resp.data)['response']['start']
        self.assertIn(9, startNums)

        req = self.req(self.D_S_1[0], self.D_S_1[1], seq)
        resp = self.app.post('/observation/add', data=req)
        startNums = json.loads(resp.data)['response']['start']
        self.assertIn(9, startNums)

        req = "{'observation': {'color': 'red'}, 'sequence': '" + seq + "'}"
        resp = self.app.post('/observation/add', data=req)
        startNums = json.loads(resp.data)['response']['start']
        self.assertIn(9, startNums)


    def test_observation_2(self):
        resp = self.app.get('/clear')
        seq = self.new_seq()

        req = self.req(self.D_S_1[2], self.D_S_1[9], seq)
        resp = self.app.post('/observation/add', data=req)
        startNums = json.loads(resp.data)['response']['start']
        self.assertIn(29, startNums)

        req = self.req(self.D_S_1[2], self.D_S_1[8], seq)
        resp = self.app.post('/observation/add', data=req)
        startNums = json.loads(resp.data)['response']['start']
        self.assertIn(29, startNums)

        req = self.req(self.D_S_1[2], self.D_S_1[7], seq)
        resp = self.app.post('/observation/add', data=req)
        startNums = json.loads(resp.data)['response']['start']
        self.assertIn(29, startNums)

        req = self.req(self.D_S_1[2], self.D_S_1[6], seq)
        resp = self.app.post('/observation/add', data=req)
        startNums = json.loads(resp.data)['response']['start']
        self.assertIn(29, startNums)

        req = self.req(self.D_S_1[2], self.D_S_1[5], seq)
        resp = self.app.post('/observation/add', data=req)
        startNums = json.loads(resp.data)['response']['start']
        self.assertIn(29, startNums)

        req = self.req(self.D_S_1[2], self.D_S_1[4], seq)
        resp = self.app.post('/observation/add', data=req)
        startNums = json.loads(resp.data)['response']['start']
        self.assertIn(29, startNums)

        req = self.req(self.D_S_1[2], self.D_S_1[3], seq)
        resp = self.app.post('/observation/add', data=req)
        startNums = json.loads(resp.data)['response']['start']
        self.assertIn(29, startNums)

        req = self.req(self.D_S_1[2], self.D_S_1[2], seq)
        resp = self.app.post('/observation/add', data=req)
        startNums = json.loads(resp.data)['response']['start']
        self.assertIn(29, startNums)

        req = self.req(self.D_S_1[2], self.D_S_1[1], seq)
        resp = self.app.post('/observation/add', data=req)
        startNums = json.loads(resp.data)['response']['start']
        self.assertIn(29, startNums)

        req = self.req(self.D_S_1[2], self.D_S_1[0], seq)
        resp = self.app.post('/observation/add', data=req)
        startNums = json.loads(resp.data)['response']['start']
        self.assertIn(29, startNums)

        req = self.req(self.D_S_1[1], self.D_S_1[9], seq)
        resp = self.app.post('/observation/add', data=req)
        startNums = json.loads(resp.data)['response']['start']
        self.assertIn(29, startNums)

        req = self.req(self.D_S_1[1], self.D_S_1[8], seq)
        resp = self.app.post('/observation/add', data=req)
        startNums = json.loads(resp.data)['response']['start']
        self.assertIn(29, startNums)

    def test_skipped(self):
        resp = self.app.get('/clear')
        seq = self.new_seq()

        req = {'observation': {'color': 'green', 'numbers': ['1110111', '0010000']}, 'sequence': seq}
        resp = self.app.post('/observation/add', data=json.dumps(req))

        req = {'observation': {'color': 'red'}, 'sequence': seq}
        resp = self.app.post('/observation/add', data=json.dumps(req))

        parsed = json.loads(resp.data)
        startNums = parsed['response']['start']
        self.assertEquals([1], startNums)

        missing = parsed['response']['missing']
        self.assertEquals(["0000000", "0000010"], missing)

    def test_skipped_2(self):
        resp = self.app.get('/clear')
        seq = self.new_seq()

        req = {'observation': {'color': 'green', 'numbers': ['1110111', '1011101']}, 'sequence': seq}
        resp = self.app.post('/observation/add', data=json.dumps(req))

        req = {'observation': {'color': 'green', 'numbers': ['1110111', '0010010']}, 'sequence': seq}
        resp = self.app.post('/observation/add', data=json.dumps(req))

        req = {'observation': {'color': 'red'}, 'sequence': seq}
        resp = self.app.post('/observation/add', data=json.dumps(req))

        parsed = json.loads(resp.data)
        startNums = parsed['response']['start']
        self.assertEquals([2], startNums)

        missing = parsed['response']['missing']
        self.assertEquals(["0000000", "0000000"], missing)


if __name__ == '__main__':
    unittest.main()