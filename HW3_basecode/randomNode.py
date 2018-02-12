# randomNode.py
#   Produces random locations to be used with the Maya instancer node.

import sys
import random

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
kPluginNodeTypeName = "randomNode"

# Give the node a unique ID. Make sure this ID is different from all of your
# other nodes!
randomNodeId = OpenMaya.MTypeId(0x8704)

# Node definition
class randomNode(OpenMayaMPx.MPxNode):
    # Declare class variables:
    # TODO:: declare the input and output class variables
    #         i.e. inNumPoints = OpenMaya.MObject()
    inNumPoints = OpenMaya.MObject()
    minBound = OpenMaya.MObject()
    minX = OpenMaya.MObject()
    minY = OpenMaya.MObject()
    minZ = OpenMaya.MObject()
    maxBound = OpenMaya.MObject()
    maxX = OpenMaya.MObject()
    maxY = OpenMaya.MObject()
    maxZ = OpenMaya.MObject()

    outPoints = OpenMaya.MObject()
    
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
        if(plug == randomNode.outPoints) :
            print "I'm inside\n"
            inNHandle = data.inputValue(randomNode.inNumPoints)
            inN = inNHandle.asInt()

            minBHandle = data.inputValue(randomNode.minBound)
            minB = minBHandle.asDouble3()

            miX = minB[0]
            miY = minB[1]
            miZ = minB[2]

            maxBHandle = data.inputValue(randomNode.maxBound)
            maxB = maxBHandle.asDouble3()

            maX = maxB[0]
            maY = maxB[1]
            maZ = maxB[2]

            pointsData = data.outputValue(randomNode.outPoints)
            pointsAAD = OpenMaya.MFnArrayAttrsData()
            pointsObject = pointsAAD.create()

            positionArray = pointsAAD.vectorArray("position")
            idArray = pointsAAD.doubleArray("id")

            x = 0
            while x < inN :
                positionArray.append(OpenMaya.MVector(random.uniform(miX, maX), random.uniform(miY, maY), random.uniform(miZ, maZ)))
                idArray.append(x)
                print "x\n"
                x = x + 1

            pointsData.setMObject(pointsObject)

            data.setClean(plug)

        else :
            print plug.name()
            if(randomNode.outPoints.isNull()) :
                print "Foook"
        
    
# initializer
def nodeInitializer():
    tAttr = OpenMaya.MFnTypedAttribute()
    nAttr = OpenMaya.MFnNumericAttribute()
    cAttrMin = OpenMaya.MFnCompoundAttribute()
    cAttrMax = OpenMaya.MFnCompoundAttribute()
    
    # TODO:: initialize the input and output attributes. Be sure to use the 
    #         MAKE_INPUT and MAKE_OUTPUT functions.
    randomNode.inNumPoints = nAttr.create("inNum", "inN", OpenMaya.MFnNumericData.kInt, 10);

    randomNode.minX = nAttr.create("minX", "mix", OpenMaya.MFnNumericData.kDouble, 0.0)
    randomNode.minY = nAttr.create("minY", "miy", OpenMaya.MFnNumericData.kDouble, 0.0)
    randomNode.minZ = nAttr.create("minZ", "miz", OpenMaya.MFnNumericData.kDouble, 0.0)
    randomNode.minBound = cAttrMin.create("minBound", "minB");#create before add child
    cAttrMin.addChild(randomNode.minX)
    cAttrMin.addChild(randomNode.minY)
    cAttrMin.addChild(randomNode.minZ)
    
    randomNode.maxX = nAttr.create("maxX", "max", OpenMaya.MFnNumericData.kDouble, 10.0)
    randomNode.maxY = nAttr.create("maxY", "may", OpenMaya.MFnNumericData.kDouble, 10.0)
    randomNode.maxZ = nAttr.create("maxZ", "maz", OpenMaya.MFnNumericData.kDouble, 10.0)
    randomNode.maxBound = cAttrMax.create("maxBound", "maxB");#create before add child
    cAttrMax.addChild(randomNode.maxX)
    cAttrMax.addChild(randomNode.maxY)
    cAttrMax.addChild(randomNode.maxZ)
    
    randomNode.outPoints = tAttr.create("outPoints", "outP", OpenMaya.MFnArrayAttrsData.kDynArrayAttrs)

    if(randomNode.outPoints.isNull()) :
        print "shiiiiiiit"

    MAKE_INPUT(nAttr)
    MAKE_INPUT(cAttrMax)
    MAKE_INPUT(cAttrMin)

    MAKE_OUTPUT(tAttr)

    try:
        # TODO:: add the attributes to the node and set up the
        #         attributeAffects (addAttribute, and attributeAffects)


        randomNode.addAttribute(randomNode.minBound)


        randomNode.addAttribute(randomNode.maxBound)
        
        randomNode.addAttribute(randomNode.inNumPoints)

        randomNode.addAttribute(randomNode.outPoints)

        randomNode.attributeAffects(randomNode.minBound, randomNode.outPoints)
        
        randomNode.attributeAffects(randomNode.maxBound, randomNode.outPoints)

        randomNode.attributeAffects(randomNode.inNumPoints, randomNode.outPoints)

        print "Initialization!\n"

    except:
        sys.stderr.write(("Failed to create attributes of %s node\n", kPluginNodeTypeName))

# creator
def nodeCreator():
    return OpenMayaMPx.asMPxPtr( randomNode() )

# initialize the script plug-in
def initializePlugin(mobject):
    mplugin = OpenMayaMPx.MFnPlugin(mobject)
    try:
        mplugin.registerNode( kPluginNodeTypeName, randomNodeId, nodeCreator, nodeInitializer )
    except:
        sys.stderr.write( "Failed to register node: %s\n" % kPluginNodeTypeName )

# uninitialize the script plug-in
def uninitializePlugin(mobject):
    mplugin = OpenMayaMPx.MFnPlugin(mobject)
    try:
        mplugin.deregisterNode( randomNodeId )
    except:
        sys.stderr.write( "Failed to unregister node: %s\n" % kPluginNodeTypeName )
