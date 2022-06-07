#!/usr/bin/env python3

# Copyright (c) Jeremías Casteglione <jeremias@talkingpts.org>
# See LICENSE file.

import unittest
from unittest.mock import MagicMock

class Test(unittest.TestCase):

	def test_fake(t):
		t.assertEqual(1, 1)

if __name__ == '__main__':
	unittest.main()
