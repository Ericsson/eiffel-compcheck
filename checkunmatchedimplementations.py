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
import json
from compcheck import parseInput, readInputFromFile, artifactMatchesDependency, findArtifacts, getInput

def report(unmatchedImplementations, implementations):
  print(len(unmatchedImplementations), "of", len(implementations), "implementations unmatched.")
  print("--------------------------------------------")
  for i in unmatchedImplementations:
     print(json.dumps(i, indent=2, separators=(",", ": ")))
     print("--------------------------------------------")
     
def findImplementations(events):
  implementations = []
  for e in events:
    if e['meta']['type'] == "EiffelArtifactCreatedEvent" and 'implements' in e['data']:
      for implementation in e['data']['implements']:
        implementations.append(implementation)
      
  return implementations

def checkImplementations(implementations, artifacts):
  unmatchedImplementations = []

  for i in implementations:
    matched = False
    for a in artifacts:
      if artifactMatchesDependency(i, a):
        matched = True
        break
    if not matched:
      unmatchedImplementations.append(i)
  
  return unmatchedImplementations
  
def main(input):
  events = parseInput(input)
  print("Received", len(events), "events.")
  
  artifacts = findArtifacts(events)
  implementations = findImplementations(events)
  unmatchedImplementations = checkImplementations(implementations, artifacts)
  
  report(unmatchedImplementations, implementations)
  if len(unmatchedImplementations) > 0:
    sys.exit("Validation failed.")

description = "    This script checks the validity of an Eiffel composition.\n    It reads a JSON array of Eiffel events constituting the elements of the composition,\n    and checks for \"implements\" declarations unmatched by any artifact present in the composition.\n    If any failures were detected, the script will print a summary and exit with code 1."
main(getInput(description))
