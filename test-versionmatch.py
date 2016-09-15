#!/usr/bin/env python

# Copyright 2016 Ericsson AB.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
# http://www.apache.org/licenses/LICENSE-2.0
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

import sys
from versionmatch import versionMatchesRangesString
from versionmatch import getRangesAndVersions
from versionmatch import isLesserEqualsGreater

failures = 0

if versionMatchesRangesString("1.0.0", "1.0.0") == False: failures += 1
if versionMatchesRangesString("1.0.0", "1.0.1") == True: failures += 1
if versionMatchesRangesString("1.0.0", "[1.0.0,)") == False: failures += 1
if versionMatchesRangesString("1.0.5", "(1.0.0,1.9]") == False: failures += 1
if versionMatchesRangesString("1.0.0", "[1.0.0,)") == False: failures += 1
if versionMatchesRangesString("1.0.0", "(1.0.0,)") == True: failures += 1
if versionMatchesRangesString("1.0.0", "(1.0,)") == False: failures += 1
if versionMatchesRangesString("1.0.0", "(,)") == False: failures += 1
if versionMatchesRangesString("1.0.0", "(,1.0)") == True: failures += 1
if versionMatchesRangesString("1.0", "(,1.0.0)") == False: failures += 1
if versionMatchesRangesString("1.0.0", "(,1.0.0)") == True: failures += 1
if versionMatchesRangesString("1.0.0", "(,1.0.0]") == False: failures += 1
if versionMatchesRangesString("1.0.0", "(5,1.0.0]") == True: failures += 1
if versionMatchesRangesString("G", "[A,D], G, J, (K, M]") == False: failures += 1
if versionMatchesRangesString("B", "[A,D], G, J, (K, M]") == False: failures += 1
if versionMatchesRangesString("L", "[A,D], G, J, (K, M]") == False: failures += 1
if versionMatchesRangesString("K", "[A,D], G, J, (K, M]") == True: failures += 1
if versionMatchesRangesString("H", "[A,D], G, J, (K, M]") == True: failures += 1

if isLesserEqualsGreater("A", "5") != "1": failures += 1
if isLesserEqualsGreater("1.10.0", "1.9.0") != "1": failures += 1
if isLesserEqualsGreater("1.0.0", "1.0.0") != "0": failures += 1
if isLesserEqualsGreater("1.0.1", "1.0.0") != "1": failures += 1
if isLesserEqualsGreater("0.9.0", "1.0.0") != "-1": failures += 1
if isLesserEqualsGreater("1.0.0", "1.0") != "1": failures += 1
if isLesserEqualsGreater("1.0", "1.0.0") != "-1": failures += 1
if isLesserEqualsGreater("R1A", "R1A") != "0": failures += 1
if isLesserEqualsGreater("R1A", "R1B") != "-1": failures += 1
if isLesserEqualsGreater("R1C", "R1B") != "1": failures += 1
if isLesserEqualsGreater("R5C", "R6B") != "-1": failures += 1
if isLesserEqualsGreater("R1A.3", "R1A.2") != "1": failures += 1
if isLesserEqualsGreater("R1A.2", "R1A.3") != "-1": failures += 1
if isLesserEqualsGreater("1.0.A", "1.0.B") != "-1": failures += 1

if getRangesAndVersions("1.0.0") != ([], ["1.0.0"]): failures += 1
if getRangesAndVersions("[1.0.0,2.0.0)") != (["[1.0.0,2.0.0)"], []): failures += 1
if getRangesAndVersions("[1.0.0,2.0.0),[3.0.0,4.0.0)") != (["[1.0.0,2.0.0)", "[3.0.0,4.0.0)"], []): failures += 1
if getRangesAndVersions("[1.0.0,2.0.0),3.0.5") != (["[1.0.0,2.0.0)"], ["3.0.5"]): failures += 1
if getRangesAndVersions("[R1A,R2C],R2F,[R3A,)") != (["[R1A,R2C]","[R3A,)"], ["R2F"]): failures += 1

#if not isCommaRangeSplitting("1,2", 1): failures += 1
#if isCommaRangeSplitting("1,", 1): failures += 1
#if isCommaRangeSplitting(",2", 0): failures += 1
#if isCommaRangeSplitting("[1,2)", 0): failures += 1

print(failures,"tests failed")
if failures > 0:
  sys.exit(1)

