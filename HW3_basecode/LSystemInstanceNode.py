# LSystemInstanceNode.py
#   Produces random locations to be used with the Maya instancer node.

import sys
import LSystem

import maya.OpenMaya as OpenMaya
import maya.OpenMayaAnim as OpenMayaAnim
import maya.OpenMayaMPx as OpenMayaMPx
import maya.cmds as cmds

# Useful functions for declaring attributes as inputs or outputs.
def MAKE_INPUT(attr):
    attr.setKeyable(True)
    attr.setStorable(True)
    attr.setReadable(True)
    attr.setWritable(True)
def MAKE_OUTPUT(attr):
    attr.setKeyable(False)
    attr.setStorable(False)
    attr.setReadable(True)
    attr.setWritable(False)

# Define the name of the node
kPluginNodeTypeName = "LSystemInstanceNode"

# Give the node a unique ID. Make sure this ID is different from all of your
# other nodes!
LSystemInstanceNodeId = OpenMaya.MTypeId(0x4444)
path = " "
# Node definition
class LSystemInstanceNode(OpenMayaMPx.MPxNode):
    # Declare class variables:
    # TODO:: declare the input and output class variables
    #         i.e. inNumPoints = OpenMaya.MObject()
    angle = OpenMaya.MObject()
    step = OpenMaya.MObject()
    grammar = OpenMaya.MObject()
    iteration = OpenMaya.MObject()
    time = OpenMaya.MObject()

    branches = OpenMaya.MObject()
    flowers = OpenMaya.MObject()
    
    # constructor
    def __init__(self):
        OpenMayaMPx.MPxNode.__init__(self)

    # compute
    def compute(self,plug,data):
        # TODO:: create the main functionality of the node. Your node should 
        #         take in three floats for max position (X,Y,Z), three floats 
        #         for min position (X,Y,Z), and the number of random points to
        #         be generated. Your node should output an MFnArrayAttrsData 
        #         object containing the random points. Consult the homework
        #         sheet for how to deal with creating the MFnArrayAttrsData. 

        print "I'm computing\n"
        if(plug == LSystemInstanceNode.branches or plug == LSystemInstanceNode.flowers) :
            print "I'm inside\n"
            angleHandle = data.inputValue(LSystemInstanceNode.angle)
            d_angle = angleHandle.asDouble()

            stepHandle = data.inputValue(LSystemInstanceNode.step)
            d_step = stepHandle.asDouble()

            grammarHandle = data.inputValue(LSystemInstanceNode.grammar)
            s_grammar = str(grammarHandle.asString())
            
            iterationHandle = data.inputValue(LSystemInstanceNode.iteration)
            i_iteration = iterationHandle.asInt()

            timeHandle = data.inputValue(LSystemInstanceNode.time)
            t_time = timeHandle.asTime()
            i_time = int(t_time.asUnits(OpenMaya.MTime.kFilm))

            branchesHandle = data.outputValue(LSystemInstanceNode.branches)
            branchesAAD = OpenMaya.MFnArrayAttrsData()
            branchesObject = branchesAAD.create()

            branchesPositionArray = branchesAAD.vectorArray("position")
            branchesIdArray = branchesAAD.doubleArray("id")
            branchesScaleArray = branchesAAD.vectorArray("scale")
            branchesAimArray = branchesAAD.vectorArray("aimDirection")

            flowersHandle = data.outputValue(LSystemInstanceNode.flowers)
            flowersAAD = OpenMaya.MFnArrayAttrsData()
            flowersObject = flowersAAD.create()

            flowersPositionArray = flowersAAD.vectorArray("position")
            flowersIdArray = flowersAAD.doubleArray("id")
            flowersScaleArray = flowersAAD.vectorArray("scale")
            flowersAimArray = flowersAAD.vectorArray("aimDirection")

            vecBranch = LSystem.VectorPyBranch()
            vecFlower = LSystem.VectorPyBranch()
            l = LSystem.LSystem()

            l.setDefaultAngle(d_angle)
            l.setDefaultStep(d_step)
            l.loadProgram(s_grammar)#s_grammar
            l.processPy(i_time, vecBranch, vecFlower)#iteration

            i = 0
            for x in vecBranch :
                length = ((x[0] - x[3])*(x[0] - x[3]) + (x[1] - x[4])*(x[1] - x[4]) + (x[2] - x[5])*(x[2] - x[5])) ** 0.5
                branchesPositionArray.append(OpenMaya.MVector((x[0]+x[3])/2, (x[1]+x[4])/2, (x[2]+x[5])/2))
                branchesIdArray.append(i)
                branchesScaleArray.append(OpenMaya.MVector(length, 1, 1))
                branchesAimArray.append(OpenMaya.MVector((x[3] - x[0]), (x[4] - x[1]), (x[5] - x[2])))
                i += 1
                print i

            i = 0
            for x in vecFlower :
                length = (x[0]*x[0] + x[1]*x[1] + x[2]*x[2]) ** 0.5
                flowersPositionArray.append(OpenMaya.MVector(x[0], x[1], x[2]))
                flowersIdArray.append(i)
                flowersScaleArray.append(OpenMaya.MVector(1, 1, 1))
                flowersAimArray.append(OpenMaya.MVector(x[0], x[1], x[2]))
                i += 1
                print i

            branchesHandle.setMObject(branchesObject)
            flowersHandle.setMObject(flowersObject)

            data.setClean(plug)

        else :
            print plug.name()
        
    
# initializer
def nodeInitializer():
    branchesAttr = OpenMaya.MFnTypedAttribute()
    flowersAttr = OpenMaya.MFnTypedAttribute()
    iAttr = OpenMaya.MFnNumericAttribute()
    sAttr = OpenMaya.MFnTypedAttribute()
    dAttr = OpenMaya.MFnNumericAttribute()
    uAttr = OpenMaya.MFnUnitAttribute()
    
    # TODO:: initialize the input and output attributes. Be sure to use the 
    #         MAKE_INPUT and MAKE_OUTPUT functions.
    print "I'm in nodeInitiializer" + path
    sD = OpenMaya.MFnStringData()
    sDObject = sD.create(path)
    LSystemInstanceNode.angle = dAttr.create("angle", "a", OpenMaya.MFnNumericData.kDouble, 10.0)
    LSystemInstanceNode.step = dAttr.create("step", "s", OpenMaya.MFnNumericData.kDouble, 10.0)
    LSystemInstanceNode.grammar = sAttr.create("grammar", "g", OpenMaya.MFnData.kString, sDObject)
    LSystemInstanceNode.iteration = iAttr.create("iteration", "i", OpenMaya.MFnNumericData.kInt, 3)

    LSystemInstanceNode.time = uAttr.create("time", "t", OpenMaya.MFnUnitAttribute.kTime, 1)

    LSystemInstanceNode.branches = branchesAttr.create("branches", "b", OpenMaya.MFnArrayAttrsData.kDynArrayAttrs)
    LSystemInstanceNode.flowers = flowersAttr.create("flowers", "f", OpenMaya.MFnArrayAttrsData.kDynArrayAttrs)

    if(LSystemInstanceNode.branches.isNull() or LSystemInstanceNode.flowers.isNull()) :
        print "shiiiiiiit"

    MAKE_INPUT(dAttr)
    MAKE_INPUT(sAttr)
    MAKE_INPUT(iAttr)

    MAKE_INPUT(uAttr)

    MAKE_OUTPUT(branchesAttr)
    MAKE_OUTPUT(flowersAttr)

    try:
        # TODO:: add the attributes to the node and set up the
        #         attributeAffects (addAttribute, and attributeAffects)


        LSystemInstanceNode.addAttribute(LSystemInstanceNode.angle)
        LSystemInstanceNode.addAttribute(LSystemInstanceNode.step)
        LSystemInstanceNode.addAttribute(LSystemInstanceNode.grammar)
        LSystemInstanceNode.addAttribute(LSystemInstanceNode.iteration)

        LSystemInstanceNode.addAttribute(LSystemInstanceNode.time)
        
        LSystemInstanceNode.addAttribute(LSystemInstanceNode.branches)
        LSystemInstanceNode.addAttribute(LSystemInstanceNode.flowers)

        LSystemInstanceNode.attributeAffects(LSystemInstanceNode.angle, LSystemInstanceNode.branches)
        LSystemInstanceNode.attributeAffects(LSystemInstanceNode.step, LSystemInstanceNode.branches)
        LSystemInstanceNode.attributeAffects(LSystemInstanceNode.grammar, LSystemInstanceNode.branches)
        LSystemInstanceNode.attributeAffects(LSystemInstanceNode.iteration, LSystemInstanceNode.branches)

        LSystemInstanceNode.attributeAffects(LSystemInstanceNode.time, LSystemInstanceNode.branches)
        
        LSystemInstanceNode.attributeAffects(LSystemInstanceNode.angle, LSystemInstanceNode.flowers)
        LSystemInstanceNode.attributeAffects(LSystemInstanceNode.step, LSystemInstanceNode.flowers)
        LSystemInstanceNode.attributeAffects(LSystemInstanceNode.grammar, LSystemInstanceNode.flowers)
        LSystemInstanceNode.attributeAffects(LSystemInstanceNode.iteration, LSystemInstanceNode.flowers)

        LSystemInstanceNode.attributeAffects(LSystemInstanceNode.time, LSystemInstanceNode.flowers)

        print "Initialization!\n"

    except:
        sys.stderr.write(("Failed to create attributes of %s node\n", kPluginNodeTypeName))

# creator
def nodeCreator():
    return OpenMayaMPx.asMPxPtr( LSystemInstanceNode() )

# initialize the script plug-in
def initializePlugin(mobject):
    mplugin = OpenMayaMPx.MFnPlugin(mobject)
    global path
    path = mplugin.loadPath() + "/plants/flower1.txt"
    print path
    try:
        mplugin.registerNode( kPluginNodeTypeName, LSystemInstanceNodeId, nodeCreator, nodeInitializer )
    except:
        sys.stderr.write( "Failed to register node: %s\n" % kPluginNodeTypeName )

# uninitialize the script plug-in
def uninitializePlugin(mobject):
    mplugin = OpenMayaMPx.MFnPlugin(mobject)
    try:
        mplugin.deregisterNode( LSystemInstanceNodeId )
    except:
        sys.stderr.write( "Failed to unregister node: %s\n" % kPluginNodeTypeName )
