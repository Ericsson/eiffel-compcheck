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

def report(unsatisfiedDependencies, dependencies):
  print(len(unsatisfiedDependencies), "of", len(dependencies), "dependencies unsatisfied.")
  print("--------------------------------------------")
  for d in unsatisfiedDependencies:
     print(json.dumps(d, indent=2, separators=(",", ": ")))
     print("--------------------------------------------")

def findDependencies(events):
  dependencies = []
  for e in events:
    if e['meta']['type'] == "EiffelArtifactCreatedEvent" and 'dependsOn' in e['data']:
      for dependency in e['data']['dependsOn']:
        dependencies.append(dependency)
      
  return dependencies
 
def checkDependencies(dependencies, artifacts):
  unsatisfiedDependencies = []
  
  for d in dependencies:
    satisfied = False
    for a in artifacts:
      if artifactMatchesDependency(d, a):
        satisfied = True
        break
    if not satisfied:
      unsatisfiedDependencies.append(d)
 
  return unsatisfiedDependencies
  
def main(input):
  events = parseInput(input)
  print("Received", len(events), "events.")
  
  artifacts = findArtifacts(events)
  dependencies = findDependencies(events)
  unsatisfiedDependencies = checkDependencies(dependencies, artifacts)
  
  report(unsatisfiedDependencies, dependencies)
  
  if len(unsatisfiedDependencies) > 0:
    sys.exit("Validation failed.")

description = "    This script checks the validity of an Eiffel composition.\n    It reads a JSON array of Eiffel events constituting the elements of the composition,\n    and checks whether all dependencies are satisfied.\n    If any failures were detected, the script will print a summary and exit with code 1."
main(getInput(description))

