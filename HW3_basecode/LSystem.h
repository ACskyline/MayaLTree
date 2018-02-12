#ifndef LSystem_H_
#define LSystem_H_

#include <string>
#include <vector>
#include <map>
#include "vec.h"

int test(int a);

extern "C" int test0(int a);

class LSystem
{
public:
    typedef std::pair<vec3, std::string> Geometry;
    typedef std::pair<vec3, vec3> Branch;

	static int test2(int a);
	int test3(int a);

public:
    LSystem();
    ~LSystem() {}

    // Set/get inputs
    void loadProgram(const std::string& fileName);
    void loadProgramFromString(const std::string& program);
    void setDefaultAngle(float degrees);
    void setDefaultStep(float distance);

    float getDefaultAngle() const;
    float getDefaultStep() const;
    const std::string& getGrammarString() const;

    // Iterate grammar
    const std::string& getIteration(unsigned int n);

    // Get geometry from running the turtle
    void process(unsigned int n, 
        std::vector<Branch>& branches);
    void process(unsigned int n, 
        std::vector<Branch>& branches, 
        std::vector<Geometry>& models);

	// Process the L-System and return the branches and the flowers.
	void processPy(unsigned int n,
		std::vector<std::vector<float> >& branches, 
        std::vector<std::vector<float> >& flowers);

protected:
    void reset();
    void addProduction(std::string line);
    std::string iterate(const std::string& input);
    
    std::map<std::string, std::string> productions;
    std::vector<std::string> iterations;
    std::vector<Branch> bboxes;
    std::string current;
    float mDfltAngle;
    float mDfltStep;
    std::string mGrammar;

    class Turtle
    {
    public:
        Turtle();
        Turtle(const Turtle& t);
        Turtle& operator=(const Turtle& t);

        void moveForward(float distance);
        void applyUpRot(float degrees);
        void applyLeftRot(float degrees);
        void applyForwardRot(float degrees);

        vec3 pos;
        vec3 up;
        vec3 forward;
        vec3 left;
    };
};

#endif