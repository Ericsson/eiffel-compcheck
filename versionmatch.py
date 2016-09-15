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

import re

def getRangeComponents(range):
  lowerBoundType = range[0]
  upperBoundType = range[-1]
  lowerBound = range[1:range.index(",")]
  upperBound = range[range.index(",") + 1:-1]
  
  return lowerBoundType, lowerBound, upperBound, upperBoundType
  
def compareVersionElement(a, b):
  maxlen = max(len(a),len(b))
  a = a.zfill(maxlen)
  b = b.zfill(maxlen)

  if a > b:
    return "1"
  
  if a < b:
    return "-1"
    
  return 0
  
def isLesserEqualsGreater(a, b):
  aElements = a.split(".")
  bElements = b.split(".")
  
  for x in range(max(len(aElements),len(bElements))):
    if x >= len(bElements):
      return "1"
  
    if x >= len(aElements):
      return "-1"
  
    elementComparison = compareVersionElement(aElements[x], bElements[x])
    if elementComparison != 0:
      return elementComparison
    
  return "0"
  
def isWithinLowerBound(version, lowerBound, lowerBoundType):
  if lowerBound == "" and lowerBoundType == "(":
    return True
    
  comparison = isLesserEqualsGreater(version, lowerBound)
  
  if comparison == "1":
    return True
    
  return comparison == "0" and lowerBoundType == "["

def isWithinUpperBound(version, upperBound, upperBoundType):
  if upperBound == "" and upperBoundType == ")":
    return True
    
  comparison = isLesserEqualsGreater(version, upperBound)
  
  if comparison == "-1":
    return True
    
  return comparison == "0" and upperBoundType == "]"
  
def getRangesAndVersions(input):
  input = re.sub(" ", "", input)
  regexp = "[\\[\\(].*?,.*?[\\]\\)]"
  ranges = re.findall(regexp, input)
  remainder = re.sub(regexp, "", input)
  
  versions = []
  for s in remainder.split(","):
    if s != "":
      versions.append(s)
  
  return ranges, versions

def versionMatchesSingleRange(version, range):
  lowerBoundType, lowerBound, upperBound, upperBoundType = getRangeComponents(range)
  
  if not isWithinLowerBound(version, lowerBound, lowerBoundType):
    return False
    
  if not isWithinUpperBound(version, upperBound, upperBoundType):
    return False
  
  return True

def versionMatchesRangesString(version, rangeString):
  ranges, versions = getRangesAndVersions(rangeString)
  
  for v in versions:
    if(version == v):
      return True
  
  for range in ranges:
    if versionMatchesSingleRange(version, range):
      return True
  
  return False
  
