#!/usr/bin/env bash


if [ $# -lt 1 ]
then
    echo Usage: ./solve.sh scen[0-9][0-9]
    exit 1
fi

echo 'starting'
cd frodo2
if [ $# -gt 1 ]
then
    echo 'computing...'
    java -cp frodo2.jar frodo2.algorithms.AgentFactory opti/celar-$1-all-opti.xml ./agents/SynchBB/SynchBBagentJaCoP.xml > ../$2
else
    java -cp frodo2.jar frodo2.algorithms.AgentFactory opti/celar-$1-all-opti.xml ./agents/SynchBB/SynchBBagentJaCoP.xml
fi
echo 'DONE'