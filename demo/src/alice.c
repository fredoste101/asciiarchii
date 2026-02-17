#include "messages.h"

void somethingHappening()
{
	// la la la

}


void sendToCharlie()
{
	//Send it.
}


void receiveBobSignal(Signal* s)
{
	//do things
	sendToCharlie()
}


void sendMessageToBob(const char* msg)
{
	//Send something to bob
	Greeting g;
	//Send to bob somehow, socket or msgq, or pipe or signal or shared mem... doesn't matter
}


void getFinalMessage(FinalMessage* fm)
{
	//We got the final message! yeah!
}


/*
 * Alice process or thread
 */
void Alice(void* input)
{
	/* something something alice */


	somethingHappening();

	sendMessageToBob("hi bob")
}




