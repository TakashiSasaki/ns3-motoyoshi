#!python
#export PYTHONPATH=/home/sasaki.takashi.mg/ns3-2016/workspace/ns-allinone-3.25/ns-3.25/build/bindings/python
#export LD_LIBRARY_PATH=/home/sasaki.takashi.mg/ns3-2016/workspace/ns-allinone-3.25/ns-3.25/build

import ns
import ns.core
import ns.network

object_factory = ns.core.ObjectFactory()
object_factory.SetTypeId("ns3::RateErrorModel")
object_factory.Set("ErrorRate", ns.core.DoubleValue(100))
error_model = object_factory.Create()
print(error_model)



